# 测试报告生成时 加的描述
from py.xml import html
from datetime import datetime
import pytest


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("测试人：Mei~")])


def pytest_html_report_title(report):
    report.title = "用户登录测试报告"


def pytest_html_results_table_header(cells):
    """
    处理结果表的表头
    """
    # 往表格增加一列Description，并且给Description列增加排序
    cells.insert(2, html.th("Description", class_="sortable desc", col="desc"))
    # 往表格增加一列Time，并且给Time列增加排序
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    # 移除表格最后一列
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """
    处理结果表的行
    """
    # 往列 Description插入每行的值
    cells.insert(2, html.th(report.description))
    # 往列 Time 插入每行的值
    cells.insert(1, html.th(datetime.utcnow(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # 定义列 Description的值，默认为测试方法的文档注释，如果测试方法没有文档注释，就自定义Description的值
    if str(item.function.__doc__) != "None":
        # 结果表的description列的值 = 测试方法的文档注释
        report.description = str(item.function.__doc__)
    else:
        # 结果表的description列的值 = 自定义的信息
        # 注意：这里可以将测试用例中的用例标题或者描述作为列 Description的值
        report.description = "这里是描述信息"
