from threading import Thread

def f1(n):
    for i in range(n):
        print(f"FFFFFFFFF {i}")

def f2(n):
    for i in range(n):
        print(f"SSSSSS {i}")

if __name__=="__main__" :
    t1 = Thread(target=f1,args=(50,))
    t2 = Thread(target=f2,args=(50,))

    t1.start()
    t2.start()
