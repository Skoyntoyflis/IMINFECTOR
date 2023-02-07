import time
import string
import sys
import subprocess
import numpy as np

def get_cpumem(pid):
    d = [i for i in subprocess.getoutput("ps aux").split("\n")
        if i.split()[1] == str(pid)]
    return (float(d[0].split()[2]), float(d[0].split()[5])) if d else None

if __name__ == '__main__':
    if not len(sys.argv) == 2 or not all(i in string.digits for i in sys.argv[1]):
        print("usage: %s PID" % sys.argv[0])
        exit(2)
    
    file_object = open('memory_log.txt', 'a')
    mem=[]
    file_object.write("%CPU\t%MEM\n")
    try:
        while True:
            try:
                x,y = get_cpumem(sys.argv[1])
            except TypeError:
                max = max(mem)
                file_object.write(max)
                file_object.close()
            if not x:
                print("no such process")
                exit(1)
            y = y/1024
            mem.append(y)
            # print(max(mem))
            file_object.write("%.2f\t%.2f\n" % (x,max(mem)))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print
        max = max(mem)
        file_object.write(max)
        file_object.close()
        exit(0)