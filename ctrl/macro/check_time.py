"구한 시간차에서 50ms전에 미리 실행!"
import threading


def check_time(sec, func, interval=0.05):
    "n초 기다리고 실행!"
    threading.Timer(sec-interval, func).start()
