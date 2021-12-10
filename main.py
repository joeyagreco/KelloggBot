from req import *
from threading import Thread
import sys

def create_application():
    application = JobApp()
    city, gender = application.apply()
    num = log_application_num(city, gender)
    print(city, gender, num)

def mainloop():
    try:
        t1 = Thread(target=create_application)
        t2 = Thread(target=create_application)
        t1.daemon = True
        t2.daemon = True
        t1.start()
        time.sleep(1.0)
        t2.start()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        sys.exit()

def log_application_num(city, gender):
    with open('executions.log', 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        try:
            num = int(lines[-1].split(',')[-1])
        except Exception as e:
            print(e)
            num = 0
        num += 1
        file.writelines(city + ',' + gender + ',' + str(num) + '\n')
        file.close()
        return num
        


if __name__ == "__main__":
    i = 0
    while (i < 10000):
        mainloop()
        i += 1
        time.sleep(3.0)
