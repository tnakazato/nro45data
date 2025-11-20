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
