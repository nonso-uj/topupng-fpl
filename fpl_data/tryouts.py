import schedule
import time

def job():
    print('running...')


schedule.every(30).seconds.do(job)

x=0
while True:
    schedule.run_pending()
    time.sleep(31)
    x += 1
    print(x)
    if x == 11:
        break