import threading
from math import sqrt

#get the square root of every number from 1-N (read in N) break it into threads and return the sum of square roots
results = []
def allocate(threads, n):
    inactive = threads
    active = []
    for i in range(1, n):
        if inactive >= 1:
            print("")
            active.append(threading.Thread(target=sqrt_func,args=(i)))
            inactive -= 1

        for j in range(len(active)):
            if active[j].is_alive():
                active[j].join()
                print("print")

    print(results)

            

def sqrt_func(x):
    
    results.append(sqrt(x))

allocate(8, 900)