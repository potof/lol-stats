# coding: UTF-8
import dataclasses
from dataclasses import field
import csv
import time
import datetime
import re
import requests
from bs4 import BeautifulSoup

class Player:

    roles = ("top", "jg", "mid", "adc", "sup")

    def __init__(self, playerno, teamno):
        self.teamno = teamno
        self.role = Player.roles[playerno]
        self.playerno = playerno
        if self.teamno == 1:
            self.playerno += 5
        self.name = ""
        self.champion = ""
        self.kill = 0
        self.death = 0
        self.assist = 0
        self.cs = 0
        self.stats = {}

    def to_dict(self):
        t = {"name":self.name, "champion":self.champion, "role":self.role, "kill":self.kill,
                "death":self.death,"assist":self.assist, "cs": self.cs}
        t.update(self.stats)
        return t
    
    def parse(self, soup):
        div_names = soup.select("div.champion-nameplate-name > div > span")
        self.name = div_names[self.playerno].text

        div_champs = soup.select("div.player > div.champion-col > div > div.champion-nameplate > div > div > div")
        self.champion = div_champs[self.playerno].attrs["data-rg-id"]

        # プレイヤーの詳細statsを登録する
        rows = soup.select("tbody#stats-body > tr.grid-row")
        for row in rows:

            # 項目(div.viewで項目を表示しているぽい)
            key = row.find("div", class_="view").string.replace("\n","")

            # 値(div.grid-cellで値を表示しているぽい)
            value = row.find_all("div", class_="grid-cell")

            self.__set_stats(key, value[self.playerno].string.replace("\n",""))

    def __set_stats(self, key, val):
        if val == "-":
            self.stats[key] = 0
        elif val == "○":
            self.stats[key] = 0
        elif val == "●":
            self.stats[key] = 1
        elif key == "KDA":
            n = val.split("/")
            self.kill = int(n[0])
            self.death = int(n[1])
            self.assist = int(n[2])
            if self.death == 0 or (self.kill + self.assist) == 0:
                self.stats[key] = self.kill + self.assist
            else:
                self.stats[key] = (self.kill + self.assist) / self.death
        elif re.match(r"([0-9]+\.[0-9]+k)|([0-9]+k)", val):
            self.stats[key] = float(val.rstrip("k")) * 1000
        else:
            self.stats[key] = val


class Team:

    def __init__(self, teamno):
        self.teamno = teamno
        self.game_result= ""
        # TODO: 配列にする
        self.player1 = Player(0, teamno)
        self.player2 = Player(1, teamno)
        self.player3 = Player(2, teamno)
        self.player4 = Player(3, teamno)
        self.player5 = Player(4, teamno)
        self.towers_destroyed = 0
        self.inhibitors_destroyed = 0
        self.barons_slain = 0
        self.dragons_slain = 0
        self.rift_heralds_slain = 0
        # TODO: 配列にする
        self.ban1 = ""
        self.ban2 = ""
        self.ban3 = ""
        self.ban4 = ""
        self.ban5 = ""

    def to_csv(self):
        cm = {"game_result":self.game_result, "towers_destroyed":self.towers_destroyed, "inhibitors_destroyed":self.inhibitors_destroyed,
            "barons_slain":self.barons_slain, "dragons_slain":self.dragons_slain, "rift_heralds_slain":self.rift_heralds_slain,
            "ban1":self.ban1, "ban2":self.ban2, "ban3":self.ban3, "ban4":self.ban4, "ban5":self.ban5}
        p1 = self.player1.to_dict()
        p2 = self.player2.to_dict()
        p3 = self.player3.to_dict()
        p4 = self.player4.to_dict()
        p5 = self.player5.to_dict()
        p1.update(cm)
        p2.update(cm)
        p3.update(cm)
        p4.update(cm)
        p5.update(cm)
        return p1, p2, p3, p4, p5

    def parse(self, soup):

        self.towers_destroyed = soup.select("div.tower-kills > span")[self.teamno].text
        self.inhibitors_destroyed = soup.select("div.inhibitor-kills > span")[self.teamno].text
        self.barons_slain = soup.select("div.baron-kills > span")[self.teamno].text
        self.dragons_slain = soup.select("div.dragon-kills > span")[self.teamno].text
        self.rift_heralds_slain = soup.select("div.rift-herald-kills > span")[self.teamno].text
        self.game_result = soup.select("div.game-conclusion")[self.teamno].text.strip()

        # TODO: きれいにできそう
        div_bans = soup.select("div.bans > div.champion-nameplate > div > div > div")
        if self.teamno == 0:
            self.ban1 = div_bans[0].attrs["data-rg-id"]
            self.ban2 = div_bans[1].attrs["data-rg-id"]
            self.ban3 = div_bans[2].attrs["data-rg-id"]
            self.ban4 = div_bans[3].attrs["data-rg-id"]
            self.ban5 = div_bans[4].attrs["data-rg-id"]
        elif self.teamno == 1:
            self.ban1 = div_bans[5].attrs["data-rg-id"]
            self.ban2 = div_bans[6].attrs["data-rg-id"]
            self.ban3 = div_bans[7].attrs["data-rg-id"]
            self.ban4 = div_bans[8].attrs["data-rg-id"]
            self.ban5 = div_bans[9].attrs["data-rg-id"]
        
        self.player1.parse(soup)
        self.player2.parse(soup)
        self.player3.parse(soup)
        self.player4.parse(soup)
        self.player5.parse(soup)

class Game:

    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(self.html, "lxml")
        self.date = ""
        self.time = ""
        # TODO: team1, team2 は配列にしたほうがよさそう
        self.team1 = Team(0)
        self.team2 = Team(1)

    def to_csv(self):
        t1 = self.team1.to_csv()
        t2 = self.team2.to_csv()
        rs = []
        for t in t1:
            t.update({"date":self.date, "time":self.time})
            rs.append(t)
        for t in t2:
            t.update({"date":self.date, "time":self.time})
            rs.append(t)
        return rs

    def parse(self):
        self.time = self.soup.select_one("div#binding-698").text
        self.date = self.soup.select_one("div#binding-699").text

        self.team1.parse(self.soup)
        self.team2.parse(self.soup)



# ダウンロードしたhtmlファイルを開く
htmlfile = './data/sample.html'
with open(htmlfile , encoding='utf-8') as f:
    html = f.read()

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "lxml")

game = Game(html)
game.parse()

# CSV出力
output_file = "./output/LJL-stats.csv"
with open( output_file, "w", newline="") as f:
    csv_g = game.to_csv()
    writer = csv.DictWriter(f, csv_g[0].keys())
    writer.writeheader()
    writer.writerows(csv_g)
f.close()

