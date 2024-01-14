from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.keys import Keys
import re
import pytest
from testcases.test_admin_login import TestAdminLogin
from util import util


class TestRVmanag(object):

    def setup_method(self):
        self.login = TestAdminLogin
        print('调用loginadmin--setup')

    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_add_RV(self):
        '''添加床车成功'''
        Bedcar_name = '自在旅途床车店'
        Bedcar_detail = '自在旅途床车店是一家专注于提供床车自驾游服务的商家。我们提供多种款式的床车，以及详细的自驾游攻略，让您在旅途中尽情享受自由和舒适。'
        Bedcar_add = '成都市武侯区人民南路四段8号附2号'
        Bedcar_phone = '028-66667890'
        sleep(3)
        # 点击关闭弹框
        self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        sleep(2)
        # 点击发布信息管理
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="menuNav"]/div[1]/app-side-nav/div/div[2]/app-nav-bar/ul/li[3]/div[1]/span[1]').click()
        sleep(2)
        # 点击景点管理
        self.login.driver.find_element(By.LINK_TEXT,
                                       '床车管理').click()

        sleep(2)
        # 获取列表数据总数
        # ！！！
        # 定位包含总数据条数信息的元素
        RV_total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print("列表总数为：", RV_total)

        # 点击新建
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[1]/div/div[2]/div/div[1]/button').click()
        # 页面最大化
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/button/span/div/span[1]').click()

        # 上传门店图片
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[1]/nz-form-control/div/div/div[1]/nz-upload/div/div/input').send_keys(
            r"F:\picture\test\pic10.png")

        # 上传门店缩略图
        upload_element = self.login.driver.find_element(By.XPATH,
                                                        '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[2]/nz-form-control/div/div/div[1]/nz-upload/div/div/input')
        upload_element.send_keys(r"F:\picture\test\pic10.png")
        # upload_element.send_keys(Keys.RETURN)

        # 填写房车店名称
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[3]/nz-form-control/div/div/input').send_keys(
            Bedcar_name)
        # 填写门店介绍
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[4]/nz-form-control/div/div/textarea').send_keys(
            Bedcar_detail)
        # 填写门店地址
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[5]/nz-form-control/div/div/input').send_keys(
            Bedcar_add)
        # 填写联系电话
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[8]/nz-form-control/div/div/input').send_keys(
            Bedcar_phone)
        sleep(5)
        # 选择开放起始时间
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[6]/nz-form-control/div/div/nz-time-picker/div/input').send_keys(
            "8:30")
        # 选择开放截至时间
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[7]/nz-form-control/div[1]/div/nz-time-picker/div/input').send_keys(
            "22:00")
        sleep(2)
        # 点击确认按钮
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[3]/button[1]').click()
        sleep(1)
        # 刷新页面数据（页面刷新不行，我选择使用点击搜索来刷新！！！不是刷新不行，是变量传递的问题o(╥﹏╥)o）
        self.login.driver.refresh()
        # self.login.driver.find_element(By.XPATH,'/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/nz-card/div/form/div/div[3]/button[1]').click()
        sleep(1)
        # 验证是否新增成功（与新增前获取的总数值进行对比）
        RV_add_total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print("列表总数为：", RV_add_total)

        assert RV_add_total == RV_total + 1

        sleep(3)

    def teardowm_class(self):
        self.login.driver.quit()


if __name__ == '__main__':
    pytest.main(['-vs','test_Bedcar_manag.py'])
