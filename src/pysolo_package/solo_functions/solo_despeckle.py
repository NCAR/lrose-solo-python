from copy import deepcopy
import ctypes
import os
import numpy as np
from multiprocessing import Manager, shared_memory, cpu_count, Process, Array
import math
import logging
import psutil

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases

se_despeckle = aliases['despeckle']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(process)d] - %(message)s')

def despeckle(input_list_data, bad, a_speckle, input_list_mask=None, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a despeckle operation on a list of data (a single ray)

        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            a_speckle: An integer that determines the number of contiguous good data considered a speckle,
            (optional) input_list_mask: A list of bools for masking valid/invalid values for input_list (default: a list with True entries for all 'bad' values in 'input_list_data'),
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list),
            (optional) boundary_mask: this is the masked region bool list where the function will perform its operation (default: all True, so operation performed on entire region).

        Returns:
            RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    # if input_list_mask was provided, check if it's the same size as input_list_data
    if (input_list_mask != None and len(input_list_data) != len(input_list_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list_data), len(input_list_mask)))

    # set return type and arg types
    se_despeckle.restype = None
    se_despeckle.argtypes = [
        ctypes.POINTER(ctypes.c_float),        # data
        ctypes.POINTER(ctypes.c_float),        # newData
        ctypes.c_size_t,                       # nGates
        ctypes.c_float,                        # bad
        ctypes.c_int,                          # a_speckle
        ctypes.c_size_t,                       # dgi_clip_gate
        ctypes.POINTER(ctypes.c_bool)          # boundary_mask
        ]


    # retrieve size of input/output/mask array
    data_length = len(input_list_data)

    # optional parameters
    if boundary_mask == None:
        boundary_mask = [True] * data_length # set boundary_mask to all true, match size of input_list_data
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length 
    if input_list_mask == None:
        input_list_mask = [True if x == np.float32(bad) else False for x in input_list_data] # set mask to True on indexes with 'bad' value

    # create a ctypes float/bool array from a list of size data_length
    input_array = ctypes_helper.initialize_float_array(data_length, input_list_data)

    boundary_array = ctypes_helper.initialize_bool_array(data_length, boundary_mask)

    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)

    # run C function, output_array is updated with despeckle results
    se_despeckle(
        input_array,
        output_array,
        ctypes.c_size_t(data_length),
        ctypes.c_float(bad),
        ctypes.c_int(a_speckle),
        ctypes.c_size_t(dgi_clip_gate),
        boundary_array
    )

    # convert resultant ctypes array back to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    # the solo functions doesn't do this, but
    # update the mask for the new bad values created from the despeckle.
    output_list_mask, changes = ctypes_helper.update_boundary_mask(output_list, bad, input_list_mask)

    # returns the new data and masks packaged in an object
    return radar_structure.RayData(output_list, output_list_mask, changes)


def despeckle_masked(masked_array, a_speckle, boundary_mask=None, parallel=False):
    """
        Performs a despeckle operation on a numpy masked array

        Args:
            masked_array: A numpy masked array data structure,
            a_speckle: An integer that determines the number of contiguous good data considered a speckle

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """
    rayData = RayData(masked_array, a_speckle, boundary_mask, parallel)
    if parallel:
        rayData.run_parallel()
    else:
        rayData.run_serial() 

    # repackage as masked array and return
    output_masked_array = np.ma.masked_array(data=rayData.result_data, mask=rayData.result_mask, fill_value=rayData.missing)
    return output_masked_array


class RayData:
    def __init__(self, masked, a_speckle, boundary_mask, parallel):
        self.a_speckle = a_speckle
        self.boundary_mask = boundary_mask

        self.parallel = parallel

        self.missing = masked.fill_value
        self.mask_list = masked.mask.tolist()
        self.data_list = masked.tolist(self.missing)

        self.output_data = self.data_list
        self.output_mask = self.mask_list 
        

    def despeckle_rays(self, start, end):
        for ray in range(start, end):
            self.despeckle_single_ray(ray)


    def despeckle_single_ray(self, i):
        input_data = self.data_list[i]
        input_mask = self.mask_list[i]

        # and run despeckle on each individual ray
        despec = despeckle(input_data, self.missing, self.a_speckle, input_list_mask=input_mask, boundary_mask=self.boundary_mask)
        # despec returns resultant data and mask lists, append to output_data and output_mask
        if (self.parallel):
            with self.lock:
                self.shared_data[i] = despec.data
                self.shared_mask[i] = despec.mask
        else:
            self.output_data[i] = despec.data
            self.output_mask[i] = despec.mask



    def run_serial(self):
        self.despeckle_rays(0, len(self.data_list))
        self.result_data = list(self.output_data)
        self.result_mask = list(self.output_mask)


    def run_parallel(self):

        manager = Manager()
        self.shared_data = manager.list(self.output_data)
        self.shared_mask = manager.list(self.output_mask)
        self.lock = manager.Lock()

        processes = []
        chunks = []
        start = 0
        end = 0
        nums = list(range(0, len(self.data_list)))
        chunk_size = math.ceil(len(self.data_list) / cpu_count())

        for i in range(0, len(self.data_list), chunk_size):
            start = i
            end = start + chunk_size
            chunks.append( (start, end) )

        logging.info(chunks)

        logging.info("received chunk size of %d" % (chunk_size))
        for chunk in chunks:
            logging.info("processing chunks: %d to %d" % (chunk[0], chunk[1]))
            process = Process(target=self.despeckle_rays, args=(chunk[0], chunk[1]))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()
            logging.info("process finished.")

        self.result_data = list(self.shared_data)
        self.result_mask = list(self.shared_mask)
