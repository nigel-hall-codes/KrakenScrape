import krakenAPItests
import schedule
import time

schedule.every(10).seconds.do(lambda: krakenAPItests.download_depth_chart(["ETHUSD"]))

while True:
    schedule.run_pending()
    time.sleep(1)