import schedule
import time

def job():
    print('running...')

def second():
    print('run second...')


schedule.every(5).seconds.do(job)
schedule.every(6).seconds.do(second)

x=0
while True:
    schedule.run_pending()
    time.sleep(6)
    x += 1
    print(x)
    if x == 11:
        break