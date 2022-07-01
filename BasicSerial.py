import time
from pySerialTransfer import pySerialTransfer as txfer

class struct(object):
    accX = 0
    accY = 0
    accZ = 0
    gyroX = 0
    gyroY = 0
    gyroZ = 0
    pressure = 0
    batteryVolt = 0
    batteryAmp = 0
    waterTemp = 0
    internalTemp = 0

class struct1(object):
    buttons = 100
    leftTrigger = 0
    rightTrigger = 0
    leftThumbX = 0
    leftThumbY = 0
    rightThumbX = 0
    rightThumbY = 0



if __name__ == '__main__':
    try:
        rovDataTx = struct1
        rovDataRx = struct
        link = txfer.SerialTransfer('/dev/cu.usbmodem14101')
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        
        while True:
            sendSize = 0
            sendSize = link.tx_obj(rovDataTx.buttons, start_pos=sendSize) 
            sendSize = link.tx_obj(rovDataTx.leftTrigger, start_pos=sendSize)
            sendSize = link.tx_obj(rovDataTx.rightTrigger, start_pos=sendSize)
            sendSize = link.tx_obj(rovDataTx.rightTrigger, start_pos=sendSize)
            sendSize = link.tx_obj(rovDataTx.leftThumbX, start_pos=sendSize)
            sendSize = link.tx_obj(rovDataTx.leftThumbY, start_pos=sendSize)
            sendSize = link.tx_obj(rovDataTx.rightThumbX, start_pos=sendSize)
            sendSize = link.tx_obj(rovDataTx.rightThumbY, start_pos=sendSize)

            link.send(sendSize)
            ###################################################################
            # Wait for a response and report any errors while receiving packets
            ###################################################################
            while not link.available():
                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))
            
            recSize = 0
            rovDataRx.accX = link.rx_obj(obj_type=type(rovDataRx.accX),obj_byte_size= sendSize, start_pos=recSize)
            rovDataRx.accY = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 4)
            rovDataRx.accZ = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 8)
            rovDataRx.gyroX = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 12)
            rovDataRx.gyroY = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 16)
            rovDataRx.gyroZ = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 20)
            rovDataRx.pressure = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 24)
            rovDataRx.batteryVolt = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 28)
            rovDataRx.batteryAmp = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 32)
            rovDataRx.waterTemp = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 36)
            rovDataRx.internalTemp = link.rx_obj(obj_type=type(rovDataRx.accY),obj_byte_size= sendSize, start_pos=recSize + 40)

            ###################################################################
            # Display the received data
            ###################################################################
           
            print(rovDataRx.accX)
    
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass