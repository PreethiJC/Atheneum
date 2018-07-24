from app import app
from flask import render_template, session
from pymongo import MongoClient
from app.helpers import Helpers as Helpers


helper = Helpers()


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Preethi'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Eiffel'},
            'body': 'Hello Earth! Greetings from Wolf 359!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/list')
def book_list():
    client = MongoClient("localhost", 27017, maxPoolSize=50)
    db = client.mobilism
    collection = db['children']
    cursor = collection.find().skip(0).limit(6)
    book_list = [x for x in cursor]
    book_details, session_details = helper.get_list_details(book_list[:6])
    pagination = helper.get_pagination(cursor)
    session['details'] = session_details
    return render_template('list.html', title='List', book_list=book_details, pagination=pagination)

@app.route('/details/<id>')
def book_details(id):
    details = session.get('details', None)
    detail = [detail for detail in details if detail['id'] == int(id)]
    info = helper.get_book_details(detail[0])
    return render_template('details.html', title='Details', id=id, info= info)









