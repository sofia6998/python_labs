"""
Вход: файл guess.txt содержащий имена для угадывания
(например из http://www.biographyonline.net/people/famous-100.html можно взять имена)
Написать игру "Угадай по фото"
3 уровня сложности:
1) используются имена только 1-10
2) имена 1-50
3) имена 1-100
- из используемых имен случайно выбрать одно
- запустить поиск картинок в Google по выбранному
- получить ~30-50 первых ссылок на найденные по имени изображения
- выбрать случайно картинку и показать ее пользователю для угадывания
  (можно выбрать из выпадающего списка вариантов имен)
- после выбора сказать Правильно или Нет
п.с. сделать серверную часть, т.е. клиент играет в обычном браузере обращаясь к веб-серверу.
п.с. для поиска картинок желательно эмулировать обычный пользовательский запрос к Google
или можно использовать и Google image search API
https://ajax.googleapis.com/ajax/services/search/images? или др. варианты
НО в случае API нужно предусмотреть существующие ограничения по кол-ву запросов
т.е. кешировать информацию на случай исчерпания кол-ва разрешенных (бесплатных)
запросов или другим образом обходить ограничение. Т.е. игра не должна прерываться после N запросов (ограничение API)
п.с. желательно "сбалансировать" параметры поиска (например искать только лица,
использовать только первые 1-30 найденных и т.п.)
для минимизации того что найденная картинка не соответствует имени
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse
import json

import feedparser

my_list = {}


class Reader:
    def __init__(self, name, url, lang='ru'):
        self.lang = lang
        self.rss_path = url
        self.title = name

    def get_feed(self):
        d = feedparser.parse(self.rss_path)
        return d['entries']

    def read(self, offset=0, limit=5):
        f = self.get_feed()
        print(f[0].keys())
        result = []
        for i, item in enumerate(f):
            if int(offset) <= i < int(limit) + int(offset):
                real_number = (i + 1)
                result.append({'name': item['title'], 'url': item['link']})

        return result

class HTTPServerQuiz(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        print('do get')
        params = parse_qs(urlparse(self.path).query)

        print(params)
        if 'event' not in params:
            # do not act
            return

        event = params['event'][0]

        if event == 'add':
            self.add_rss(params)
            return
        elif event == 'getlist':
            self.get_list()
            return
        elif event == 'getarticles':
            self.get_articles(params)
            return

        return

    def get_articles(self, params):
        global my_list
        if 'name' not in params:
            self.send_message({'error': 'already exist'})
            return
        name = params['name'][0]
        if name not in my_list:
            self.send_message({'error': 'no such list'})
            return

        offset = params['offset'][0]
        limit = params['limit'][0]
        self.send_message(my_list[name].read(offset, limit))
        return

    def get_list(self):
        print('get list')
        self.send_message(list(my_list.keys()))
        print('get list')
        return

    def add_rss(self, params):
        name = params['name'][0]
        url = params['url'][0]
        if name in my_list:
            self.send_message({'error': 'already exist'})
            return

        reader = Reader(name, url)
        my_list[name] = reader
        self.send_message(list(my_list.keys()))
        return

    def send_message(self, response):
        print('resp')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), encoding='utf-8'))
        return


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8086)
    httpd = HTTPServer(server_address, HTTPServerQuiz)

    httpd.serve_forever()