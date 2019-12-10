import requests
from flask import Flask, render_template
from flask import Blueprint

from keys import KAKAO_ADMIN_KEY
from rest_client import read_kakao
from rest_client.read_kakao import KAKAO_BASE_URL
from views.auth import kakao_oauth

headers = {"Authorization": 'KakaoAK ' + KAKAO_ADMIN_KEY}
app = Flask(__name__)

menus_blueprint = Blueprint('menus', __name__)


@menus_blueprint.route('/main')
def menus_main():
    return 'welcome news {0}'.format("Hkt")


@menus_blueprint.route('/sports')
def menus_sports():
    return 'welcome sports news {0}'.format("Hkt")


@menus_blueprint.route('/science')
def menus_science():
    return 'welcome science news {0}'.format("Hkt")


@menus_blueprint.route('/images')
def images():
    res1 = requests.get(
        url=KAKAO_BASE_URL + "/v2/search/image?query=아이유",
        headers=headers
    )
    if res1.status_code == 200:
        images = res1.json()

        for image in images['documents']:
            print("{0}".format(image['image_url']))
    else:
        print("Error {0} ".format(res1.status_code))

    return render_template(
        'images.html', image=images, nav_menu="image" ,kakao_oauth=kakao_oauth
    )


@menus_blueprint.route('/books')
def books():

    res1 = requests.get(
        url=KAKAO_BASE_URL + "/v3/search/book?target=authors&query=정태윤",
        headers=headers
    )
    if res1.status_code == 200:
        books = res1.json()

        for book in books['documents']:
            print("{0:50s} - {1:>20s}".format(book['title'] ,str(book['authors'])))
    else:
        print("Error {0} ".format(res1.status_code))

    return render_template(
        'books.html', books=books['documents'], nav_menu="book" , kakao_oauth=kakao_oauth
    )
