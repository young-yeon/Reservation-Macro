"""
시간 동기화
그런데 문제는 패킷에 나오는 서버 시간이 초단위로 표시됨
따라서 초가 바뀔때까지 연속으로 패킷을 요청해서 바뀌는 타이밍을 0ms로 가정하고
매크로를 동작시킬것
"""
import urllib.request
import urllib.error
import datetime
import time


def time_sync(target):
    """목표 시간이랑 서버 시간 차이 구해서 적당한 기다릴 시간 반환!
    ['연(yyyy)', '월(MM)', '일(dd)', '시(hh)', '분(mm)', '초(ss)']"""

    def server_time():
        "패킷에서 서버 시간 확인(문제는 초단위임..)"
        date = urllib.request.urlopen(
            'https://www.namyeoju.co.kr/').headers['Date']
        server_sec = int(time.mktime(
            time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z'))) + 32400
        return server_sec

    year, month, day, hour, minute, second = target
    target_datetime = datetime.datetime(year, month, day, hour, minute, second)
    target_delta = time.mktime(target_datetime.timetuple())
    tmp = server_time()
    server_now = server_time()
    while tmp == server_now:
        server_now = server_time()
    return target_delta - server_now
    