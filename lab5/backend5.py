import sys
import json
import random

from urllib.request import Request, urlopen
from lxml import html

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse

from serverparams import LEVELS_TO_NUM_VARIANTS, COUNT_ANSWERS

# This function is created for generating names
# def init_names():
#     req = Request(
#         "https://www.biographyonline.net/people/famous-100.html",
#         headers={'User-Agent': 'Mozilla/5.0'})
#     html_content = urlopen(req).read()
#
#     tree = html.fromstring(html_content)
#
#     name = []
#     for i in range(1, 100):
#         name.append(tree.xpath('(.//*[@class=\'post-content clearfix\']/ol/li)[' + str(i) + ']/a/text()'))
#     return name


def get_names_list_from_file(filename):
    file = open(filename, "r")
    lines_in_file = file.readlines()

    names = []
    for name in lines_in_file:
        names.append(name)

    return names


def generate_answers(names_list, count_variants):
    generated_answers = []
    index = 0
    while index < count_variants:
        answer = names_list[random.randint(0, len(names_list) - 1)]
        formatted_answer = answer.split('\n')[0]
        if formatted_answer not in generated_answers:
            generated_answers.append(formatted_answer)
            index += 1

    correct_answer = generated_answers[
        random.randint(0, len(generated_answers) - 1)
    ]

    return generated_answers, correct_answer


def get_photo_for_correct_answer(name):
    url = "https://www.google.ru/search?site=&tbm=isch&source=hp&biw=1600&bih=1600&q=" + (name + ' png').replace(" ", "%20")

    #url = "https://pokemondb.net/pokedex/national"
    req = Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'})
    html_content = urlopen(req).read()

    tree = html.fromstring(html_content)

    import random
    #path = ".//a[@href='/pokedex/" + name.lower() + "'" + ']/img/@src'
    return tree.xpath('(.//*[@target="_blank"]/img)[' + str(random.randint(1, 10)) + ']/@src')

class QuizServer(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        names = get_names_list_from_file(filename=sys.argv[1])

        params = parse_qs(urlparse(self.path).query)
        if 'level' not in params:
            # do not any action
            return

        level = params['level'][0]
        if level in LEVELS_TO_NUM_VARIANTS:
            num_variants = LEVELS_TO_NUM_VARIANTS[level]
        else:
            num_variants = LEVELS_TO_NUM_VARIANTS[1]

        answer_variants, correct_answer = generate_answers(
            names_list=names,
            count_variants=num_variants
        )

        photo_for_answer = get_photo_for_correct_answer(name=correct_answer)[0]
        print(photo_for_answer)
        print(correct_answer + ' - ' + photo_for_answer)

        response = {
            'photo': photo_for_answer,
            'answer': correct_answer,
            'variants': answer_variants
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), encoding='utf-8'))


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8085)
    http_server = HTTPServer(server_address, QuizServer)
    http_server.serve_forever()