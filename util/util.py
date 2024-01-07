# 获取图片验证码并转换为数字
import pickle
import random
import string
import time
from PIL import Image
import os

from pytesseract import pytesseract
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def get_total(driver, id):
    # 获取列表数据总数
    # ！！！
    # 定位包含总数据条数信息的元素
    total_records_element = driver.find_element(By.CSS_SELECTOR, id)

    # 获取元素文本信息
    if total_records_element:
        total_records_text = total_records_element.text
        # 从文本中解析出数字
        # 格式为：’1-10 共 15 条‘，需要获取其中的15
        total_records = int(total_records_text.split('共')[-1].split('条')[0].strip())
        return total_records
        print("新增前总数据条数：", total_records)
    else:
        print("未获取到总数据提条数")
        return False

# 调用语句：total=get_total(self.login.driver,'.ant-pagination-total-text')
#  .ant-pagination-total-text (定位的元素)

# 获取验证码
def get_code(driver, id):
    t = time.time()
    path = os.path.dirname(os.path.dirname(__file__)) + '\\screenshots'
    picture_name1 = path + '\\' + str(t) + '.png'
    WebDriverWait(driver, 10, 0.5).until(
        lambda el: driver.find_element(By.XPATH, id))
    driver.find_element(By.XPATH, id).screenshot(picture_name1)
    imagel = Image.open(picture_name1)
    str1 = pytesseract.image_to_string(imagel)
    code = int(str1)
    return code


# 随机生成字符串
def gen_random_str():
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return rand_str


# 保存cookie
def save_coolie(driver, path):
    with open(path, 'wb') as filehandler:
        cookies = driver.get_cookies()
        print(cookies)
        pickle.dump(cookies, filehandler)


# 加载cookie
def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
