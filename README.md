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

## Services, Characteristics, Descriptors
### Cable Replacement
Cable Replacement Service - `0bd51666-e7cb-469b-8e4d-2742f1ba77cc`
Cable Replacement Char. - `e7add780-b042-4876-aae1-112855353cc1`
Configuration Desc. - `00002902-0000-1000-8000-00805f9b34fb`

## Pipeline
1. Write 1 byte `0x02` to *Configuration Desc.* (i guess this asks tells device to enable sending data via bluetooth)
2. Enable indicaitions for *Cable Replacement Char.*
3. Every time you need to read data from the deviceб you have to write 14 bytes `0x12, 0x12, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00` to *Cable Replacement Char.*
4. and wait for notification from *Cable Replacement Char.*
5. Read the value you got, penultimate byte is a radiation value

**apparently you are able to request data not more than 1 time in 30 seconds**