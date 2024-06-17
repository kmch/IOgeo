from setuptools import setup, find_packages

setup(
    name='iogeo',
    version='0.0.2',
    packages=find_packages(), # organise the internal dependencies, not external 
    install_requires=[
        'autologging',
        'geopandas',
        'numpy==1.*',
        'pandas', 
        'rioxarray',
        'xarray',
    ],    
    description='Managing file I/O for Earth science.',
    long_description='Managing file I/O for Earth science: most common file formats, generic framework for adding new file formats, fast I/O with sequential access to binary files.',
    author='Kajetan Chrapkiewicz',
    author_email='k.chrapkiewicz17@imperial.ac.uk',
    url='https://github.com/kmch/iogeo',
)
