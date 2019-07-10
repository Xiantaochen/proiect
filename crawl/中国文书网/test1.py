import requests

from lxml import etree

sess = requests.session()

a = sess.get('http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=d0189691-5575-48d5-9506-aa8400a346ce')



Etree = etree.HTML(a)

b = Etree.xpath("/html/body/div[10]/text()")

print(b)