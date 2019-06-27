import requests
from lxml import etree
from fontTools.ttLib import TTFont
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
}

def get_font_face(font_url):
    font_content = requests.get(font_url, headers=headers).content
    with open('douyin_lx.woff', 'wb') as f:
        f.write(font_content)

    font1 = TTFont('douyin_lx.woff')
    font1.saveXML('douyin_lx.xml')

    print(font1.getBestCmap())
    pass

def handel_decode(input_data):
    search_douyin_str = re.compile(r"抖音ID：")

    #抖音web分享数字破解列表
    regex_list = [
        {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
        {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
        {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
        {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
        {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
        {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
        {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
        {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
        {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
        {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9}
    ]
    for i1 in regex_list:
        for i2 in i1['name']:
            input_data = re.sub(i2, str(i1['value']),input_data)
    #构造HTML结结构
    share_web_html = etree.HTML(input_data)
    user_info = {}
    user_info['nickname'] = share_web_html.xpath('//p[@class="nickname"]/text()')[0]
    douyin_id1 = share_web_html.xpath('//p[@class="shortid"]/text()')[0].replace(" ","")
    douyin_id2 = share_web_html.xpath('//p[@class="shortid"]/i/text()')
    user_info['douyin_id'] = re.sub(search_douyin_str,"", douyin_id1 +  ''.join(douyin_id2))
    user_info['job'] = share_web_html.xpath('//span[@class="info"]/text()')[0].strip()
    user_info['describe'] = share_web_html.xpath('//p[@class = "signature"]/text()')[0]
    user_info['follow'] = share_web_html.xpath('//p[@class = "follow-info"]/span[1]//i/text()')[0]
    fans ="".join(share_web_html.xpath('//p[@class = "follow-info"]/span[2]//i/text()'))
    danwei1 = share_web_html.xpath('//p[@class = "follow-info"]/span[2]/span[@class="num"]/text()')[-1]
    if danwei1.strip() == "w":
        user_info['fans'] = str(int(fans)/10) + "w"

    like = "".join(share_web_html.xpath('//p[@class = "follow-info"]/span[3]//i/text()'))
    danwei2 = share_web_html.xpath('//p[@class = "follow-info"]/span[3]/span[@class="num"]/text()')[-1]
    if danwei2.strip() == "w":
        user_info['favor'] = str(int(fans)/10) + "w"
    print(user_info)


def handle_douyin_web_share():
    share_web_url = 'https://www.douyin.com/share/user/61002725169'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }
    #请求的文本数据
    share_web_response = requests.get(url=share_web_url, headers = headers)
    #就行破解
    handel_decode(share_web_response.text)



handle_douyin_web_share()