# Rigol Automation

This project aims to control Rigol products (though right now, I only have the DP832)

## Install

We make use of some dependencies so install the following.

NI-VISA backend - https://pyvisa.readthedocs.io/en/latest/faq/getting_nivisa.html#faq-getting-nivisa

The library needs some additional files. If you know how to install local packages in an env, then do so - its probably the better way. 

If not, then install the following (and hope you don't have any problems lol)

`pip install -r requirements.txt`

Run the setup.py to install so that pip can see it.

```bash
python setup.py install
```

If there is an update to the repo be sure to install it again. You may need to update other projects that use this to ensure its using the latest.

## How to Use

You need to know the VISA descriptor number of your device. Within the UTILY section, you should see it.

It should look something like `USB0::0x1AB1::0x0E11::DP8C231401286::INSTR`

Alternatively you can write up some quick python code

```python
import pyvisa

rm = pyvisa.ResourceManager()
res = rm.list_resources()
print(res)

```

Create a new instance of the RigolPowerSupply()

```python
psu = RigolPowerSupply(MODEL,VISA_DES)

psu.set_levels(1,5,2) # channel 1, 5V, 2A
psu.turn_on(1) # turn on channel 1
```

Valid values for MODEL = 'dp832'
VISA_DESC is a string of the Visa Descriptor

### Create config file

Create a config file so that you can load preset values.

```json
{
  "visa_desc": "USB0::0x1AB1::0x0E11::DP8C231401286::INSTR",
  "ch3": {
    "volt": 3.6,
    "current": 3.0
  }
}
```

## Running Tests

In the root directory, run

```shell
python -m pytest
```
