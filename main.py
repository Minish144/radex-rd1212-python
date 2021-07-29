from bluepy.btle import Peripheral, Characteristic, Descriptor, UUID, DefaultDelegate
import time

UUID_SVC_CABLE_REPLACEMENT = UUID('0bd51666-e7cb-469b-8e4d-2742f1ba77cc')
UUID_CHAR_CABLE_REPLACEMENT = UUID('e7add780-b042-4876-aae1-112855353cc1')
UUID_DESC_CONFIGURATION = UUID('00002902-0000-1000-8000-00805f9b34fb')

MAC = '00:07:80:14:83:B6'

ENABLE_PROTOCOL = bytearray([2])

_WRITE = bytearray([18, 18, 1, 1])

class RD1212(Peripheral):
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
        print(f'[{hnd}]: {data}')

def main():
    device = RD1212(MAC)
    print('Connected!')

    # device.inspect()

    delegate = NotificationDelegate(device)
    device.setDelegate(delegate)

    data_svc = device.getServiceByUUID(UUID_SVC_CABLE_REPLACEMENT)
    
    data_char = data_svc.getCharacteristics(UUID_CHAR_CABLE_REPLACEMENT)[0]

    client_config: Descriptor = data_svc.getDescriptors(UUID_DESC_CONFIGURATION)[0]

    client_config.write(ENABLE_PROTOCOL)

    time.sleep(0.5)

    bytearr = bytearray(14)

    bytearr[0] = 18
    bytearr[1] = 18
    bytearr[2] = 1
    bytearr[3] = 1
    
    data_char.write(bytearr, True)
    device.waitForNotifications(5)

main()