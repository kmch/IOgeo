"""
Dependencies (see  the list below) are inside calls, the motivation being 
there is no need to import everything if you the user needs
only one function.

import json
import geopandas as gpd
import pandas as pd
from rioxarray import open_rasterio

"""
from autologging import logged, traced
import numpy as np
import numpy as np
import xarray as xr

@traced
@logged
def read_ascii(file_name):
    # Open the ASCII file and read header information
    with open(file_name, 'r') as f:
        header = {line.split()[0]: float(line.split()[1]) for line in [next(f) for _ in range(6)]}
    
    # Extract metadata from header
    ncols = int(header['ncols'])
    nrows = int(header['nrows'])
    xllcorner = header['xllcorner']
    yllcorner = header['yllcorner']
    cellsize = header['cellsize']
    nodata = header['NODATA_value']
    
    # Compute the coordinates for each cell
    x = xllcorner + np.arange(ncols) * cellsize
    y = yllcorner + np.arange(nrows) * cellsize
    
    # Read the data part of the file into a NumPy array
    data = np.loadtxt(file_name, skiprows=6)
    data[data == nodata] = np.nan  # Convert NODATA values to NaN
    
    # Create an xarray DataArray
    da = xr.DataArray(
        data,
        dims=['y', 'x'],
        coords={'y': y, 'x': x},
        name='topography'
    )
    
    return da
@traced
@logged
def save_ascii(file_name, da:xr.DataArray, nodata_value=-9999):
    """
    Save an xarray.DataArray to an ASCII Grid file.

    Parameters:
    - da: xarray.DataArray containing the data to save.
    - file_name: String with the path to the output ASCII Grid file.
    - nodata_value: Value to use for missing data. Defaults to -9999.
    """
    # Extract grid metadata
    ncols = da.sizes['x']
    nrows = da.sizes['y']
    xllcorner = min(da.x.values)
    yllcorner = min(da.y.values)
    cellsize = (da.x[1] - da.x[0]).values
    # Handle the case where y increases with index
    # if da.y[1] > da.y[0]:
    #   save_ascii._log.warning('y increases with index')
    #   yllcorner = da.y[-1].values - (nrows - 1) * cellsize
    
    # Prepare data
    data = da.values[0]
    data[np.isnan(data)] = nodata_value  # Replace NaN with nodata_value

    # Write header and data to file
    with open(file_name, 'w') as file:
      file.write(f"ncols         {ncols}\n")
      file.write(f"nrows         {nrows}\n")
      file.write(f"xllcorner     {xllcorner}\n")
      file.write(f"yllcorner     {yllcorner}\n")
      file.write(f"cellsize      {cellsize}\n")
      file.write(f"NODATA_value  {nodata_value}\n")
      
      for row in data:
        row_str = ' '.join(map(str, row))
        file.write(f"{row_str}\n")

@traced
@logged
def read_csv(file_name, header=0, **kwargs):
  from pandas import read_csv
  return read_csv(file_name, header=header, **kwargs)

@traced
@logged
def read_json(file_name, **kwargs):
  from json import load
  with open(file_name, 'r') as file:
    content = load(file, **kwargs)
  return content
@traced
@logged
def save_json(file_name, di: dict):
  from json import dump
  with open(file_name, 'w') as file:
    dump(di, file)


@traced
@logged
def read_mmp(file_name, shape, mmp_dtype=np.float32):
  """
  Read a memory-mapped file.

  Parameters
  ----------
  file_name : str
    The file name, including the '.mmp' extension.

  shape : tuple
    Shape of the array stored in the memory-mapped file.

  mmp_dtype : data-type, optional (default is np.float32)
    The data type to interpret the binary data in the file.

  Returns
  -------
  np.memmap
    The memory-mapped array.

  Raises
  ------
  FileNotFoundError
    If the specified file does not exist.

  """
  from numpy import memmap
  if not os.path.exists(file_name):
    raise FileNotFoundError(file_name)
  
  fA = memmap(file_name, dtype=mmp_dtype, shape=shape)
  return fA
@traced
@logged
def save_mmp(file_name, A, mmp_dtype=np.float32):
  """
  Save an array to a memory-mapped file.
  
  Parameters
  ----------
  A : array_like
    The array to be saved to the memory-mapped file.

  file_name : str
    The file name, including the '.mmp' extension.

  mmp_dtype : data-type, optional (default is np.float32)
    The data type to be used for saving the array.

  Returns
  -------
  np.memmap
    The memory-mapped array.

  """
  from numpy import memmap
  with open(file_name, 'wb') as file:
    A.tofile(file)

  fA = memmap(file_name, dtype=mmp_dtype, mode='r+', shape=A.shape)
  return fA

@traced
@logged
def read_shp(file_name, **kwargs):
  from geopandas import read_file
  return read_file(file_name, **kwargs)

@traced
@logged
def read_tif(file_name, **kwargs):
  from rioxarray import open_rasterio
  return open_rasterio(file_name, **kwargs)

@traced
@logged
def read_xlsx(file_name, header=1, **kwargs):
  from pandas import read_excel
  return read_excel(file_name, header=header, **kwargs)


@traced
@logged
def read_netcdf(file_name) -> xr.DataArray:
  return xr.open_dataset(file_name).to_array()
@traced
@logged
def save_netcdf(file_name, da:xr.DataArray):
  """
  Of course this function is just an alias of da.to_netcdf.
  But it serves as an example that it does work for our purposes,
  i.e. it can be read by `read_netcdf`.
  Examples
  --------
  import xarray as xr

  da = xr.DataArray(
    data=np.random.rand(2800, 1850).astype(np.float32),
    dims=['y', 'x'],
    coords={
        'x': np.linspace(521500, 540000, 1850),
        'y': np.linspace(179500, 151500, 2800),
    }
  )
  file_name = 'output.nc'
  da.to_netcdf(file_name)
  """
  da.to_netcdf(file_name)
