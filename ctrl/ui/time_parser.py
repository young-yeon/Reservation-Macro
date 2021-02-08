"예약 가능 시간 조회"
from bs4 import BeautifulSoup


def parser(source):
    "시간만 파싱해서 리스트로 제공하자!"
    soup = BeautifulSoup(source, 'html.parser')
    table = soup.select(
        '#ctl00_ContentPlaceHolder1_UpdPandel > div > div.cnt-right > div > table > tbody > tr')
    data = list()
    for tr in table:
        line = tr.select('td')
        line = [x.get_text() for x in line[:4]] + [line[4].find('a')['href']]
        data.append(["%s\t|\t%s\t|\t%s\t|\t%s" %
                     (line[0], line[1], line[2], line[3]), line[4][11:]])
    return data
