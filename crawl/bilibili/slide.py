"""参照blog：https://blog.csdn.net/qq_28654919/article/details/89923687"""
import random
import time, re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import base64


name = "18862054696"
password = "ch302811X"

class bilibili():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1440, 900)

    def visit_index(self):
        """输入账号和密码"""
        self.browser.get('https://passport.bilibili.com/login?gourl=https://space.bilibili.com')
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btn-login')))
        loginName = self.browser.find_element_by_id('login-username')
        loginName.send_keys(name)
        loginPassword = self.browser.find_element_by_id('login-passwd')
        loginPassword.send_keys(password,)
        time.sleep(2)

        # 点击登录，弹出滑块验证码
        btn = self.browser.find_element_by_xpath('//*[@id="geetest-wrap"]/ul/li[5]/a[1]')
        btn.click()
        time.sleep(5)
        WebDriverWait(self.browser, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))

        # 进入模拟拖动流程
        self.analog_drag()

    def analog_drag(self):
        # 刷新一下极验图片
        element = self.browser.find_element_by_xpath('//a[@class="geetest_refresh_1"]')
        element.click()
        time.sleep(1)
        # 保存两张图片
        self.save_img('full.jpg', 'geetest_canvas_fullbg')
        self.save_img('cut.jpg', 'geetest_canvas_bg')
        full_image = Image.open('full.jpg')
        cut_image = Image.open('cut.jpg')

        # 根据两个图片计算距离
        distance = self.get_offset_distance(cut_image, full_image)

        # 开始移动
        self.start_move(distance)

        # 如果出现error
        try:
            WebDriverWait(self.browser, 5, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider geetest_error"]')))
            print("验证失败")
            return
        except TimeoutException as e:
            pass

        # 判断是否验证成功
        try:
            WebDriverWait(self.browser, 10, 0.5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider geetest_success"]')))
        except TimeoutException:
            print("again times")
            self.analog_drag()
        else:
            print("验证成功")

    def save_img(self, img_name, class_name):
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        img = self.browser.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

        # 判断颜色是否相近

    def is_similar_color(self, x_pixel, y_pixel):
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:
                return False
        return True

        # 计算距离

    def get_offset_distance(self, cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("1.png")
                    return x

        # 开始移动

    def start_move(self, distance):
        element = self.browser.find_element_by_xpath('//div[@class="geetest_slider_button"]')

        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= element.size.get('width') / 2
        distance += 25

        # 按下鼠标左键
        ActionChains(self.browser).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.browser).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)

        ActionChains(self.browser).move_by_offset(distance, 1).perform()
        ActionChains(self.browser).release(on_element=element).perform()

if __name__ == "__main__":
    b = bilibili()
    b.visit_index()


