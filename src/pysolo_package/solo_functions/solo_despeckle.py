import ctypes
import numpy as np
from multiprocessing import Manager, Process
import math
import psutil
import logging

from pysolo_package.utils.run_solo import run_solo_function
from pysolo_package.utils import radar_structure, DataPair
from pysolo_package.utils.function_alias import aliases

se_despeckle = aliases['despeckle']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(process)d] - %(message)s')

def despeckle(input_list_data, bad, a_speckle, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a despeckle operation on a list of data (a single ray)

        Args:
            input_list_data: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            a_speckle: An integer that determines the number of contiguous good data considered a speckle,
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list),
            (optional) boundary_mask: this is the masked region bool list where the function will perform its operation (default: all True, so operation performed on entire region).

        Returns:
            RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    args = {
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "a_speckle" : DataPair.DataTypeValue(ctypes.c_size_t, a_speckle),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_despeckle, args)


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


# TODO: clean up
class RayData:
    def __init__(self, masked, a_speckle, boundary_mask, parallel):
        self.a_speckle = a_speckle
        self.boundary_mask = boundary_mask

        self.parallel = parallel

        self.missing = masked.fill_value
        self.mask_list = masked.mask.tolist()
        self.data_list = masked.tolist(self.missing)

        # if either data_list or mask_list are 1D lists, cast them to be 2D lists
        # essentially, from: 1 list -> 1 list containing 1 list
        if (not any(isinstance(el, list) for el in self.data_list)):
            self.data_list = [self.data_list]
        if (not any(isinstance(el, list) for el in self.mask_list)):
            self.mask_list = [self.mask_list]

        self.output_data = self.data_list
        self.output_mask = self.mask_list 
        

    def despeckle_rays(self, start, end):
        for ray_num in range(start, end):
            self.despeckle_single_ray(ray_num)


    def despeckle_single_ray(self, i):
        input_data = self.data_list[i]
        input_mask = self.mask_list[i]

        # and run despeckle on each individual ray
        despec = despeckle(input_data, self.missing, self.a_speckle, boundary_mask=self.boundary_mask)
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
        chunk_size = math.ceil(len(self.data_list) / psutil.cpu_count(logical = False))

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
