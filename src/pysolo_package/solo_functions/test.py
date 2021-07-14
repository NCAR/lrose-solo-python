from pysolo_package.utils.enums import Where

where = Where.ABOVE

if isinstance(where, Where):
    where = where.value

if not isinstance(where, int):
    raise ValueError(f"Expected integer or Where enum for 'where' parameter, received {type(where)}")