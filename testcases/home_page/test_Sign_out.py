from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import pytest

'''
退出登录
'''


class Testquit(object):
    def setup_class(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://202.111.177.155:8081/manager/static/ng-ant-admin/index.html#/login/login-form')
        self.driver.maximize_window()
        print('类setup')

    # 登录
    def test_admin_login(self):
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
        print('\n登录成功！')
        self.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()

    def test_Sign_out(self):
        """
        这是管理员退出用例
        :return:
        """
        # 定位头像框
        sleep(2)
        el = self.driver.find_element(By.XPATH, '//*[@id="tools"]/span[3]/img')
        # 悬停鼠标并显示下拉框
        ActionChains(self.driver).move_to_element(el).perform()
        sleep(2)
        # 定位下拉框设置个人信息元素并点击进入设置信息页面
        self.driver.find_element(By.LINK_TEXT, '退出登录').click()
        sleep(2)
        url = self.driver.current_url
        print('\n退出后的连接地址：', url)
        assert url == 'http://202.111.177.155:8081/manager/static/ng-ant-admin/index.html#/login/login-form', '未退出到登录页，请检查！！'
        print('退出登录成功！！！')

    def teardown_class(self):
        self.driver.quit()
        print('关闭浏览器')


if __name__ == '__main__':
    pytest.main()
