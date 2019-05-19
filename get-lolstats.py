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

    def __init__(self):
        self.name = ""
        self.champion = ""
        self.role = ""
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
    
    def set_stats(self, key, val):
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

    def __init__(self):
        self.game_result= ""
        # TODO: player1~5は配列にしたほうがよさそう
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.player4 = Player()
        self.player5 = Player()
        self.towers_destroyed = 0
        self.inhibitors_destroyed = 0
        self.barons_slain = 0
        self.dragons_slain = 0
        self.rift_heralds_slain = 0
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

class Game:

    def __init__(self):
        self.date = ""
        self.time = ""
        # TODO: team1, team2 は配列にしたほうがよさそう
        self.team1 = Team()
        self.team2 = Team()

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

# ダウンロードしたhtmlファイルを開く
htmlfile = './data/sample.html'
with open(htmlfile , encoding='utf-8') as f:
    html = f.read()

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "lxml")

game = Game()

# Game情報の取得
game.time = soup.select_one("div#binding-698").text
game.date = soup.select_one("div#binding-699").text

# Team情報の取得 
game.team1.towers_destroyed = soup.select("div.tower-kills > span")[0].text
game.team2.towers_destroyed = soup.select("div.tower-kills > span")[1].text

game.team1.inhibitors_destroyed = soup.select("div.inhibitor-kills > span")[0].text
game.team2.inhibitors_destroyed = soup.select("div.inhibitor-kills > span")[1].text

game.team1.barons_slain = soup.select("div.baron-kills > span")[0].text
game.team2.barons_slain = soup.select("div.baron-kills > span")[1].text

game.team1.dragons_slain = soup.select("div.dragon-kills > span")[0].text
game.team2.dragons_slain = soup.select("div.dragon-kills > span")[1].text

game.team1.rift_heralds_slain = soup.select("div.rift-herald-kills > span")[0].text
game.team2.rift_heralds_slain = soup.select("div.rift-herald-kills > span")[1].text

div_bans = soup.select("div.bans > div.champion-nameplate > div > div > div")
game.team1.ban1 = div_bans[0].attrs["data-rg-id"]
game.team1.ban2 = div_bans[1].attrs["data-rg-id"]
game.team1.ban3 = div_bans[2].attrs["data-rg-id"]
game.team1.ban4 = div_bans[3].attrs["data-rg-id"]
game.team1.ban5 = div_bans[4].attrs["data-rg-id"]
game.team2.ban1 = div_bans[5].attrs["data-rg-id"]
game.team2.ban2 = div_bans[6].attrs["data-rg-id"]
game.team2.ban3 = div_bans[7].attrs["data-rg-id"]
game.team2.ban4 = div_bans[8].attrs["data-rg-id"]
game.team2.ban5 = div_bans[9].attrs["data-rg-id"]

game.team1.game_result = soup.select("div.game-conclusion")[0].text.strip()
game.team2.game_result = soup.select("div.game-conclusion")[1].text.strip()

# プレイヤー情報
div_names = soup.select("div.champion-nameplate-name > div > span")
game.team1.player1.name = div_names[0].text
game.team1.player2.name = div_names[1].text
game.team1.player3.name = div_names[2].text
game.team1.player4.name = div_names[3].text
game.team1.player5.name = div_names[4].text
game.team2.player1.name = div_names[5].text
game.team2.player2.name = div_names[6].text
game.team2.player3.name = div_names[7].text
game.team2.player4.name = div_names[8].text
game.team2.player5.name = div_names[9].text

div_champs = soup.select("div.player > div.champion-col > div > div.champion-nameplate > div > div > div")
game.team1.player1.champion = div_champs[0].attrs["data-rg-id"]
game.team1.player2.champion = div_champs[1].attrs["data-rg-id"]
game.team1.player3.champion = div_champs[2].attrs["data-rg-id"]
game.team1.player4.champion = div_champs[3].attrs["data-rg-id"]
game.team1.player5.champion = div_champs[4].attrs["data-rg-id"]
game.team2.player1.champion = div_champs[5].attrs["data-rg-id"]
game.team2.player2.champion = div_champs[6].attrs["data-rg-id"]
game.team2.player3.champion = div_champs[7].attrs["data-rg-id"]
game.team2.player4.champion = div_champs[8].attrs["data-rg-id"]
game.team2.player5.champion = div_champs[9].attrs["data-rg-id"]

game.team1.player1.role = "top"
game.team1.player2.role = "jg"
game.team1.player3.role = "mid"
game.team1.player4.role = "adc"
game.team1.player5.role = "sup"
game.team2.player1.role = "top"
game.team2.player2.role = "jg"
game.team2.player3.role = "mid"
game.team2.player4.role = "adc"
game.team2.player5.role = "sup"


# プレイヤーの詳細statsを登録する
# tr.grid-rowが選手ごとの情報を格納している形式ぽい
rows = soup.select("tbody#stats-body > tr.grid-row")
for row in rows:

    # 項目(div.viewで項目を表示しているぽい)
    key = row.find("div", class_="view").string.replace("\n","")

    # 値(div.grid-cellで値を表示しているぽい)
    value = row.find_all("div", class_="grid-cell")

    # player classのdictにいれる
    # TODO: プレイヤーごとに書かないような感じにしたい
    game.team1.player1.set_stats(key, value[0].string.replace("\n",""))
    game.team1.player2.set_stats(key, value[1].string.replace("\n",""))
    game.team1.player3.set_stats(key, value[2].string.replace("\n",""))
    game.team1.player4.set_stats(key, value[3].string.replace("\n",""))
    game.team1.player5.set_stats(key, value[4].string.replace("\n",""))
    game.team2.player1.set_stats(key, value[5].string.replace("\n",""))
    game.team2.player2.set_stats(key, value[6].string.replace("\n",""))
    game.team2.player3.set_stats(key, value[7].string.replace("\n",""))
    game.team2.player4.set_stats(key, value[8].string.replace("\n",""))
    game.team2.player5.set_stats(key, value[9].string.replace("\n",""))


# CSV出力
output_file = "LJL-stats.csv"
with open( output_file, "w", newline="") as f:
    csv_g = game.to_csv()
    writer = csv.DictWriter(f, csv_g[0].keys())
    writer.writeheader()
    writer.writerows(csv_g)
f.close()

