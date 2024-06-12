import schedule
import time
from crawl import Crawl
from extract import Extract
from store import Store

def job():
    crawl = Crawl()
    all_text = crawl.get_all_info_async()

    extract = Extract()
    info = extract.extract_info(all_text)
    print(info)
    print('获得的数据总量是:{}'.format(len(info)))

    store = Store(info)
    store.mode_excel('热搜数据.xlsx')
    store.mode_mysql('HotSearch','hot_search')

# 每隔一个小时运行一次
schedule.every(1).hours.do(job)

# 初次运行
job()

while True:
    schedule.run_pending()
    time.sleep(1)
