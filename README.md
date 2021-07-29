# radex-rd1212

## Turn on bluetooth
```zsh
$ bluetoothctl

[bluetooth] power on
```

## Installing dependencies
```zsh
$ python3 -m venv env

$ source env/bin/activate

$ pip install -r requirements.txt
```

## Setting MAC address and auth key
set `MAC` in `.env` file according to example in `.env.example`
```zsh
MAC=AA:AA:AA:AA:AA:AA
```

## Running
```zsh
python3 main.py
```