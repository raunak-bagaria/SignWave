import numpy as np

# Define np.object if it does not exist
if not hasattr(np, 'object'):
    np.object = object

# Define np.bool if it does not exist
if not hasattr(np, 'bool'):
    np.bool = bool

# Check for NumPy version and define np.int if it does not exist
import numpy
if numpy.__version__ < '1.20.0':
    # For older versions, np.int is available
    if not hasattr(np, 'int'):
        np.int = np.int64  # or np.int32 depending on your needs
else:
    # For newer versions, np.int has been removed
    if not hasattr(np, 'int'):
        np.int = int  # Use built-in int type

# Define np.typeDict if it does not exist
if not hasattr(np, 'typeDict'):
    np.typeDict = {
        'bool': np.bool_,
        'int': np.int,
        'float': np.float_,
        'complex': np.complex_,
        'str': np.str_,
        'object': np.object_,
        'int8': np.int8,   
        'int16': np.int16, 
        'int32': np.int32, 
        'int64': np.int64, 
        'uint8': np.uint8, 
        'uint16': np.uint16,
        'uint32': np.uint32,
        'uint64': np.uint64,
        'short': np.int16,
        'ushort': np.uint16,
        'intc': np.intc,
        'uintc': np.uintc,
        'longlong': np.longlong,
        'ulonglong': np.ulonglong,
        'single': np.float32,
        'double': np.float64,
        'longdouble': np.float64,  # Use np.float64 if np.float128 is not available
        'csingle': np.complex64,
        'cdouble': np.complex128,
        'clongdouble': np.complex128  # Add this line
    }

# Define np.cdouble if it does not exist
if not hasattr(np, 'cdouble'):
    np.cdouble = np.complex128

# Define np.clongdouble if it does not exist
if not hasattr(np, 'clongdouble'):
    np.clongdouble = np.complex128  # Fallback to np.complex128
