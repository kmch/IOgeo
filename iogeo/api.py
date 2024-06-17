from autologging import logged, traced
from iogeo.base import *
import os

@traced
@logged
def read(file_path, **kwargs):
  _, ext = os.path.splitext(file_path)
  ext = ext[1:] # remove the dot
  if ext == 'csv':
    fun = read_csv
  elif ext == 'json':
    fun = read_json
  elif ext == 'mmp':
    fun = read_mmp
  elif ext == 'nc' or ext == 'netcdf':
    fun = read_netcdf
  elif ext == 'shp':
    fun = read_shp
  elif ext == 'tif':
    fun = read_tif
  elif ext == 'xlsx' or ext == 'xls':
    fun = read_xlsx
  else:
    raise ValueError('Unknown ext: %s' % ext)
  return fun(file_path, **kwargs)

@traced
@logged
def save(file_path, data, **kwargs):
  _, ext = os.path.splitext(file_path)
  ext = ext[1:] # remove the dot
  save._log.debug('Extension: %s' % ext)
  if ext == 'json':
    fun = save_json
  elif ext == 'mmp':
    fun = save_mmp
  else:
    raise ValueError('Unknown ext: %s' % ext)
    
  return fun(file_path, data, **kwargs)
