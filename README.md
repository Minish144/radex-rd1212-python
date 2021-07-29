# radex-rd1212

## Turn on bluetooth
```bash
$ bluetoothctl

[bluetooth] power on
```

## Installing dependencies
```bash
$ python3 -m venv env

$ source env/bin/activate

$ pip install -r requirements.txt
```

## Setting MAC address and auth key
set `MAC` in `.env` file according to example in `.env.example`
```
MAC=AA:AA:AA:AA:AA:AA
```

## Running
```bash
python3 main.py
```