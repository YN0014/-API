import falcon
import json
import datetime
from sirasuna import html_get
import datetime


def fileRead(req_day):
    for count in range(2):
        fp = open('kondate_1.txt')
        f = fp.read()
        f = f.split('\n')
        line = f[0]
        line = line.split()
        line = line[0]
        line = line.split('/')
        today = datetime.datetime.today()
        if not int(line[0]) == today.month or not int(line[1]) == today.day:
            if count == 0:
                html_get()
                count = 1
            elif count == 1:
                return 1
        fp.close()

    fp = open('kondate_' + str(req_day + 1) + '.txt')
    f = fp.read()
    f = f.split('\n')
    kondate_list = [[], [], []]
    category = 0
    for line in f:
        if(line == "朝食"):
            category = 1
            continue
        elif(line == "昼食"):
            category = 2
            continue
        elif(line == "夕食"):
            category = 3
            continue
        if category == 0:
            continue

        kondate_list[category - 1].append(line)

    for idx in range(3):
        kondate_list[idx] = list(
            map(lambda x: x.replace(' ', ''), kondate_list[idx]))
        kondate_list[idx] = list(
            map(lambda x: x.replace('　', ' '), kondate_list[idx]))

    fp.close()
    return kondate_list


class ItemsResource:
    def on_get(self, req, resp, isbn):
        params = req.params
        if "day" in params:
            try:
                value = int(params["day"])
            except ValueError:
                isbn = 'error'
                value = 0
        else:
            value = 0
        if value < 0 or value > 4:
            value = 0
        kondate_list = fileRead(value)
        if kondate_list == 1:
            isbn = "notfound"
        today = datetime.datetime.today()
        today += datetime.timedelta(days=value)
        month = int(today.month)
        day = int(today.day)

        items = {}
        if isbn == "breakfast":
            items = {
                'code': 0,
                'title': '朝食',
                'date': str(month) + '/' + str(day),
                'menu': kondate_list[0][:]
            }
        elif isbn == "lunch":
            items = {
                'code': 0,
                'title': '昼食',
                'date': str(month) + '/' + str(day),
                'menu': kondate_list[1][:]
            }
        elif isbn == "dinner":
            items = {
                'code': 0,
                'title': '夕食',
                'date': str(month) + '/' + str(day),
                'menu': kondate_list[2][:]
            }
        elif isbn == "all":
            items = {
                'code': 0,
                'title': 'All',
                'date': str(month) + '/' + str(day),
                'menu': {
                    'breakfast': kondate_list[0][:],
                    'lunch': kondate_list[1][:],
                    'dinner': kondate_list[2][:]
                }
            }
        elif isbn == "notfound":
            items = {
                'code': 1,
                'errors': {
                    'message': "最新の情報が取得できませんでした"
                }
            }
        elif isbn == "error":
            items = {
                'code': 2,
                'errors': {
                    'message': "サーバ内部でエラーが発生しました"
                }
            }
        else:
            items = {
                'code': 3,
                'errors': {
                    'message': "指定されたURLは見つかりませんでした"
                }
            }

        resp.body = json.dumps(items, ensure_ascii=False)


api = falcon.API()
api.add_route('/sirasuna_kondateAPI/{isbn}', ItemsResource())

if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server("127.0.0.1", 8000, api)
    httpd.serve_forever()
