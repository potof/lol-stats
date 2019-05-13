# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary



# # TODO URLはlolesports.apiから取ってくる
# # http://loltool.info/promatch/
# # http://api.lolesports.com/api/v1/scheduleItems?leagueId=42
# url = "https://matchhistory.na.leagueoflegends.com/en/#match-details/ESPORTSTMNT03/1000235?gameHash=2c25f80326c7ac14&tab=stats"

# # TODO htmlをローカルに保存する
# # get html file
# # r = requests.get(url) 
# # soup = BeautifulSoup(r.text, "lxml")
# # print(r)

# # ブラウザのオプションを格納する変数をもらってきます。
# options = Options()

# # Headlessモードを有効にする（裏で起動する）
# options.set_headless(True)

# # ブラウザを起動してhtmlを取得する
# driver = webdriver.Chrome(chrome_options=options)
# driver.get(url)

# # HTMLの文字コードをUTF-8に変換する
# html = driver.page_source.encode('utf-8')
