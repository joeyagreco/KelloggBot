from req import *
import sys
import multiprocessing

def create_application():
    application = JobApp()
    city, gender, first_name, last_name, email = application.apply()
    num = log_application_num(city, gender, first_name, last_name, email)
    print(city, gender, first_name, last_name, email, num)

def mainloop():
    process_count = 4
    processes = []
    for i in range(process_count):
        process = multiprocessing.Process(target=create_application)
        process.daemon = True
        processes.append(process)
    try:
        for j in processes:
            j.start()
        for j in processes:
            j.join()
    except KeyboardInterrupt:
        for j in processes:
            j.terminate()
            j.join()
        sys.exit()

def log_application_num(*args):
    with open('executions.log', 'a+') as file:
        file.seek(0)
        lines = file.readlines()
        try:
            num = int(lines[-1].split(',')[-1])
        except Exception as e:
            print(e)
            num = 0
        num += 1
        line_to_write = str()
        for arg in args:
            line_to_write += arg + ','
        line_to_write += str(num) + '\n'
        file.writelines(line_to_write)
        file.close()
        return num
        


if __name__ == "__main__":
    i = 0
    while (i < 10000):
        mainloop()
        i += 1
        time.sleep(3.0)
