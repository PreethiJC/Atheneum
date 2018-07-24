import requests
import html
from flask import request
from flask_paginate import Pagination, get_page_parameter
from bs4 import BeautifulSoup

class Helpers:
    def get_pagination(self, cursor):
        search = False
        q = request.args.get('q')
        if q:
            search = True
        page = request.args.get(get_page_parameter(), type=int, default=1)
        raw_pagination = Pagination(page=page, total=cursor.count(), search=search, record_name='books')
        pagination = self.fix_pagination(raw_pagination.links)
        return pagination

    def get_list_details(self, book_list):
        details = []
        sessions = []
        for book in book_list:
            res = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + book['topic']
                               + ":inauthor:" + book['author'], verify=False)
            data = res.json()
            authors = ', '.join(data['items'][0]['volumeInfo']['authors'])
            selflink = data['items'][0]['selfLink']
            info_dict = {"id": book['_id'],
                         "topic": book['topic'],
                         "author": authors,
                         "snippet": html.unescape(data['items'][0]['searchInfo']['textSnippet']),
                         "image": self.get_image(selflink),
                         "gblink": selflink
                         }
            session_dict = {
                "id": book['_id'],
                "topic": book['topic'],
                "author": authors,
                "image": self.get_image(selflink),
                "gblink": selflink,
                "download_link": book['link']
            }
            sessions.append(session_dict)
            details.append(info_dict)
        return details, sessions

    def get_book_details(self, book_detail):
        res = requests.get(book_detail['gblink'], verify=False)
        data = res.json()
        info_dict = {
            "id": book_detail['id'],
            "topic": book_detail['topic'],
            "author": book_detail['author'],
            "image": book_detail['image'],
            "description": data['volumeInfo']['description'],
            "download_link": book_detail['download_link'],
            "genres": data['volumeInfo']['categories']
        }
        if "averageRating" in data['volumeInfo']:
            info_dict["rating"] = data['volumeInfo']['averageRating']
        else:
            info_dict["rating"] = "N/A"

        return info_dict

    def get_description(self, url):
        res = requests.get(url, verify=False)
        data = res.json()
        return data['volumeInfo']['description']

    def get_image(self, url):
        res = requests.get(url, verify=False)
        data = res.json()
        try:
            return data['volumeInfo']['imageLinks']['small']
        except:
            return data['volumeInfo']['imageLinks']['thumbnail']

    def fix_pagination(self, pagination):
        soup = BeautifulSoup(pagination, 'html.parser')
        ul_search = soup.find('ul')
        ul_search['class'] = 'pagination'
        div_search = soup.find('div', class_='pagination')
        div_search['class'] = 'row text-center'
        return div_search


