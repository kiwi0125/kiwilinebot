import requests
from bs4 import BeautifulSoup

#####傳回油價的函數######
def oil_price():
    target_url = "https://gas.goodlife.tw"
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    #從第一個id為main的文字內容尋找
    title = soup.select("#main")[0].text.replace("\n","").split("(")[0]
    gas_price = soup.select("#gas-price")[0].text.replace("\n\n\n","").replace(" ","")
    cpc = soup.select("#cpc")[0].text.replace(" ","")
    content = "{}\n{}{}".format(title, gas_price, cpc)
    return content
