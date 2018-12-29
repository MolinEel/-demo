import requests
from lxml import html
import json
from urllib import request as urllib2
from lxml import etree
import json
import xlsxwriter
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}


def spider():
    """
    爬取数据
    :rtype: object
    """
    url = 'http://movie.mtime.com/228745/reviews/short/new.html'  # 需要爬数据的网址
    # page = requests.Session().get(url)
    # tree = html.fromstring(page.text)
    # node_list = tree.xpath('//dd[contains(@class)]')
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    dom = etree.HTML(html)
    # 模糊查询  存储为根节点
    node_list = dom.xpath('//div[@class="mod_short"]')
    list_item = list()
    for node in node_list:
        # 得到用户名
        user = node.xpath('.//p[@class="px14"]/a/text()')[0]
        # 得到评论
        comment = node.xpath('./h3/text()')[0]  # 获取需要的数据
        # 得到评分
        score = node.xpath('.//span[@class="db_point ml6"]/text()')[0]
        # 得到时间
        time = node.xpath('.//div[@class="mt10"]/a/@entertime')[0]
        # # 创建dict
        items = {'user': user,
                 'comment': comment,
                 'score': score,
                 'time': time}
        list_item.append(items)
        with open('qiushi.json', 'a', encoding='utf-8') as file:
            file.write(json.dumps(items, ensure_ascii=False) + '\n')
    print(len(list_item))
    print(list_item)
    save_data(list_item)

            # # 得到用户名
            # node = node_list[0]
            # user = node.xpath('.//p[@class="px14"]/a/text()')
            # # 得到评论
            # comment = node.xpath('./h3/text()')  # 获取需要的数据
            # # 得到评分
            # score = node.xpath('.//span[@class="db_point ml6"]/text()')
            # # 得到时间
            # time = node.xpath('.//div[@class="mt10"]/a/@entertime')
            # print(node_list)
            # print(user)
            # print(comment)
            # print(score)
            # print(time)


def save_data(list_data):
    """将数据导出到表格
    :rtype: object
    """
    print(len(list_data))
    # 创建xlsx文件
    workbook = xlsxwriter.Workbook('comments.xlsx')
    # 新增工作区
    worksheet = workbook.add_worksheet()
    i = 0
    # 循环添加进表格
    while i < len(list_data):
        # write(行，列，数据)
        worksheet.write(i, 0, list_data[i]['user'])
        worksheet.write(i, 1, list_data[i]['comment'])
        worksheet.write(i, 2, list_data[i]['score'])
        worksheet.write(i, 3, list_data[i]['time'])
        i += 1
    # 注意关闭文件
    workbook.close()

if __name__ == "__main__":
    spider()

# 求属性值  @xx
# 求文本值 text()
