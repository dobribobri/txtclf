#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import regex as re


class Insta_Data_Scraper:
    def __init__(self):
        self.sentences = []
        self.tags = []

    def getdata(self, url):
        try:
            html = urllib.request.urlopen(url, context=self.ctx, timeout=666).read()
        except urllib.error.HTTPError:
            return
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        # print ('Scraping links with #' + hashtag+"...........")               # скрапим ссылки на изображения
        # for post in data['entry_data']['TagPage'][0]['graphql'
        #         ]['hashtag']['edge_hashtag_to_media']['edges']:
        #     image_src = post['node']['thumbnail_resources'][1]['src']
        #     hs = open(hashtag + '.txt', 'a')
        #     hs.write(image_src + '\n')
        #     hs.close()
        for i, post in enumerate(data['entry_data']['TagPage'][0]['graphql']
                              ['hashtag']['edge_hashtag_to_media']['edges']):
                                            # как вариант 'edge_hashtag_to_top_posts'
            try:
                text = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
            except IndexError:
                continue
            text = re.sub(r'[^а-яА-ЯёЁ#\s\n\.]', '', text)     # удалим из строки всё ненужное
            text = re.sub(r'#{1}[\s$]', '', text)              # удалим из строки одиночные вхождения решётки '#_',
                                                     # после которой идёт пробельный символ или символ конца строки
            text = re.sub(r'#{2,}', '', text)                                    # удалим 'поезда' из решёток
            if text == '':
                continue
            text = re.sub('#', ' #', text)  # на случай слитного написания хештегов, добавим лишний пробел перед '#'
            post_tags = re.findall('#{1}[а-яА-ЯёЁ]+', text)                      # найдём все хештеги
            post_tags = [t.lower() for t in post_tags]                           # маленькие буквы
            post_sentences = [s for s in re.split(r'[\n\.]', text) if s != '']   # выделим предложения
            post_sentences = [re.sub(r'[\s]+', ' ', s) for s in post_sentences]  # проставим нормальные пробелы
            post_sentences = [re.sub('^[ ]', '', s) for s in post_sentences]     # если пробел идёт в начале строки,
                                                     # то его необходимо удалить
            if len(post_sentences) > 1:
                post_sentences[-1] = re.sub('#{1}$', '', post_sentences[-1])     # Христу угодно
            post_sentences = [s for s in post_sentences if s != '']              # тоже
            post_sentences = [s.lower() for s in post_sentences]                 # маленькие буквы
            # text = []
            # for s in post_sentences:
            #     if re.search('#{1}[а-яА-ЯёЁ]+', s):
            #         continue # пропустить предложение, если оно содержит хештег
            #     text.append(re.sub('[#]', '', s)) # +очистить от решёток
            # post_sentences = text
            self.sentences.extend(post_sentences)
            self.tags.extend(post_tags)
            # print(i, post_tags, '\n', post_sentences)

    def refresh(self):
        self.tags = list(set(self.tags))
        self.sentences = []

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        for j in range(1, 3):
            print('ITERATION {}'.format(j))
            with open('hashtaglist_iteration{}.txt'.format(j), 'r') as f:
                htlist = f.readline()
            htlist = re.sub('#', '', htlist)
            self.htlist = re.split(' ', htlist)
            self.htlist = [x.strip() for x in self.htlist]
            print(len(self.htlist))
            break
            for hashtag in self.htlist:
                print('https://www.instagram.com/explore/tags/'
                              + hashtag + '/')
                self.getdata('https://www.instagram.com/explore/tags/'
                              + urllib.parse.quote(hashtag) + '/')
                with open('sentences/' + hashtag + '.txt', 'w') as htsf:
                    for sentence in self.sentences:
                        htsf.write(sentence + '\n')
            self.refresh()
            with open('hashtaglist_iteration{}.txt'.format(j+1), 'w') as o:
                for tag in self.tags:
                    o.write(str(tag) + ' ')

        print('done!')


if __name__ == '__main__':
    obj = Insta_Data_Scraper()
    obj.main()

# class Insta_Info_Scraper:
#
#     def getinfo(self, url):
#         html = urllib.request.urlopen(url, context=self.ctx).read()
#         soup = BeautifulSoup(html, 'html.parser')
#         data = soup.find_all('meta', attrs={'property': 'og:description'
#                              })
#         text = data[0].get('content').split()
#         user = '%s %s %s' % (text[-3], text[-2], text[-1])
#         followers = text[0]
#         following = text[2]
#         posts = text[4]
#         print ('User:', user)
#         print ('Followers:', followers)
#         print ('Following:', following)
#         print ('Posts:', posts)
#         print ('---------------------------')
#         print(text)
#
#     def main(self):
#         self.ctx = ssl.create_default_context()
#         self.ctx.check_hostname = False
#         self.ctx.verify_mode = ssl.CERT_NONE
#
#         with open('users.txt') as f:
#             self.content = f.readlines()
#         self.content = [x.strip() for x in self.content]
#         for url in self.content:
#             self.getinfo(url)
#
#
# if __name__ == '__main__':
#     obj = Insta_Info_Scraper()
#     obj.main()