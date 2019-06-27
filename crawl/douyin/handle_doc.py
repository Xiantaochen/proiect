

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome()

share_id = "88445518961"
share_url = "https://www.douyin.com/share/user/" +share_id
headers = {
"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}

dytk_search = re.compile(r"dytk: '(.*?)'")
tac_search = re.compile(r"<script>tac=(.*?)</script>")

response = requests.get(url=share_url, headers = headers)

dytk = re.search(dytk_search,response.text).group(1)
tac = "var tac="+re.search(tac_search,response.text).group(1)+";"

with open('html_head.txt','r') as f1:
    f1_read = f1.read()


with open('html_tail.txt','r') as f2:
    f2_read = f2.read().replace("&&&",share_id)
print(tac, dytk)
with open('text.html','w') as f_w:
    f_w.write(f1_read + "\n" +tac+ "\n" + f2_read)

driver.get('file://C:\\Users\涛声依旧\PycharmProjects\\WorkProject\\crawlProject\\douyin\\text.html')

signature = driver.title

driver.quit()

print(signature)

# signature = input("秘钥为：")
movie_url = "https://www.douyin.com/web/api/v2/aweme/post/?user_id="+share_id+"&count=21&max_cursor=0&aid=1128&_signature="+signature+"&dytk="+dytk

while True:
    movie_response = requests.get(url=movie_url, headers = headers)
    if json.loads(movie_response.text)['aweme_list'] == []:
        time.sleep(1)
        continue
    else:
        for item in json.loads(movie_response.text)['aweme_list']:
            video_url  = item['video']['play_addr']['url_list'][1]
            print(video_url)
            video_respose = requests.get(url= video_url, headers = headers)
            print(video_respose.content)
            with open('douyin.mp4','wb') as v:
                v.write(video_respose.content)
            break
        break

