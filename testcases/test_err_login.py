from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pytest


class TesterrUserLogin(object):

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://202.111.177.155:8081/manager/static/ng-ant-admin/index.html#/login/login-form')
        self.driver.maximize_window()

    login_data = [
        ('admin1', '123456', '登录失败，用户名密码错误或该账号已被禁用！'),
        ('admin', '12121212', '登录失败，用户名密码错误或该账号已被禁用！')
    ]

    @pytest.mark.parametrize('username,pwd,excepted', login_data)
    def test_uesr_err_login(self, username, pwd, excepted):
        '''
        验证登录错误用例
        :param username:
        :param pwd:
        :param excepted:
        :return:
        '''
        user = self.driver.find_elements(By.CSS_SELECTOR, 'input[formcontrolname="userName"]')
        user[0].clear()
        user[0].send_keys(username)
        pw = self.driver.find_elements(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        pw[0].clear()
        pw[0].send_keys(pwd)
        bt = self.driver.find_element(By.CSS_SELECTOR, 'button.ant-btn-primary')
        bt.click()

        loc = (By.XPATH, '//*[@id="cdk-overlay-0"]/nz-message-container/div/nz-message/div/div/div/span[2]')
        WebDriverWait(self.driver, 20, 0.5).until(EC.visibility_of_element_located(loc))
        msg = self.driver.find_element(*loc).text
        print(msg)
        assert msg == excepted
        sleep(2)

    def wrong_test_empty_userlogin(self):
        user = self.driver.find_elements(By.CSS_SELECTOR, 'input[formcontrolname="userName"]')
        user[0].clear()
        pw = self.driver.find_elements(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        pw[0].clear()
        bt = self.driver.find_element(By.CSS_SELECTOR, 'button.ant-btn-primary')
        bt.click()
        message1=self.driver.find_element(By.CLASS_NAME,'ng-tns-c58-105 ant-form-item-control ant-col ng-star-inserted')
        assert message1.text=='账号名'

    def teardown_class(self):
        self.driver.quit()


if __name__ == '__main__':
    pytest.main(['test_err_login.py'])
