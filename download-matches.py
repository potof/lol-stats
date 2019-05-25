# coding: UTF-8
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary


csvfile = open("./url_list.csv", "r", encoding="utf-8")
csvreader = csv.reader(csvfile, delimiter=",")

# 裏でブラウザを起動する
options = Options()
options.set_headless(True)
driver = webdriver.Chrome(options=options)
driver.set_script_timeout(10)


for row in csvreader:

    # 「#」から始まる行はコメントとして扱う
    if row[0][0] == "#":
        continue

    url = row[1]
    htmlfilename = "./data/" + row[0] + "_" + row[2] + ".html"

    driver.get(url)
    time.sleep(10)
    html = driver.page_source

    with open(htmlfilename, "w", newline="", encoding="utf-8") as f:
        f.write(html)
    f.close()

