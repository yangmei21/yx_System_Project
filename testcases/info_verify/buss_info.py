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

    # 取消删除商家认证信息审核数据
    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_del_cancel_shopinfo(self):
        """
        这是商家认证信息删除取消操作用例
        :return:
        """
        # 点击关闭弹框
        self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        sleep(1)

        # 点击信息审核管理
        self.login.driver.find_element(By.XPATH,
                                       '//*[@id="menuNav"]/div[1]/app-side-nav/div/div[2]/app-nav-bar/ul/li[4]/div[1]/span[1]').click()
        sleep(2)
        # 点击商家认证信息审核
        self.login.driver.find_element(By.LINK_TEXT,
                                       '商家认证信息审核').click()
        sleep(1)

        # 获取原列表总数值
        total_records_element = self.login.driver.find_element(By.CSS_SELECTOR,
                                                               'li.ant-pagination-total-text.ng-star-inserted')

        # 获取元素文本信息
        if total_records_element:
            total_records_text = total_records_element.text
            # 从文本中解析出数字
            # 格式为：’1-10 共 xx 条‘，需要获取其中的xx数
            total_records = int(total_records_text.split('共')[-1].split('条')[0].strip())
            print('\n' +"总数据条数：", total_records)
        else:
            print("未获取到总数据提条数")

        # 点击第一条数据删除按钮将弹框点出
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[3]/td[6]/span[2]').click()

        # 定位取消按钮并对其进行处理点击
        cancel_button_xpath = "//button[contains(@class, 'ant-btn') and not(contains(@class, 'ant-btn-primary')) and contains(@class, 'ng-star-inserted') and contains(., '取消')]"
        cancel_button = WebDriverWait(self.login.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cancel_button_xpath)))
        cancel_button.click()
        # 刷新页面
        self.login.driver.refresh()
        sleep(1)
        # 验证是否新增成功（与新增前获取的总数值进行对比）
        cancel_total_records_element = self.login.driver.find_element(By.CSS_SELECTOR,
                                                                      'li.ant-pagination-total-text.ng-star-inserted')

        # 获取元素文本信息
        if cancel_total_records_element:
            cancle_total_records_text = cancel_total_records_element.text
            # 从文本中解析出数字
            # 格式为：’1-10 共 15 条‘，需要获取其中的 15
            cancel_total_records = int(cancle_total_records_text.split('共')[-1].split('条')[0].strip())
            print("取消后列表总数据条数：", cancel_total_records)
        else:
            print("未获取到总数据提条数")

        assert cancel_total_records == total_records
        sleep(1)
        # self.login.driver.quit()

    # 删除商家认证信息审核数据
    def notest_del_succ_shopinfo(self):
        """
        这是商家认证信息删除操作用例
        :return:
        """
        #
        # # 点击关闭弹框
        # self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        # sleep(1)
        #
        # # 点击信息审核管理
        # self.login.driver.find_element(By.XPATH,
        #                                '//*[@id="menuNav"]/div[1]/app-side-nav/div/div[2]/app-nav-bar/ul/li[4]/div[1]/span[1]').click()
        # sleep(2)
        # # 点击商家认证信息审核
        # self.login.driver.find_element(By.LINK_TEXT,
        #                                '商家认证信息审核').click()
        # sleep(1)

        # 获取原列表总数值
        total_records_element = self.login.driver.find_element(By.CSS_SELECTOR,
                                                               'li.ant-pagination-total-text.ng-star-inserted')

        # 获取元素文本信息
        if total_records_element:
            total_records_text = total_records_element.text
            # 从文本中解析出数字
            # 格式为：’1-10 共 xx 条‘，需要获取其中的xx数
            total_records = int(total_records_text.split('共')[-1].split('条')[0].strip())
            print("总数据条数：", total_records)
        else:
            print("未获取到总数据提条数")

        # 点击第一条数据删除按钮将弹框点出
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[3]/td[6]/span[2]').click()

        # 定位确定按钮并对其进行处理点击
        confirm_button_xpath = "//button[contains(@class, 'ant-btn-primary') and contains(@class, 'ng-star-inserted')]"
        confirm_button = WebDriverWait(self.login.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
        confirm_button.click()
        # 刷新页面
        self.login.driver.refresh()
        sleep(1)
        # 验证是否新增成功（与新增前获取的总数值进行对比）
        scu_total_records_element = self.login.driver.find_element(By.CSS_SELECTOR,
                                                                   'li.ant-pagination-total-text.ng-star-inserted')

        # 获取元素文本信息
        if scu_total_records_element:
            scu_total_records_text = scu_total_records_element.text
            # 从文本中解析出数字
            # 格式为：’1-10 共 15 条‘，需要获取其中的 15
            scu_total_records = int(scu_total_records_text.split('共')[-1].split('条')[0].strip())
            print("删除后列表总数据条数：", scu_total_records)
        else:
            print("未获取到总数据提条数")

        assert scu_total_records == total_records - 1
        sleep(1)

    def teardown_class(self):
        self.login.driver.quit()
        print("关闭网页")


if __name__ == '__main__':
    pytest.main('[test_del_bussio.py]')
