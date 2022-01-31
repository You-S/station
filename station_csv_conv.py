import sqlite3
import csv

con = sqlite3.connect("stationData.db")
cur = con.cursor()

csv_list = ['station', 'line', 'pref']

for table in csv_list:
    if table == 'station':
        create_test = "CREATE TABLE IF NOT EXISTS station (id INTEGER, stationNo INTEGER, stationUno INTEGER, name TEXT, yomi TEXT,lineid INTEGER, prefNo INTEGER, address TEXT,lon TEXT,lat TEXT)"
        cur.execute(create_test)

        delete_test = "DELETE FROM station"
        cur.execute(delete_test)

        #csvファイルの指定
        open_csv = open("Station_output.csv")

        #csvファイルを読み込む
        read_csv = csv.reader(open_csv)
    
        #csvデータをINSERTする
        rows = []
        for row in read_csv:
            rows.append(row)

        #executemany()で複数のINSERTを実行する
        cur.executemany(
            "INSERT INTO station (id, stationNo, stationUno, name, yomi, lineid, prefNo, address, lon, lat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
        
    elif table == 'line':
        create_test = "CREATE TABLE IF NOT EXISTS line (id INTEGER, lineid INTEGER, linename TEXT, lineCname TEXT)"
        cur.execute(create_test)

        delete_test = "DELETE FROM line"
        cur.execute(delete_test)

        open_csv = open("Line_output.csv")
        read_csv = csv.reader(open_csv)
    
        rows = []
        for row in read_csv:
            rows.append(row)

        cur.executemany(
            "INSERT INTO line (id, lineid, linename, lineCname) VALUES (?, ?, ?, ?)", rows)
        
    elif table == 'pref':
        create_test = "CREATE TABLE IF NOT EXISTS pref (id INTEGER, prefname TEXT)"
        cur.execute(create_test)

        delete_test = "DELETE FROM pref"
        cur.execute(delete_test)

        open_csv = open("Pref.csv")
        read_csv = csv.reader(open_csv)
    
        rows = []
        for row in read_csv:
            rows.append(row)

        cur.executemany(
            "INSERT INTO pref (id, prefname) VALUES (?, ?)", rows)

    #テーブルの変更内容保存
    con.commit()
    open_csv.close()

#データベースの接続終了
con.close