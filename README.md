# lol-stats

====

Download the League of Legend's match-history and parse to csv.

## Description
You can analyze the LoL Game from match-history.

LJLのスタッツをまとめたいと思いましたが、LJLの試合はRiot APIで情報を取得することができないので、Match-historyから情報を取得するために作りました。

## Demo
- Input
  - LJL-stats.csv
- Output
```
name,champion,role,kill,death,assist,cs,KDA,Largest Killing Spree,Largest Multi Kill,First Blood,Total Damage to Champions,Physical Damage to Champions,Magic Damage to Champions,True Damage to Champions,Total Damage Dealt,Physical Damage Dealt,Magic Damage Dealt,True Damage Dealt,Largest Critical Strike,Total Damage to Objectives,Total Damage to Turrets,Damage Healed,Damage Taken,Physical Damage Taken,Magic Damage Taken,True Damage Taken,Wards Placed,Wards Destroyed,Stealth Wards Purchased,Control Wards Purchased,Gold Earned,Gold Spent,Minions Killed,Neutral Minions Killed,Neutral Minions Killed in Team's Jungle                                      ,Neutral Minions Killed in Enemy Jungle                                      ,game_result,towers_destroyed,inhibitors_destroyed,barons_slain,dragons_slain,rift_heralds_slain,ban1,ban2,ban3,ban4,ban5,date,time
SG Reiya,Urgot,top,5,1,6,0,11.0,5,2,0,14900.0,12300.0,100.0,2500.0,303800.0,267100.0,100.0,36700.0,0,26800.0,9000.0,1600.0,17500.0,8700.0,8500.0,300.0,22,14,0,9,17400.0,16200.0,323,20,5,4,VICTORY,11,3,1,3,0,Irelia,Galio,Sejuani,Akali,Sion,1/19/2019,39:32
SG Smile,Gragas,jg,1,2,9,0,5.0,1,1,0,6600.0,600.0,5000.0,1000.0,118200.0,22100.0,87700.0,8400.0,0,11300.0,200.0,11900.0,23600.0,16100.000000000002,6500.0,1000.0,18,10,0,15,11000.0,10100.0,21,117,78,12,VICTORY,11,3,1,3,0,Irelia,Galio,Sejuani,Akali,Sion,1/19/2019,39:32
SG Taka,Syndra,mid,6,0,3,0,9,6,3,0,13800.0,500.0,12900.0,300.0,280400.0,16700.0,258100.00000000003,5600.0,0,11400.0,3700.0,1900.0,9000.0,4400.0,4500.0,100.0,25,9,0,15,17100.0,15200.0,331,29,29,0,VICTORY,11,3,1,3,0,Irelia,Galio,Sejuani,Akali,Sion,1/19/2019,39:32
SG OdduGi,Caitlyn,adc,6,1,8,0,14.0,4,1,0,19700.0,16900.0,800.0,2000.0,344000.0,324000.0,7500.0,12500.0,1964,32700.000000000004,8400.0,3600.0,12800.0,8600.0,4200.0,0.0,10,26,0,3,19300.0,17700.0,349,46,27,4,VICTORY,11,3,1,3,0,Irelia,Galio,Sejuani,Akali,Sion,1/19/2019,39:32
SG Raina,Morgana,sup,0,5,11,0,2.2,0,0,0,6200.0,200.0,5400.0,700.0,18400.0,5000.0,12700.0,700.0,0,2000.0,200.0,1000.0,12600.0,6200.0,6100.0,400.0,65,22,0,19,9900.0,8800.0,31,0,0,0,VICTORY,11,3,1,3,0,Irelia,Galio,Sejuani,Akali,Sion,1/19/2019,39:32
AXZ uinyan,Kennen,top,4,4,0,0,1.0,2,2,1,14400.0,1000.0,13400.0,0.0,209700.0,34200.0,168900.0,6700.0,0,2900.0,2100.0,3200.0,20700.0,13600.0,5200.0,1900.0,24,7,0,12,15000.0,13600.0,317,15,13,0,DEFEAT,3,0,0,3,1,Cassiopeia,Lucian,Aatrox,XinZhao,LeeSin,1/19/2019,39:32
AXZ iSeNN,Khazix,jg,3,6,4,0,1.1666666666666667,2,1,0,9600.0,8200.0,1100.0,400.0,195600.0,168300.0,10900.0,16400.0,0,36800.0,500.0,18800.0,36300.0,27500.0,6800.0,2000.0,33,11,0,11,11800.0,10900.0,13,171,127,0,DEFEAT,3,0,0,3,1,Cassiopeia,Lucian,Aatrox,XinZhao,LeeSin,1/19/2019,39:32
AXZ Gariaru,Lissandra,mid,0,4,3,0,0.75,0,0,0,5800.0,300.0,5400.0,0.0,245500.0,19000.0,208900.0,17600.0,0,1500.0,900.0,1700.0,16200.0,7300.0,8200.0,700.0,18,18,0,14,13700.0,14200.0,336,12,8,0,DEFEAT,3,0,0,3,1,Cassiopeia,Lucian,Aatrox,XinZhao,LeeSin,1/19/2019,39:32
AXZ NoA,Ezreal,adc,2,1,2,0,4.0,2,1,0,17700.0,11800.0,5400.0,600.0,309800.0,258100.00000000003,25900.0,25700.0,0,7900.0,3700.0,1700.0,16300.0,12000.0,3800.0,500.0,14,5,0,5,16100.000000000002,16500.0,365,16,12,0,DEFEAT,3,0,0,3,1,Cassiopeia,Lucian,Aatrox,XinZhao,LeeSin,1/19/2019,39:32
AXZ ThintoN,Rakan,sup,0,3,5,0,1.6666666666666667,0,0,0,2300.0,0.0,1400.0,800.0,12000.0,7100.0,3100.0,1800.0,0,1400.0,500.0,2300.0,10900.0,6600.0,2900.0,1300.0,75,27,0,23,8400.0,8000.0,30,0,0,0,DEFEAT,3,0,0,3,1,Cassiopeia,Lucian,Aatrox,XinZhao,LeeSin,1/19/2019,39:32
```

## VS. 
Riot API 

## Requirement
None

## Usage
1. Create [url_list.csv]
2. Run download-matches.py
3. Run get-lolstats.py

## Install

## Contribution

## Licence

## Author
[potof]
