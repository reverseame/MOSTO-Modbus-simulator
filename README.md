# MODBUS SIMULATOR TOOL - MOST  

[![License](http://img.shields.io/:license-GPLv2+-green.svg)](http://www.gnu.org/licenses/gpl-2.0.html)

MOST is a simulator of SCADA networks based in ModbusTCP communications. The simulator involves both the master and the 
slave appliances of a ModbusTCP communication where most common features of an SCADA system can be easily configured.

## Environment configuration

MOST is python based framework that have some dependencies. To ease starting configuration, a conda environment has been
exported to a yml file. This file can be easily install just typing:

```
$ conda env create -f environment.yml
```

## How to use MOST

The master and the slaves are completely disengaged from each other. To run the master simulator just run:

```
$ python ~/ModbusMaster/master.py
```

On the same way, to run the slave:

```
$ python ~/ModbusSlave/slave.py
```
