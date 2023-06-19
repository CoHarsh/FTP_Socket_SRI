import matplotlib.pyplot as plt
import numpy as np

#download_timedata.csv
# size,time

down_data = np.genfromtxt('./plot_data/download_timedata.csv', delimiter=',', names=['size', 'time'])
plt.plot(down_data['size'], down_data['time'], 'ro')
plt.xlabel('Data size (bytes)')
plt.ylabel('Time (microseconds)')
plt.title('Download time vs data size')
plt.savefig('./plot_data/download_time.png')
# plt.show()

#upload_timedata.csv
upload_data = np.genfromtxt('./plot_data/upload_timedata.csv', delimiter=',', names=['size', 'time'])
plt.plot(upload_data['size'], upload_data['time'], 'ro')
plt.xlabel('Data size (bytes)')
plt.ylabel('Time (microseconds)')
plt.title('Upload time vs data size')
plt.savefig('./plot_data/upload_time.png')
# plt.show()

#list_timedata.csv
list_data = np.genfromtxt('./plot_data/list_timedata.csv', delimiter=',', names=['size', 'time'])
plt.plot(list_data['size'], list_data['time'], 'ro')
plt.xlabel('Number of files')
plt.ylabel('Time (microseconds)')
plt.title('List time vs number of files')
plt.savefig('./plot_data/list_time.png')
# plt.show()

