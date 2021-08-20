import serial
import time
import os
import sys

print('#########################################################################')
print('#################### FT Arduino Sensor Interpreter ######################')
print('#########################################################################')

if len(sys.argv) != 3:
    print('[!] Unsufficient arguments!')
    print('Usage: ./arduino_interpreter.py [communication port] [baud rate]')
    sys.exit()

comm_port = sys.argv[1]
baud_rate = int(sys.argv[2])

print('[#] Trying to listen on port ' + comm_port)

ser = None

while ser is None:
    try:
        ser = serial.Serial(comm_port, baud_rate, timeout=None)
    except:
        print('[!] No connection found, retrying...')


print('[#] Opened Serial terminal on port ' + str(comm_port) + ' at ' + str(baud_rate) + ' baud rate!')
print('[#] Waiting for transfer...')

while ser.isOpen():
    slave_input = ser.readline()
    print(slave_input)
    if slave_input != b"DM_RDY\r\n":
        print('[!] Didn\'t receive correct ready message at Serial, skipping...')
        continue
    print('[#] Acknowledging transfer request at Serial...')
    ser.write(b"DM_ACK")
    print('[#] Requesting EEPROM dump...')
    slave_input = ser.readline()

    mem_block = 1

    while slave_input != b'DM_END\r\n':
        print(str(hex(mem_block)) + ': ' + str(slave_input))
        #ser.write(b"DM_RCV")
        slave_input = ser.readline()
        mem_block += 1
    print('[#] Dumping complete, closing Serial connection...')

    ser.close()