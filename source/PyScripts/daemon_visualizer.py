import sys
import os
import json
import matplotlib.pyplot as plt

def generate_intervals(val_len, offset):
    count = 0
    last_val = 0
    vals = []
    while True:
        vals.append(last_val)
        last_val += offset
        count += 1
    
    return vals

print('#########################################################################')
print('#################### FT Daemon Sensor Parser ############################')
print('#########################################################################')

if len(sys.argv) != 3:
    print('[!] Unsufficient arguments!')
    print('Usage: ./daemon_visualizer.py [result-file] [l/t/h] [record-interval]')
    sys.exit()

result_file_path = sys.argv[1]
option = sys.argv[2]
record_interval = int(sys.argv[3])

light_vals = []
temp_vals = []
hum_vals = []

if (not os.path.exists(result_file_path)):
    print('[!] Result file does not exist!')
    sys.exit()

if (option not in ('l', 't', 'h')):
    print('[!] Invalid option selected!')
    sys.exit()

result_file = open(result_file_path, "r")

json_result_data = result_file.read()

result_file.close()

parsed_data = json.loads(json_result_data)
raw_data = []

for kvp in parsed_data:
    raw_data.append(int(parsed_data[kvp]))


for i in range(0, len(raw_data), 3):
    light_vals.append(i)

for i in range(1, len(raw_data), 3):
    temp_vals.append(i)

for i in range(2, len(raw_data), 3):
    hum_vals.append(i)

selected_vals = light_vals if option == 'l' else (temp_vals if option == 't' else (hum_vals if option == 'h' else None))

x_plot_vals = generate_intervals(len(selected_vals), record_interval)

plt.plot(x_plot_vals, selected_vals)

plt.show()

# TODO: Add option to plot multiple values from sensor (humidity, light, temp) at once with different colors; see also for different line styles