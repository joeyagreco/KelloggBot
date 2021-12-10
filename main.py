from req import *
from threading import Thread

def create_application():
    application = JobApp()
    application.apply()

def mainloop():
    t1 = Thread(target=create_application)
    t2 = Thread(target=create_application)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    i = 0
    while (i < 10000):
        mainloop()
        i += 1
