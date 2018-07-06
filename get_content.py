import requests
from bs4 import BeautifulSoup
import time
import re
import random


# soup = BeautifulSoup(rsp.text, 'html.parser')

# print(soup.prettify())

class wenjuanxini(object):
    def __init__(self, num):
        self.base_url = 'https://www.wjx.cn/m/{}.aspx'
        self.base_submit = 'https://www.wjx.cn/joinnew/processjq.ashx?'
        self.session = requests.session()
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;',
            # 'cookie': '.ASPXANONYMOUS=weSCc8wu1AEkAAAANjE3MGMxZGItNDQ5OC00YWI3LTkxZGEtNmVkNTY5MzU5OTdlVi6pfvz50MfKv5R7T8xKFWe2LqE1; UM_distinctid=163b2116ddfbbc-048109171a2d4f-737356c-144000-163b2116de07fd; jac24389107=04539338; CNZZDATA4478442=cnzz_eid%3D1533293032-1527696898-%26ntime%3D1527730790; Hm_lvt_21be24c80829bd7a683b2c536fcf520b=1527700877,1527732232; Hm_lpvt_21be24c80829bd7a683b2c536fcf520b=1527732232',
            'origin': 'https://www.wjx.cn',
            'referer': 'https://www.wjx.cn/m/24389107.aspx',
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.curID = num # ID of the question
        self.submit_data = {}
        self.html = ''
        self.validate_text = ''
        self.rn = 0
        self.submit_host_url = 'https://www.wjx.cn/joinnew/processjq.ashx?'
        self.title_list = []

    def getHtml(self):
        response = self.session.get(self.base_url.format(self.curID))
        self.html = response.text


    def getRandNum(self):
        self.rn = re.search(r'rndnum="(\d+.?\d+?)";', self.html).group(1)
        # print('rn = ' + self.rn)


    def get_title_list(self):
        main_soup = BeautifulSoup(self.html, 'html.parser')
        title_soup_list = main_soup.findAll(class_='ui-field-contain')
        for title_soup in title_soup_list:
            title_str = title_soup.find(class_='field-label').text.strip()             #field-label
            if (title_soup['type'] == '5'):
                choice_list = [choice.string for choice in title_soup.find_all('td')]
                title_dict = {
                    'title': title_str,
                    'choice_list': choice_list,
                    'type': title_soup['type']
                }
                self.title_list.append(title_dict)
            else:
                choice_list = [choice.string for choice in title_soup.find_all(class_='label')]            #select('.label')
                title_dict = {
                    'title': title_str,
                    'choice_list': choice_list,
                    'type': title_soup['type']
                }
                self.title_list.append(title_dict)


    def get_submit_url(self, start, end):
        start_time = time.localtime(time.time() - random.randint(start, end))
        query_dict = {
            'curID': str(self.curID),                                                # 从填写页面获取的问卷curid
            'starttime': time.strftime('%Y/%m/%d %H:%M:%S', start_time),        # 模拟开始时间
            # 'source': 'directphone',
            'submittype': '1',
            'rn': str(self.rn),                            # 从填写页面获取的rn
            't': str(int(time.time()*1000)),                                   # 模拟提交时间
        }
        query_str = ''
        for key, value in query_dict.items():
            query_str += key + '=' + value + '&'
        self.submit_host_url += query_str[:-1]

    def random_choose(self):
        '''random choose the answer'''
        for title in self.title_list:
            if(title['type'] in ['3', '4', '5'] ):
                title['answer'] = random.randint(1, len(title['choice_list']))
            else:
                title['answer'] = 'test'
    
    def get_submit_data(self):
        form_data = ''
        for num in range(len(self.title_list)):
            title = self.title_list[num]
            form_data += str(num+1) + '$' + str(title['answer']) + '}'
            self.submit_data['submitdata'] = form_data[:-1]

    def get_random_ip(self):
        self.headers['X-Forwarded-For'] = (str(random.randint(1,255))+".")+(str(random.randint(1,255))+".")+(str(random.randint(1,255))+".")+str(random.randint(1,255))

    def post_quest(self):
        self.get_random_ip() #随机IP
        rsp = self.session.post(self.submit_host_url, data=self.submit_data, headers=self.headers)
        print(rsp.text)
        print(rsp.request.url)
    
    def refresh_session(self):
        self.session = requests.session()
def main():
    num = 25839037
    wjx = wenjuanxini(num)
    wjx.getHtml()
    wjx.getRandNum()
    wjx.get_submit_url(300,1000)
    wjx.get_title_list()
    wjx.random_choose()
    print(wjx.title_list)
    wjx.get_submit_data()
    print(wjx.submit_data)
    wjx.post_quest()
    wjx.refresh_session()
    print(wjx.submit_host_url)
    time.sleep(0.5)

if __name__ == '__main__':
    main()