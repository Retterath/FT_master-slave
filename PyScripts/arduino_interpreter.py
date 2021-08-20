import serial
import time
import os
import sys
import json

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
cached_results = {}

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
        curr_input = str(slave_input)[0:len(str(slave_input)) - 2]
        curr_addr = str(hex(mem_block))

        print(curr_addr + ': ' + curr_input)
        cached_results[curr_addr] = curr_input

        #ser.write(b"DM_RCV")
        slave_input = ser.readline()
        mem_block += 1

    json_results = json.dumps(cached_results, indent = 4)

    # Some method for sending the JSON to the daemon...

    print('[#] Dumping complete, awaiting for new transfer...')

