# Rigol Automation

This project aims to control Rigol products (though right now, I only have the DP832)

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

## Running Tests

In the root directory, run

```shell
python -m pytest
```
