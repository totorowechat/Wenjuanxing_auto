# import requests
# from bs4 import BeautifulSoup
# import re

# rsp = requests.get('https://www.wjx.cn/m/23642541.aspx#')
# soup = BeautifulSoup(rsp.text, 'lxml')
# lists = soup.find_all(id=re.compile(r'div\d'))
# for li in lists:
#     print(li.find(class_='field-label').text)

# def test(x):
#     return{
#         '1': lambda x: print(x),
#         '2': lambda x: print('2')
#     }[x]('hellp')

# test('2')

lambda_list = lambda n: lambda_list(n-1) + (lambda x: x * (n-1),) if n else () 
fs = lambda_list(2)
print(fs[1](5))  # 15)

# if ('3' in ['3', '4', '5']):
#     print('true')
# else:
#     print('false')

# def lambda_list(n):
#     return lambda_list(n-1) + (lambda x: x* (n-1),) if n else ()


# fs = lambda_list(10)
# print(fs[3](5))  # 15)

