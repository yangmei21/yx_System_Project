from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import pytest


class TestAdminLogin(object):
    def setup_class(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://202.111.177.155:8081/manager/static/ng-ant-admin/index.html#/login/login-form')
        self.driver.maximize_window()
        print('类setup')

    # 管理员正确登录
    @pytest.mark.dependency(name='admin_login')
    def test_admin_login_right(self):
        """
        这是管理员登录用例
        :return:
        """
        username = 'admin'
        pwd = '123456'
        excpetitle = '工作台'

        user = self.driver.find_elements(By.CSS_SELECTOR, 'input[formcontrolname="userName"]')
        user[0].send_keys(username)
        pw = self.driver.find_elements(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        pw[0].send_keys(pwd)
        bt = self.driver.find_element(By.CSS_SELECTOR, 'button.ant-btn-primary')
        bt.click()

        sleep(2)
        assert self.driver.title == excpetitle
        # self.assertEqual(self.driver.title, excpetitle)

    # def teardowm_class(self):
    #     self.driver.quit()
    #     print('类teardowm')

    # def teardown_class(self):
    #     self.driver.quit()
    #     print('类的teardown')


if __name__ == '__main__':
    pytest.man()
