from iogeo.xr import Xarr
import xarray as xr

class NetCDF:
  @classmethod
  def extract(cls, x1, x2, y1, y2, fname_inp, fname_out, 
              data_array="z", pad_width=0, pad_value=0, save=True):
    """
    Extracts a subdomain from a D8 flow direction file, pads it, 
    and saves as a NetCDF file readable by xarray.
    """
    xarr = xr.open_dataset(fname_inp)[data_array].sel(
      x=slice(x1, x2), y=slice(y1, y2))
    xarr = Xarr.pad(xarr, pad_width, pad_value)
    if save:
      dataset = xr.Dataset({data_array: xarr})
      dataset.to_netcdf(fname_out, format='NETCDF4')
    return xarr
