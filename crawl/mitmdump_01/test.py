from appium import webdriver

cap = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.tencent.mobileqq",
    "appActivity": "com.tencent.mobileqq.activity.SplashActivity",
    "noReset" :True
}

driver = webdriver.Remote('http://localhost:4723/wd/hub',cap)