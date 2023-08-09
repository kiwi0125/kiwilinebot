import requests
from bs4 import BeautifulSoup

#####傳回油價的函數######
def oil_price():
    target_url = "https://gas.goodlife.tw"
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    #從第一個id為main的尋找第一個文字內容(並且將換行取消)=最後更新時間
    title = soup.select("#main")[0].text.replace("\n","").split("(")[0]
    #從第一個id為gas_price的找到所有的文字內容，並將三個換行跟空格取消
    gas_price = soup.select("#gas-price")[0].text.replace("\n\n\n","").replace(" ","")
    #從第一個id為cpc的找到所有的文字內容(中油那一塊)，並將空格取消
    cpc = soup.select("#cpc")[0].text.replace(" ","")

    #將內容拼湊好
    content = "{}\n{}{}".format(title, gas_price, cpc)
    return content
