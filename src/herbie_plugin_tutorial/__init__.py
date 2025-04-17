"""Custom model templates for Herbie.

DESCRIPTION : str
    A description of the model. Give the full name and the
    domain, if relevant. Just infor for the user.
DETAILS : dict
    Some additional details about the model. Provide links
    to web documentation. Just info for the user.
PRODUCTS : dict
    Models usually have different product types. The keys are
    used in building the GRIB2 source URL.
    ORDER MATTERS -- If product is None, then Herbie uses the first
    as default.
    *ONLY ONE IS USED (FIRST IS USED IF NOT SET)*
SOURCES : dict
    Build the URL for the GRIB2 file for different sources.
    The parameters are from arguments passed into the
    ``herbie.core.Herbie()`` class.
    ORDER MATTERS -- If priority is None, then Herbie searches the
    sources in the order given here.
    *LOOP THROUGH ALL SOURCES*
LOCALFILE : str
    The local file to save the model output. The file will be saved in
    ``save_dir/model/YYYYmmdd/localFile.grib2``
    It is sometimes necessary to add details to maintain unique
    filenames (e.g., rrfs needs to have the member number in LOCALFILE).
EXPECT_IDX_FILE : {None, "remote"}
    If None, Herbie knows not to expect an index file for this kind
    of file. (Perhaps the file is not a GRIB file.)
    If "remote", then Herbie will expect an index file on the remote
    location. This is the default value.


Optional
--------
IDX_SUFFIX : list
    Default value is ["grib.idx"], which is pretty standard.
    But for some, like RAP, the idx files are messy and could be a few
    different styles.
    self.IDX_SUFFIX = [".grb2.inv", ".inv", ".grb.inv"]
    *LOOP THROUGH ALL SUFFIXES TO FIND AN INDEX FILE*

IDX_STYLE : {'wgrib2', 'eccodes'}
    This defines how the index will be interpreted.
    - NCEP products use ``wgrib2`` to create index files.
    - ECMWF products use ``eccodes`` to create index files.

Building the file path or URL
-----------------------------
Extra arguments passed to the Herbie class are used to build the file
path or URL. The arguments are:
- model: str
    The model name. This is used to build the file path or URL.
- date: datetime
    The date of the model run. This is used to build the file path or URL.
- fxx: int
    The forecast hour. This is used to build the file path or URL.
- product: str
    The product type. This is used to build the file path or URL.

```python
Herbie(date='2025-01-01', model='hrrr_analysis', fxx=0, product='prs')
```

Any extra arguments passed to the Herbie class may also used to build
the file (e.g, member, run, domain, or anything else you want).

```python
Herbie(date='2025-01-01', model='bmw', fxx=0, member=1, domain='3a')
```
"""


class hrrr_analysis:
    """Custom template for HRRR analysis data on AWS S3."""

    def template(self):
        self.DESCRIPTION = "High-Resolution Rapid Refresh - CONUS: ANALYSIS ONLY"
        self.DETAILS = {
            "custom model template": "https://github.com/blaylockbk/herbie-plugin-tutorial",
        }
        self.PRODUCTS = {
            "sfc": "2D surface level fields; 3-km resolution",
            "prs": "3D pressure level fields; 3-km resolution",
            "nat": "Native level fields; 3-km resolution",
            "subh": "Subhourly grids; 3-km resolution",
        }
        self.SOURCES = {
            "aws": f"https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.{self.date:%Y%m%d}/conus/hrrr.t{self.date:%H}z.wrf{self.product}f00.grib2",
        }


class bwm:
    """Custom template for Brian's Model of Weather (BMW) data."""

    def template(self):
        self.DESCRIPTION = "Brian's Model of Weather"
        self.DETAILS = {
            "local": "These GRIB2 files are produced by a local of the BMW model."
        }
        self.PRODUCTS = {
            "default": "default model product",
        }
        self.SOURCES = {
            "local_main": f"/path/to/bmw/model/output/{self.model}/gribfiles/{self.date:%Y%m%d%H}/my_file.t{self.date:%H}z.f{self.fxx:02d}_{self.domain}.grib2",
        }
