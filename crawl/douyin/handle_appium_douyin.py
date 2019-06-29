from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
cap = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.ss.android.ugc.aweme",
    "appActivity": "com.ss.android.ugc.aweme.activity.SplashActivity",
    "noResrt" : True,
    "unicodeKeyboard":True,
    "resetKeyboard":True
}

driver = webdriver.Remote("http://localhost:4723/wd/hub", cap)

#获取尺寸的函数
def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return x , y

#定位搜索框
try:
    if WebDriverWait(driver,10).until(lambda x:x.find_element_by_xpath('com.ss.android.ugc.aweme:id/aci')):
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/aci').click()
except:
    pass

#定位搜索框
try:
    if WebDriverWait(driver,10).until(lambda x:x.find_element_by_xpath('//android.widget.EditText[@resource_id="com.ss.android.ugc.aweme:id/a5q"]')):
        driver.find_element_by_xpath('//android.widget.EditText[@resource_id="com.ss.android.ugc.aweme:id/a5q"]').click()
        driver.find_element_by_xpath(
            '//android.widget.EditText[@resource_id="com.ss.android.ugc.aweme:id/a5q"]').send_keys("61002725169")
        while driver.find_element_by_xpath(
            '//android.widget.EditText[@resource_id="com.ss.android.ugc.aweme:id/a5q"]').text != "61002725169":
            driver.find_element_by_xpath(
                '//android.widget.EditText[@resource_id="com.ss.android.ugc.aweme:id/a5q"]').send_keys("61002725169")
            time.sleep(1)

except:
    pass

#定位搜索
driver.find_element_by_xpath('//android.widget.EditText[@resource_id="com.ss.android.ugc.aweme:id/a5s"]').click()

#点击用户标签
try:
    if WebDriverWait(driver,10).until(lambda x:x.find_element_by_xpath('//android.widget.HorizontalScrollView/android.widget.TextView[3]')):
        driver.find_element_by_xpath('//android.widget.HorizontalScrollView/android.widget.TextView[3]').click()
        time.sleep(1)

except:
    pass

#点击关注
try:
    if WebDriverWait(driver,10).until(lambda x:x.find_element_by_xpath('//android.support.v7.widget.RecylcerViev[/android.widget.RelativeLayout[1]/android.widget.TextView[1]')):
        driver.find_element_by_xpath('//android.widget.HorizontalScrollView/android.widget.TextView[3]').click()
        time.sleep(1)

except:
    pass

#获取粉丝 查看是否有粉丝
try:
    if WebDriverWait(driver,10).until(lambda x:x.find_element_by_xpath('//android.widget.TextView[@class="粉丝"]')):
        driver.find_element_by_xpath('//android.widget.TextView[@class="粉丝"]').click()
        time.sleep(1)
except:
    pass

l = get_size()
x1 = int(1[0]*0.5)
y1 = int(1[1]*0.9)
y2 = int(1[1]*0.15)

while True:
    if "没有更多了" in driver.page_source:
        break
    else:
        #初始鼠标位置
        driver.swipe(x1,y1, x1, y2)
        time.sleep(0.5)