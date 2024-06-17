from autologging import logged, traced
import numpy as np
import xarray as xr

@traced
@logged
def a2da(array:np.ndarray, extent:list) -> xr.DataArray:
  nx, ny = array.shape
  x1, x2, y1, y2 = extent
  x = np.linspace(x1, x2, nx)
  y = np.linspace(y1, y2, ny)
  return xr.DataArray(data=array, dims=['x','y'], coords={'x': x, 'y': y})


