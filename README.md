# nro45data

IO utility module to read Position-Switch (PSW) data of Nobeyama 45m telescope.

## Installation

```
git clone https://github.com/tnakazato/nro45data.git
cd nro45data
pip install .[casa6]
```

## Usage

`nqm2fits` converts NRO 45m PSW data (.nqm) to FITS.

```python
import nro45data
nro45data.nqm2fits('mydata.nqm', 'mydata.fits')
```

`nqm2ms2` converts NRO 45m PSW data (.nqm) to MS2.

```python
import nro45data
nro45data.nqm2ms2('mydata.nqm', 'mydata.ms')
```

> [!TIP]
> If you have never used CASA, you might get the error like below. If you see similar error, please do `mkdir -p ~/.casa/data` and try again.
> ```
> AutoUpdatesNotAllowed: data_update: path must exist as a directory and it must be owned by the user, path = /Users/username/.casa/data
> ```
> 
