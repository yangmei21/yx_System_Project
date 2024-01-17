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

'''
商家注册页面功能测试用例
注册商家信息新增：test_regist_buss
商家信息删除：test_regist_buss_del
商家信息提交审核:test_regist_buss_submit
不存在商家信息查询:test_regist_buss_search_noexist
存在商家信息查询:test_regist_buss_search_exist
编辑商家信息：test_regist_buss_edit
'''


# 数据是手动写入，每次需要在文件中来修改
class Test_regist_buss(object):
    def setup_class(self):
        self.login = TestAdminLogin
        print("调用管理员登录")

    @pytest.mark.dependency(depends=['admin_login'], scope='module')
    def test_goto_regist_buss(self):
        '''
        这是判断是否进入了商家注册页
        :return:
        '''
        # 点击关闭弹框
        self.login.driver.find_element(By.XPATH, '//*[@id="driver-popover-item"]/div[4]/button').click()
        # 点击仪表盘(默认打开的)
        # self.login.driver.find_element(By.XPATH,
        #                                '//*[@id="menuNav"]/div[1]/app-side-nav/div/div[2]/app-nav-bar/ul/li[1]/div[1]').click()
        # 点击商家注册
        self.login.driver.find_element(By.LINK_TEXT, '商家注册').click()
        sleep(1)
        present_url = self.login.driver.current_url
        assert present_url == 'http://202.111.177.155:8081/manager/static/ng-ant-admin/index.html#/default/dashboard/businessadd'
        print('\n成功进入商家注册页')

        sleep(2)

    def test_regist_buss_add(self):
        """
        注册商家信息新增
        :return:
        """
        bus_name = '华阳餐饮有限公司'
        bus_code = '91440101MA5D7H1U5E'
        Represen = '刘小林'
        bus_money = '600'
        bus_add = '广州市天河区珠江新城华明路9号2304室'
        bus_time = '10年'
        bus_part = '餐饮管理、酒店管理、中餐服务、快餐服务。'

        # 获取商家注册列表数
        total_regist = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print('\n该列表总数：', total_regist)

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
        print('新增后的商家注册数为：', total_add_regist)
        # 验证是否新增成功
        assert total_regist + 1 == total_add_regist
        sleep(1)

    def test_regist_buss_del(self):
        """
        这是商家注册信息删除
        :return:
        """
        # 获取页面数量
        self.login.driver.refresh()
        sleep(2)
        total_regist = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print("\n列表总数为", total_regist)
        # 点击删除按钮
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[6]/span[2]').click()
        # 点击确定
        self.login.driver.find_element(By.XPATH,
                                       '//button[@class="ant-btn ng-tns-c78-55 ant-btn-primary ng-star-inserted"]').click()
        # 获取删除后列表数
        total_regist_del = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print("删除后，列表总数为：", total_regist_del)
        # 断言判定是否通过
        assert total_regist_del == total_regist - 1
        sleep(2)

    def test_regist_buss_submit(self):
        '''
        这里是提交审核用例
        :return:
        '''
        self.login.driver.refresh()
        sleep(2)
        # 判断第一条数据的状态，已提交则不需要执行，若未提交便执行提交操作
        status = self.login.driver.find_element(By.XPATH,
                                                '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[4]')
        if status.text == '待提交':
            # 点击提交审核
            self.login.driver.find_element(By.XPATH,
                                           '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[6]/span[3]').click()
            # 点击确定
            self.login.driver.find_element(By.XPATH,
                                           '//*[@id="cdk-overlay-2"]/nz-modal-confirm-container/div/div/div/div/div[2]/button[2]').click()
            sleep(2)
            # 定位第一条数据提交审核后的状态
            status_submit = self.login.driver.find_element(By.XPATH,
                                                           '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[4]')
            sleep(2)
            # 断言判断是否成功
            assert status_submit.text == '待审核'
            print('\n提交审核成功')
        else:
            pytest.skip('该数据已提交审核，不用执行')

    def test_regist_buss_search_noexist(self):
        '''
        这里是查询不存在的商家信息
        :return:
        '''
        self.login.driver.refresh()
        sleep(2)
        # 搜索框填写不存在内容
        self.login.driver.find_element(By.XPATH, '//input[@placeholder="请输入企业名称"]').send_keys('不存在')
        # 点击搜索按钮
        self.login.driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-primary"]').click()
        # 获取列表文字
        notice = self.login.driver.find_element(By.XPATH, '//p[@class="ant-empty-description ng-star-inserted"]')
        print('\n查询结果页提示：', notice.text)
        # 断言判断
        assert notice.text == '暂无数据'
        print('成功执行查询不存在用例！！！')

    def test_regist_buss_search_exist(self):
        '''
        这里是查询存在的商家信息
        :return:
        '''
        self.login.driver.refresh()
        sleep(2)
        # 获取列表第一条数据标题（存在的数据）
        exist_title = self.login.driver.find_element(By.XPATH,
                                                     '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[1]/span')
        print('\n存在的标题名称为：', exist_title.text)

        # 输入标题到搜索框
        self.login.driver.find_element(By.XPATH, '//input[@placeholder="请输入企业名称"]').send_keys(
            exist_title.text)

        # 点击搜索按钮
        self.login.driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()

        # 判断是否查到数据【判断列表是否有数据】
        research_total = util.get_total(self.login.driver, '.ant-pagination-total-text')
        print("列表查询到的数为：", research_total)
        # 断言(好像不太严谨，但是目前方法准测是是商家名称唯一，存在一条数据)
        assert research_total == 1
        print('根据查询企业名称与审核状态能够正确查询！！！查询数为', research_total)

    def test_regist_buss_edit(self):
        '''
        这是编辑商家注册验证
        :return:
        '''
        self.login.driver.refresh()
        sleep(2)
        edit_title = 'edit_name'
        # 获取当前标题
        now_title = self.login.driver.find_element(By.XPATH,
                                                   '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[1]/span')
        print('\n修改前的商家名称为：', now_title.text)
        # 点击修改进入修改页面
        self.login.driver.find_element(By.XPATH,
                                       '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[6]/span[1]').click()
        # 清除之前的填写内容
        self.login.driver.find_element(By.NAME, 'companyName').clear()
        # 输入新的名称
        self.login.driver.find_element(By.NAME, 'companyName').send_keys(edit_title)
        # 点击确认提交修改
        self.login.driver.find_element(By.XPATH, '//button[@class="ant-btn ant-btn-primary ng-star-inserted"]').click()
        sleep(2)
        # 获取修改后的名称
        edits_title = self.login.driver.find_element(By.XPATH,
                                                     '/html/body/app-root/div/app-default/app-def-layout-content/nz-layout/nz-layout/nz-layout/nz-content/div/div/app-dept/div/app-card-table-wrap/nz-card/div[2]/app-tree-table/nz-table/nz-spin/div/div/nz-table-inner-scroll/div/table/tbody/tr[2]/td[1]/span')
        print('修改后的名称：', edits_title.text)
        # 断言判断第一条数据是否修改成功
        assert edits_title.text == edit_title

    def teardown_class(self):
        self.login.driver.quit()
        print("关闭网页")


if __name__ == '__main__':
    pytest.main(['test_buss_regist.py'])

# 终端执行： pytest .\testcases\board\test_buss_regist.py --html=.\reports\buss_regist_report.html --self-contained-html
