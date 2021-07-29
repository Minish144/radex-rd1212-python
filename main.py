from bluepy.btle import Peripheral, Characteristic, Descriptor, Service, UUID, DefaultDelegate
import time
import os
import dotenv

dotenv.load_dotenv()

MAC = os.getenv('MAC')
if not MAC:
    raise Exception('MAC address was not found in')

UUID_SVC_CABLE_REPLACEMENT = UUID('0bd51666-e7cb-469b-8e4d-2742f1ba77cc')
UUID_CHAR_CABLE_REPLACEMENT = UUID('e7add780-b042-4876-aae1-112855353cc1')
UUID_DESC_CONFIGURATION = UUID('00002902-0000-1000-8000-00805f9b34fb')

ENABLE_PROTOCOL = bytearray([2])

REQUEST_SERIAL = b'\x12\x12\x01' + b'\x01' + b'\x00' * 10
REQUEST_DATA = b'\x12\x12\x01' + b'\x02' + b'\x00' * 10

class RD1212(Peripheral):
    '''
    RD1212 is a class which provides
    you useful methods to work with
    radex rd1212
    '''
    def __init__(self, MAC: str):
        super().__init__(MAC)
    
    def inspect(self) -> None:
        '''
        inspect prints available
        services and its characteristics
        '''
        svcs = self.getServices()
        for svc in svcs: 
            print(f'\n       {svc.uuid}       ')
            print('--------------------------------------------------')
            for ch in svc.getCharacteristics():
                print(f'[{ch.getHandle()}]', '0x'+ format(ch.getHandle(),'02X')  +'   '+str(ch.uuid) +' ' + ch.propertiesToString())
        print('\n')

    def enable_indications(self):
        '''
        enable_indications enables
        notifications
        '''
        desc = self.get_configuaration_descriptor()
        desc.write(ENABLE_PROTOCOL)
        time.sleep(2)

    def get_cable_replacement_char(self) -> Characteristic:
        svc: Service = self.getServiceByUUID(UUID_SVC_CABLE_REPLACEMENT)
        chars = svc.getCharacteristics(UUID_CHAR_CABLE_REPLACEMENT)
        if len(chars) != 0:
            return chars[0]
        else:
            raise Exception(f'failed to get cable replacement char, could not find such in {UUID_SVC_CABLE_REPLACEMENT} service')

    def get_configuaration_descriptor(self) -> Descriptor:
        '''
        get_configuaration_descriptor returns
        configuration descriptor
        '''
        svc: Service = self.getServiceByUUID(UUID_SVC_CABLE_REPLACEMENT)
        chars = svc.getDescriptors(UUID_DESC_CONFIGURATION)
        if len(chars) != 0:
            return chars[0]
        else:
            raise Exception(f'failed to get configuration descriptor, could not find such in {UUID_SVC_CABLE_REPLACEMENT} service')

    def request_data(self) -> None:
        '''
        request_data sends data 
        request which you catch and 
        handle in NotificationDelegate 
        .handleNotification method
        '''
        self.get_cable_replacement_char().write(
            val=REQUEST_DATA, 
            withResponse=True)

    def handle_radiation(self, result: bytes) -> float:
        '''
        handle_radiation returns
        radiation value
        '''
        last_byte = result[-1]
        return None if last_byte == 0 else last_byte / 100

class NotificationDelegate(DefaultDelegate):
    '''
    NotificationDelegate is a
    DefaultDelegate class with
    overridden notification handler
    '''
    def __init__(self, device: RD1212):
        super().__init__()
        self.device = device

    def handleNotification(self, hnd, data):
        '''
        handleNotification handles new notification
        '''
        print(f'[{hnd}]: {list(data)}')
        print(f'Radition: {self.device.handle_radiation(data)}')


def main():
    print('Connecting..')
    device = RD1212(MAC) # initialize connection
    print('Connected!')

    # device.inspect()

    delegate = NotificationDelegate(device)
    device.setDelegate(delegate) # set indications handler

    device.enable_indications() # request for indications
    time.sleep(1)

    while True: # request data and handle it in NotificationDelegate
        device.request_data()
        device.waitForNotifications(5)
        time.sleep(30)

if __name__ == '__main__':
    main()