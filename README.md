# nro45data

IO utility module to read Position-Switch (PSW) data of Nobeyama 45m telescope.

## Installation

```
pip install .
```

## Usage

`nqm2fits` converts NRO 45m PSW data (.nqm) to FITS.

```python
import nro45data.psw as psw
psw.nqm2fits('mydata.nqm', 'mydata.fits')
```
