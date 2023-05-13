import matplotlib.pyplot as plt

file_name = 'server.csv'

# fetch the data from the csv which has three columns filesize time_elapsed throughput
def fetch_data(file_name) :
    file = open(file_name, 'r')
    file_size = []
    time_elapsed = []
    throughput = []
    for line in file :
        line = line.strip()
        line = line.split(',')
        file_size.append(int(line[0]))
        time_elapsed.append(float(line[1]))
        throughput.append(float(line[2]))
    file.close()
    return file_size, time_elapsed, throughput

# plot the graph
def plot_graph(file_size, time_elapsed, throughput) :
    plt.figure(1)
    plt.subplot(211)
    plt.plot(file_size, time_elapsed, 'ro')
    plt.xlabel('file size')
    plt.ylabel('time elapsed')
    plt.subplot(212)
    plt.plot(file_size, throughput, 'bo')
    plt.xlabel('file size')
    plt.ylabel('throughput')
    plt.show()

    
    return

# handle main function
if __name__ == '__main__' :
    file_size, time_elapsed, throughput = fetch_data(file_name)
    plot_graph(file_size, time_elapsed, throughput)

