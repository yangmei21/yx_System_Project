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
        '''添加房车成功'''
        RV_name = '房车天地'
        RV_detail = '提供多种款式的房车，包括自行式和拖挂式，适合家庭旅行、商务出差和户外探险。'
        RV_add = '北京市朝阳区建国路88号'
        RV_phone = '123-4567-8901'

        # 点击关闭弹框
        self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        sleep(2)
        # 点击发布信息管理
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="menuNav"]/div[1]/app-side-nav/div/div[2]/app-nav-bar/ul/li[3]/div[1]/span[1]').click()
        sleep(2)
        # 点击房车管理
        self.login.driver.find_element(By.LINK_TEXT,
                                       '房车管理').click()

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
            r"F:\picture\test\pic8.png")

        # 上传门店缩略图
        upload_element = self.login.driver.find_element(By.XPATH,
                                                        '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[2]/nz-form-control/div/div/div[1]/nz-upload/div/div/input')
        upload_element.send_keys(r"F:\picture\test\pic9.png")
        # upload_element.send_keys(Keys.RETURN)

        # 填写房车店名称
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[3]/nz-form-control/div/div/input').send_keys(
            RV_name)
        # 填写门店介绍
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[4]/nz-form-control/div/div/textarea').send_keys(
            RV_detail)
        # 填写门店地址
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[5]/nz-form-control/div/div/input').send_keys(
            RV_add)
        # 填写联系电话
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[8]/nz-form-control/div/div/input').send_keys(
            RV_phone)
        sleep(5)
        # 选择开放起始时间
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[6]/nz-form-control/div/div/nz-time-picker/div/input').send_keys(
            "9:30")
        # 选择开放截至时间
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[7]/nz-form-control/div[1]/div/nz-time-picker/div/input').send_keys(
            "20:00")
        sleep(2)
        # 点击确认按钮
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[3]/button[1]').click()
        sleep(1)
        # 刷新页面数据（页面刷新不行，我选择使用点击搜索来刷新！！！不是刷新不行，是变量传递的问题o(╥﹏╥)o）
        self.login.driver.refresh()
        sleep(3)
        # self.login.driver.find_element(By.XPATH,'/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/nz-card/div/form/div/div[3]/button[1]').click()

        # 验证是否新增成功（与新增前获取的总数值进行对比）
        RV_add_total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print("列表总数为：", RV_add_total)

        assert RV_add_total == RV_total + 1

        sleep(3)

        self.login.driver.quit()

    def teardown_class(self):
        print("结束执行！")


if __name__ == '__main__':
    pytest.main(['test_RV_manag.py'])
