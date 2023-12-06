import time
from threading import Thread
from multiprocessing import Process
import multiprocessing

def factorize(*number):
    rlst = [] 
    for i in list(*number):
        j, lst = 2, [1]
        while j <= i-1:
            if (i % j) == 0:
                lst.append(j)
            j += 1
        lst.append(i)
        rlst.append(lst)
        print(f"for [{i}]: {lst}")
    return rlst


def execute(num):
    factorize(num) 


def execute_th(num):
    threads = [Thread(target = factorize, args=([num[i]],)) for i in range(0, len(num))]
    for thread in threads: 
        thread.start()
    for thread in threads: 
        thread.join()


def execute_pr(num):
    proces = [Process(target = factorize, args=([num[i]],)) for i in range(0, len(num))]
    for proc in proces: 
        proc.start()
    for proc in proces: 
        proc.join()
    for proc in proces: 
        print(proc.exitcode, end=' ')
    print()


if __name__ == '__main__': 

    print("cpu count: ", multiprocessing.cpu_count())  # 4

    num = [128, 255, 99999, 10651060]   # direct order
    numr = [10651060, 99999, 255, 128]  # reverse order
    # num = [128, 255, 99999, 10651060, 3871, 888897, 77777777]  # direct order
    # numr = [77777777, 10651060, 888897, 99999, 3871, 255, 128] # reverse order

    print("\nsynchronous & direct order - num:")
    print(f">> factorize: Input numbers = {num}")
    start = time.time() 
    execute(num)
    end = time.time()
    print(f">> General time execute(): {end - start}")   
    print("\nsynchronous & reverse order - numr:")
    print(f">> factorize: Input numbers = {numr}")
    start = time.time() 
    execute(numr)
    end = time.time()
    print(f">> General time execute(): {end - start}")   

    print("\nthreads & direct order - num:")
    print(f">> factorize threads: Input numbers = {num}")
    start = time.time()
    execute_th(num)
    end = time.time()
    print(f">> General time execute_thread(): {end - start}")  
    print("threads & reverse order - numr:")
    print(f">> factorize threads: Input numbers = {numr}")
    start = time.time()
    execute_th(numr)
    end = time.time()
    print(f">> General time execute_thread(): {end - start}") 

    print("\nprocess & direct order - num:")
    print(f">> factorize process: Input numbers = {num}")
    start = time.time()
    execute_pr(num)
    end = time.time()
    print(f">> General time execute_process(): {end - start}")  
    print("\nprocess & reverse order - numr:")
    print(f">> factorize process: Input numbers = {numr}")
    start = time.time()
    execute_pr(numr)
    end = time.time()
    print(f">> General time execute_process(): {end - start}")  

