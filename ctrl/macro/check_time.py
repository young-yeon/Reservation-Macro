"그냥 로컬타임 되자마자 5ms마다 총 40회정도 실행시키면 될 듯"
import time
import schedule

class CheckTime:
    "schedule? 모듈 이용"

    def set_time(self, t):
        def _job():
            for _ in range(40):
                self.job()
                time.sleep(0.1)

        schedule.every().day.at(t).do(_job)
        while True:
            schedule.run_pending()
            time.sleep(0.5)
    
    def job(self):
        pass

if __name__ == '__main__':
    test = CheckTime()
    test.job = lambda: print(1)
    test.set_time("17:36:59")