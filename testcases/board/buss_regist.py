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

# 数据是手动写入，每次需要在文件中来修改
class Test_regist_buss(object):
    def setup_class(self):
        self.login = TestAdminLogin
        print("调用管理员登录")

    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_regist_buss(self):
        """
        注册商家信息提交
        :return:
        """
        bus_name = '华阳餐饮有限公司'
        bus_code = '91440101MA5D7H1U5E'
        Represen = '刘小林'
        bus_money = '600'
        bus_add = '广州市天河区珠江新城华明路9号2304室'
        bus_time = '10年'
        bus_part = '餐饮管理、酒店管理、中餐服务、快餐服务。'

        # 点击关闭弹框
        self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        # 点击仪表盘(默认打开的)
        # self.login.driver.find_element(By.XPATH,
        #                                '//*[@id="menuNav"]/div[1]/app-side-nav/div/div[2]/app-nav-bar/ul/li[1]/div[1]').click()
        # 点击商家注册
        self.login.driver.find_element(By.LINK_TEXT, '商家注册').click()
        sleep(1)

        # 获取商家注册列表数
        total_regist = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print('该列表总数：', total_regist)

        # 点击新建按钮
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[1]/div/div[2]/div/div[1]/button').click()
        sleep(2)
        # 页面最大化
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/button/span/div/span[1]').click()

        # 上传法人身份证
        upload_element = self.login.driver.find_element(By.XPATH,
                                                        '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/div[1]/div[1]/nz-form-item/nz-form-control/div/div/div[1]/nz-upload/div/div/input')
        upload_element.send_keys(r"F:\picture\test\pic1.png")

        # 上传营业执照
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/div[1]/div[2]/nz-form-item/nz-form-control/div/div/div[1]/nz-upload/div/div/input').send_keys(
            r"F:\picture\test\pic2.png")

        # 填写企业名称
        self.login.driver.find_element(By.NAME, 'companyName').send_keys(bus_name)
        # 社会信用代码填写
        self.login.driver.find_element(By.NAME, 'unifiedSocialCreditCode').send_keys(bus_code)
        # 法定代表人填写
        self.login.driver.find_element(By.NAME, 'legalRepresentative').send_keys(Represen)
        # 经营状态选择
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/div[3]/div[2]/nz-form-item/nz-form-control/div/div/nz-select').click()
        sleep(1)

        options = WebDriverWait(self.login.driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   '//*[@id="cdk-overlay-3"]/nz-option-container/div/cdk-virtual-scroll-viewport/div[1]/nz-option-item/div'))
        )

        # 定位并选择自己想要勾选的分类
        for option in options:
            if option.text == "存续":
                option.click()
                break
        sleep(2)

        # 注册资本
        self.login.driver.find_element(By.NAME, 'registeredCapital').send_keys(bus_money)
        # 营业期限
        self.login.driver.find_element(By.NAME, 'businessTerm').send_keys(bus_time)
        # 注册地址
        self.login.driver.find_element(By.NAME, 'registeredAddress').send_keys(bus_add)
        # 经营范围
        self.login.driver.find_element(By.NAME, 'businessScope').send_keys(bus_part)

        sleep(2)
        # 点击确定按钮
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[3]/button[1]').click()

        sleep(2)
        # 获取新增商家注册后列表数
        total_add_regist = util.get_total(self.login.driver, '.ant-pagination-total-text')

        # 验证是否新增成功
        assert total_regist + 1 == total_add_regist

    def teardown_class(self):
        self.login.driver.quit()


if __name__ == '__main__':
    pytest.main(['buss_regist'])
