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
from util import util

'''
驴友招募发布审核:
取消删除:test_del_cancel_Traveler_recruitment
删除:test_del_succ_Traveler_recruitment
审核:test_Audit_Traveler_recruitment
--->这里的操作会存在：审核不通过后数据移到最后一条数据所以要额外写断言，找到位置并进行核对是否状态成功。
数据过多我会把数据先进行状态筛选，然后分别操作o(*￣▽￣*)ブ

不存在查询：test_search_Traveler_recruitment_not_exist
存在的查询：test_search_Traveler_recruitment_exist
'''


class Test_Audit_Traveler_recruitment(object):
    def setup_class(self):
        self.login = TestAdminLogin
        print("调用管理员登录")

    # 进入驴友招募审核页
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_goto_aduit_travel_diary(self):
        """
        进入驴友招募审核页
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
                                       '驴友招募').click()
        sleep(1)
        print('\n成功进入驴友招募审核界面!!!')

    # 取消驴友招募审核删除数据
    def test_del_cancel_Traveler_recruitment(self):
        """
        这是驴友招募删除取消操作用例
        :return:
        """
        # 获取原列表总数值
        total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print('\n列表数：', total)

        # 点击第一条数据删除按钮将弹框点出
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[7]/span[2]').click()

        # 定位取消按钮并对其进行处理点击
        cancel_button_xpath = '//button[@class="ant-btn ng-tns-c78-61 ng-star-inserted"]'
        cancel_button = WebDriverWait(self.login.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cancel_button_xpath)))
        cancel_button.click()
        # 刷新页面
        self.login.driver.refresh()
        sleep(2)
        # 验证是否新增成功（与新增前获取的总数值进行对比）
        cancel_total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print('取消的列表数：', cancel_total)

        assert total == cancel_total, '取消操作失败，取消后的总数与未取消前数量不一致，请检查！！！'
        print('取消操作执行成功！！！')
        sleep(1)

    # 删除驴友招募审核数据
    def test_del_suc_Traveler_recruitment(self):
        """
        这是驴友招募删除操作用例--删除的是列表中第一条数据
        :return:
        """
        # 获取列表数
        total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print('\n列表数：', total)

        # 点击第一条数据删除按钮将弹框点出
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[7]/span[2]').click()

        # 定位确定按钮并对其进行处理点击
        confirm_button_xpath = '//button[@class="ant-btn ng-tns-c78-57 ant-btn-primary ng-star-inserted"]'
        confirm_button = WebDriverWait(self.login.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, confirm_button_xpath)))
        confirm_button.click()
        # 刷新页面
        self.login.driver.refresh()
        sleep(2)
        # 验证是否删除成功（与删除前获取的总数值进行对比）
        del_total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print('取消的列表数：', del_total)

        assert total - 1 == del_total, '操作失败！！！请检查~'
        print('删除成功！！！')
        sleep(1)

    def test_Audit_Traveler_recruitment(self):
        '''
        这里是驴友招募审核
        :return:
        '''

        sleep(2)
        # 新解决思路：获取第一条数据的状态，分别执行，如果是未通过可以根据标题进行查询然后核验状态（数据过多时的最优解决，这样就不用看行列数来构造Xpath了）
        title = self.login.driver.find_element(By.XPATH,
                                               '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[1]/span')
        key = title.text
        print('\n该数据审核标题为：', key)

        # 获取数据状态
        status = self.login.driver.find_element(By.XPATH,
                                                '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[4]')
        print('\n该数据审核状态为：', status.text)

        # 进入审核界面
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[7]/span[1]').click()
        sleep(3)
        # 界面最大化[关注页面是否刷新操作，因为前面的步骤导致元素xpath会不一致，所以要复现前面的步骤才能定位到最新的xpath]
        self.login.driver.find_element(By.XPATH,
                                       '//span[@class="hover-blue full-height flex-auto text-right d-i-b ng-tns-c89-0"]').click()

        if status.text == '审核通过':
            # 点击审核页不通过按钮
            self.login.driver.find_element(By.XPATH,
                                           '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[1]/nz-form-control/div/div/nz-radio-group/label[2]/span[1]/input').click()
            # 填写原因
            self.login.driver.find_element(By.NAME, 'auditMsg').send_keys("测试。")
            # 点击确定按钮
            self.login.driver.find_element(By.XPATH,
                                           '//button[@class="ant-btn ant-btn-primary ng-star-inserted"]').click()
            sleep(2)
            # 先根据title来查询，因为到最后了
            self.login.driver.find_element(By.XPATH, "//input[@name='name' and @placeholder='请输入活动名称']").send_keys(key)
            # 点击查询按钮
            self.login.driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            # 获取新状态
            changes = self.login.driver.find_element(By.XPATH,
                                                     '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[4]')
            # 断言查看是否审核成功
            assert changes.text == '审核未通过', '更改未成功，审核后状态显示错误！！！请检查'
            print('该数据已正确更改审核状态；通过-->未通过！！！,目前该数据状态为：', changes.text)
        elif status.text == '审核未通过':
            # 点击审核页通过按钮
            self.login.driver.find_element(By.XPATH,
                                           '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[1]/nz-form-control/div/div/nz-radio-group/label[1]/span[1]/input').click()
            # 点击确定按钮
            self.login.driver.find_element(By.XPATH,
                                           '//button[@class="ant-btn ant-btn-primary ng-star-inserted"]').click()
            sleep(2)
            # 判断修改后的审核状态
            changes = self.login.driver.find_element(By.XPATH,
                                                     '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[4]')
            # 断言查看是否审核成功
            assert changes.text == '审核通过'
            print('该数据已正确更改审核状态；未通过-->通过！！！,目前该数据状态为：', changes.text)
        elif status.text == '待审核':
            # 点击审核页通过按钮
            self.login.driver.find_element(By.XPATH,
                                           '//*[@id="cdk-overlay-2"]/nz-modal-container/div/div/div[2]/app-dept-manage-modal/form/nz-form-item[1]/nz-form-control/div/div/nz-radio-group/label[1]/span[1]/input').click()
            # 点击确定按钮
            self.login.driver.find_element(By.XPATH,
                                           '//button[@class="ant-btn ant-btn-primary ng-star-inserted"]').click()
            sleep(2)
            # 先根据title来查询，因为到别的位置了
            self.login.driver.find_element(By.XPATH, "//input[@name='name' and @placeholder='请输入活动名称']").send_keys(key)
            # 点击查询按钮
            self.login.driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            # 获取新状态
            changes = self.login.driver.find_element(By.XPATH,
                                                     '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[4]')
            # 断言查看是否审核成功
            assert changes.text == '审核通过'
            print('该数据已正确更改审核状态；未审核-->通过！！！,目前该数据状态为：', changes.text)
        else:
            print("未获取到审核状态，请检查是否存在数据或使用其他定位方法！！！")

        sleep(2)

    def test_search_Traveler_recruitment_not_exist(self):
        '''
        这里是查询驴友招募审核列表--不存在
        :return:
        '''
        self.login.driver.refresh()
        sleep(2)
        # 定义查询关键字
        keys = '不存在'
        # 填入查询内容
        self.login.driver.find_element(By.XPATH, "//input[@name='name' and @placeholder='请输入活动名称']").send_keys(keys)
        # 点击查询按钮
        self.login.driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()
        # 定位查询结果内容
        result = self.login.driver.find_element(By.XPATH, "//p[@class='ant-empty-description ng-star-inserted']")
        print('\n查询结果提示：', result.text)
        # 断言判定是否成功
        assert result.text == '暂无数据'
        print('查询不存在结束')
        sleep(1)

    def test_search_Traveler_recruitment_exist(self):
        '''
        这里是查询驴友招募信息审核列表--存在
        :return:
        '''
        # 刷新页面
        self.login.driver.refresh()
        sleep(2)
        # 获取列表第一条数据标题（存在的数据）
        exist_title = self.login.driver.find_element(By.XPATH,
                                                     '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[1]/span')
        print('\n存在的标题名称为：', exist_title.text)
        #  获取存在第一条数据的分类（一定存在的）
        exist_classify = self.login.driver.find_element(By.XPATH,
                                                        '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[4]')
        print('存在的分类名称为：', exist_classify.text)

        exist_type = self.login.driver.find_element(By.XPATH,
                                                    '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[3]')
        print('存在的类型为：', exist_type.text)
        # 点击展开，把所有的搜索条件展示出来：
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/nz-card/div/form/div/div[3]/a/span').click()
        # 输入标题到搜索框
        self.login.driver.find_element(By.XPATH, "//input[@name='name' and @placeholder='请输入活动名称']").send_keys(
            exist_title.text)

        # 展开类型分类
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/nz-card/div/form/div/div[3]/nz-form-item/nz-form-control/div/div/nz-select/nz-select-top-control').click()
        # 输入选择分类到框中
        sleep(1)

        options = WebDriverWait(self.login.driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   '//*[@id="cdk-overlay-2"]/nz-option-container/div/cdk-virtual-scroll-viewport/div[1]/nz-option-item'))
        )

        # 定位并选择自己想要勾选的分类
        for option in options:
            if option.text == exist_type.text:
                option.click()
                break
        sleep(2)

        # 展开状态分类
        self.login.driver.find_element(By.XPATH,
                                       "/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/nz-card/div/form/div/div[2]/nz-form-item/nz-form-control/div/div/nz-select/nz-select-top-control").click()
        # 输入选择分类到框中
        sleep(1)

        option1s = WebDriverWait(self.login.driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   '//*[@id="cdk-overlay-3"]/nz-option-container/div/cdk-virtual-scroll-viewport/div[1]/nz-option-item'))
        )

        # 定位并选择自己想要勾选的分类
        for option in option1s:
            if option.text == exist_classify.text:
                option.click()
                break
        sleep(2)
        # 点击搜索按钮
        self.login.driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()

        # 判断是否查到数据【判断列表是否有数据】
        research_total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print("列表查询到的数为：", research_total)
        # 断言(好像不太严谨，但是目前方法准测是是商家名称唯一，存在一条数据)
        assert research_total == 1
        print('根据查询活动名称与审核状态能够正确查询！！！查询数为', research_total)
        sleep(2)

    def teardown_class(self):
        self.login.driver.quit()
        print("关闭网页登录")


if __name__ == '__main__':
    pytest.main('-vs', '[test_Audit_Traveler_recruitment.py]', '--reruns=2')
