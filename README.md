# MOSTO-Modbus-simulator

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

`MOSTO` is a SCADA network device simulator based on ModbusTCP communications. The simulator involves both the master and slave devices of a ModbusTCP communication, where the most common features of a SCADA system can be easily configured.

## Usage

The master and the slaves are completely disengaged from each other. To run the master simulator simply run:

```
python master.py
```

Likewise, to run the slave:

```
python slave.py
```

## Authors

- Ibai Marcos Cincunegui
- Ricardo J. Rodríguez

## License

Licensed under the [GNU GPLv3](LICENSE) license.
