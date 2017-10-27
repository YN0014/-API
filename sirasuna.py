import urllib.request  # HTML取得
import codecs  # 文字コード変換
import re  # 正規表現
import datetime  # 日時取得


def html_get():
    # URL指定 - htmlダウンロード
    url = "http://shirasunaryou.sakura.ne.jp/cgi-bin/shirasuna/kondate/index.cgi?display=sp"
    title = "kondate_html.txt"
    urllib.request.urlretrieve(url, "{0}".format(title))
    kondate_get()


def kondate_get():
    # 献立を格納するリスト
    kondate = []

    # ファイルを開く
    # kondate_htmlは文字コードをShift_JISに変換
    f = codecs.open('kondate_html.txt', 'r', 'shift_jis')
    file_1 = open('kondate_1.txt', 'w')
    file_2 = open('kondate_2.txt', 'w')
    file_3 = open('kondate_3.txt', 'w')
    file_4 = open('kondate_4.txt', 'w')
    file_5 = open('kondate_5.txt', 'w')

    # 献立のみ取り出し & タグ除去
    file_line = f.readlines()
    for line in file_line:
        if not line[0] == "<":
            line = line.replace("<br>", "")
            kondate.append(" " + line)
        if line[0:4] == "<h2>":
            line = line.replace("<h2>", "")
            line = line.replace("</h2>", "")
            kondate.append(line)
        if line[0:4] == "<h4>":
            line = line.replace("<h4>", "")
            line = line.replace("</h4>", "")
            line = "\n" + line
            kondate.append(line)

    # 日時取得
    today = datetime.datetime.today()

    # 献立をそれぞれ別ファイルに書き込み
    flag = 0
    for line in kondate:
        tmp = str(today.month) + "/" + str(today.day + flag)
        if tmp in line:
            flag += 1
        if flag == 0:
            continue
        if flag == 1:
            file_1.write(line)
        elif flag == 2:
            file_2.write(line)
        elif flag == 3:
            file_3.write(line)
        elif flag == 4:
            file_4.write(line)
        elif flag == 5:
            file_5.write(line)

    # ファイルを閉じる
    f.close()
    file_1.close()
    file_2.close()
    file_3.close()
    file_4.close()
    file_5.close()


if __name__ == "__main__":
    # 献立更新関数
    # [html_get]はサーバーにアクセスするための関数.必要な時以外は実行しない
    html_get()
    # [kondate_get]はファイルを処理する関数.何度実行してもOK
    kondate_get()
    # tweet()
