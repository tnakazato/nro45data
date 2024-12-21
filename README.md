# nro45data

IO utility module to read Position-Switch (PSW) data of Nobeyama 45m telescope.

## Installation

```
pip install .
```

## Usage

- Load NRO 45m PSW data as `astropy.io.fits.hdu.hdulist.HDUList` object.
    ```
    import nro45data.reader as reader
    hdulist = reader.read('nro-psw.nqm')
    ```