# ib-physics-ia

## Getting Started
You need the following to utilise this program:
- Python 3.8 (Other versions have not been tested)
- Poetry
- ELM327 OBD Connector

Additionaly to use from source:
- Node 16 (Other versions have not been tested)
- NPM
## Installation
To begin clone this repo into your device.
``` bash
git clone https://github.com/DJCarlosValdez/ib-physics-ia \
sh ib-physics-ia/install.sh
```

## How to Use 
Execute the following command from the directory.
``` bash
sh start.sh --obd-port="PATH_TO_COM" [--refresh_rate=0.5] [--baudrate=38400]
```

Access UI through your ip @ port 5000.

If you need to download the CSV with all the data captured you can find them in the *logs* directory. 

---
Carlos Valdez (c) 2022