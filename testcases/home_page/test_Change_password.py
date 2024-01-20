from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
import pytest
from testcases.test_admin_login import TestAdminLogin
from selenium.webdriver.common.keys import Keys

"""
修改密码页功能页 [因为这个没做原密码错误提示功能所以没写，后续优化在写入]
进入修改密码页-test_goto_Change_password
必填验证-test_empty_input
前后密码不一致验证-test_pwd_incon
修改成功验证-test_change_password_success
"""


class TestChangepwd(object):
    def setup_class(self):
        self.login = TestAdminLogin
        print("调用管理员登录")
        self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        sleep(1)

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_goto_Change_password(self):
        '''
        这是进入修改密码页，看情况执行
        :return:
        '''
        # 定位头像框
        el = self.login.driver.find_element(By.XPATH, '//*[@id="tools"]/span[3]/img')
        # 悬停鼠标并显示下拉框
        ActionChains(self.login.driver).move_to_element(el).perform()
        sleep(2)
        # 定位下拉框设置个人信息元素并点击进入设置信息页面
        self.login.driver.find_element(By.LINK_TEXT, '修改密码').click()
        # 最大化页面
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-3"]/nz-modal-container/div/div/button/span/div/span[1]').click()
        page_title = self.login.driver.find_element(By.XPATH,
                                                    '//*[@id="cdk-overlay-3"]/nz-modal-container/div/div/div[1]/div/div')
        assert page_title.text == '修改密码', '该页面标题不为修改密码页，请检查！！！'
        print('成功进入修改密码页！')

    def test_empty_input(self):
        expect = '必填项'
        """
        这是修改密码填写框必填验证用例--成功
        :return:
        """
        # 全部填写框为空
        btn = self.login.driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-primary ng-star-inserted"]')
        btn.click()
        sleep(2)
        oldPassword_err = self.login.driver.find_element(By.XPATH,
                                                         '//div[@class="ng-tns-c58-52 ant-form-item-explain-error"]')
        print(oldPassword_err.text)
        newPassword_err = self.login.driver.find_element(By.XPATH,
                                                         '//div[@class="ng-tns-c58-53 ant-form-item-explain-error"]')
        sureNewPassword_err = self.login.driver.find_element(By.XPATH,
                                                             '//div[@class="ng-tns-c58-54 ant-form-item-explain-error"]')
        sleep(2)
        assert newPassword_err.text == expect and sureNewPassword_err.text == expect and oldPassword_err.text == expect, '验证失败！请检查！'
        print("全内容必填项验证成功！！！")
        # 新密码为空
        self.login.driver.find_element(By.ID, 'oldPassword').send_keys('123321')
        self.login.driver.find_element(By.ID, 'sureNewPassword').send_keys('123321')
        assert newPassword_err.text, '验证失败！请检查！'
        print("单一必填项验证成功！！！")
        # 新旧密码不一致
        # 确定密码为空

    def test_pwd_incon(self):
        expect = '两次输入密码不一致'
        """
        这是密码不一致时验证
        :return:
        """
        self.login.driver.find_element(By.ID, 'oldPassword').clear()
        self.login.driver.find_element(By.ID, 'sureNewPassword').clear()
        self.login.driver.find_element(By.ID, 'oldPassword').send_keys('123321')
        self.login.driver.find_element(By.ID, 'newPassword').send_keys('123321')
        self.login.driver.find_element(By.ID, 'sureNewPassword').send_keys('652325')
        btn = self.login.driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-primary ng-star-inserted"]')
        btn.click()
        sleep(2)
        sureNewPassword_err = self.login.driver.find_element(By.XPATH,
                                                             '//div[@class="ng-tns-c58-54 ant-form-item-explain-error"]')
        assert sureNewPassword_err.text == expect, '验证失败，请检查！！！'
        print('密码不一致验证成功！！')

    def test_change_password_success(self):
        '''
        这是修改密码成功；没有提示框及内容，所以只能判断提交确定后，回到了首页就成功了
        :return:
        '''
        succ_msg = '您好，祝开心快乐每一天！'
        # 清空内容，输入新旧确认密码
        self.login.driver.find_element(By.ID, 'oldPassword').clear()
        self.login.driver.find_element(By.ID, 'newPassword').clear()
        self.login.driver.find_element(By.ID, 'sureNewPassword').clear()
        self.login.driver.find_element(By.ID, 'oldPassword').send_keys('123321')
        self.login.driver.find_element(By.ID, 'newPassword').send_keys('123321')
        self.login.driver.find_element(By.ID, 'sureNewPassword').send_keys('123456')
        # 点击确定按钮
        btn = self.login.driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-primary ng-star-inserted"]')
        btn.click()
        # 获取确定后首页提示元素
        sleep(2)
        msg=self.login.driver.find_element(By.XPATH,"//h4[@class='left-start-center m-0 ant-typography']")
        assert msg.text==succ_msg,'验证失败！！！请检查'
        print('修改密码成功')

    def teardown_class(self):
        self.login.driver.quit()
        print("执行完毕！关闭浏览器")


if __name__ == '__main__':
    pytest.main(['-sv', 'test_Change_password.py'])
