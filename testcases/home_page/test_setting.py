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


class TestDelshopinfo(object):
    def setup_class(self):
        self.login = TestAdminLogin
        print("调用管理员登录")
        self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        sleep(1)

    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_settings(self):
        expect = '修改成功！'
        """
        这是商家设置个人信息操作用例
        :return:
        """
        # 定位头像框
        el = self.login.driver.find_element(By.XPATH, '//*[@id="tools"]/span[3]/img')
        # 悬停鼠标并显示下拉框
        ActionChains(self.login.driver).move_to_element(el).perform()
        sleep(2)
        # 定位下拉框设置个人信息元素并点击进入设置信息页面
        self.login.driver.find_element(By.LINK_TEXT, '个人设置').click()
        # 最大化页面
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-3"]/nz-modal-container/div/div/button/span/div/span[1]').click()
        # 上传头像（前端非input框 不测了）
        # upload_element = self.login.driver.find_element(By.XPATH,
        #                                                 '//*[@id="cdk-overlay-3"]/nz-modal-container/div/div/div[2]/app-base/div/div[2]/div/div/nz-upload/div/div/button')
        # upload_element.send_keys(r"F:\picture\test\pic1.png")
        # 上传昵称
        name = self.login.driver.find_element(By.ID, 'nickname')
        name.clear()
        name.send_keys('ττ')
        # 上传个人简介
        introdu = self.login.driver.find_element(By.ID, 'descs')
        introdu.clear()
        introdu.send_keys('最重要的就是不要去看远方模糊的，而要做手边清楚的事。')

        # 点击确认按钮
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-3"]/nz-modal-container/div/div/div[3]/button[1]').click()

        # 定位toast弹框内容
        loc = (By.CLASS_NAME, 'ant-message-notice-content')
        WebDriverWait(self.login.driver, 20, 0.5).until(EC.visibility_of_element_located(loc))
        msg = self.login.driver.find_element(*loc).text
        print(msg)

        # 断言
        assert msg == expect

    def teardown_class(self):
        self.login.driver.quit()


if __name__ == '__main__':
    pytest.main(['-sv', 'test_setting.py'])
