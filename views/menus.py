import requests
from flask import Flask, render_template, request
from flask import Blueprint

from keys import KAKAO_ADMIN_KEY, TRAVEL_KEY
from rest_client import read_kakao
from rest_client.read_kakao import KAKAO_BASE_URL
from views.auth import kakao_oauth
from whatdo import whatdo

BASE_URL = "http://api.visitkorea.or.kr/openapi/service/rest/KorService"
PARAM = "&listYN=Y&arrange=A&MobileOS=ETC&MobileApp=AppTest&_type=json"
TRAVEL_BASE_URL = "http://apis.data.go.kr/B553077/api/open/sdsc/baroApi?resId=dong&catId=cty&ctprvnCd="
TRAVEL_URL = "&ServiceKey=" + TRAVEL_KEY + "&type=json"
BUSINESS_URL = "http://apis.data.go.kr/B553077/api/open/sdsc/storeListInDong?divId=signguCd&key="

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


@menus_blueprint.route('/images', methods=['POST', 'GET'])
def images():
    if request.method == 'POST':
        squery = request.form['image']
        res1 = requests.get(
            url=KAKAO_BASE_URL + "/v2/search/image?query=" + squery,
            headers=headers
        )
        if res1.status_code == 200:
            images = res1.json()

            for image in images['documents']:
                print("{0}".format(image['image_url']))
        else:
            print("Error {0} ".format(res1.status_code))

    else:
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
        'images.html', image=images, nav_menu="image", kakao_oauth=kakao_oauth,
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
            print("{0:50s} - {1:>20s}".format(book['title'], str(book['authors'])))
    else:
        print("Error {0} ".format(res1.status_code))

    return render_template(
        'books.html', books=books['documents'], nav_menu="book", kakao_oauth=kakao_oauth
    )


@menus_blueprint.route('/travel', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        KEYWORD = request.form['travel']
        res = requests.get(
            url=BASE_URL + "/searchKeyword?ServiceKey=" + TRAVEL_KEY + "&keyword=" + KEYWORD + PARAM
        )

        z={}
        v={}
        i=0
        if res.status_code == 200:
            travels = res.json()

            for travel in travels["response"]['body']['items']['item']:
                try:
                    w = travel['addr1']
                except KeyError:
                    w = '서울특별시 모르군 모르동'
                    print("error")
                #print(w.split(' ')[0] + " " + w.split(' ')[1] + "의 관광지")
                do = w.split(' ')[0]
                # print(do)
                ADDRESS_CODE = str(whatdo(do))
                # print("{0}의 지역코드 = {1}".format(do,ADDRESS_CODE))
                #try:
                #    print("제목 : {0}, 주소 : {1}, 사진 : {2}".format(travel['title'], travel['addr1'], travel['firstimage']))
                #except KeyError:
                #    print("제목 : {0}, 주소 : {1}, 사진 : 없음".format(travel['title'], travel['addr1']))
                # pprint.pprint("{0}".format(travels))

                print(w.split(' ')[0] + " " + w.split(' ')[1] + w.split(' ')[2] + "의 음식점")

                res1 = requests.get(
                    url=TRAVEL_BASE_URL + ADDRESS_CODE + TRAVEL_URL
                )
                if res1.status_code == 200:
                    address = res1.json()

                    print(address)
                    for addresss in address["body"]['items']:
                        if addresss['signguNm'] == w.split(' ')[1]+' '+w.split(' ')[2]:
                            print("{0}의 지역코드 : {1}".format(w.split(' ')[1] +' '+ w.split(' ')[2], addresss['signguCd']))
                            break
                        if addresss['signguNm'] == w.split(' ')[1]:
                            print(
                                "{0}의 지역코드 : {1}".format(w.split(' ')[1], addresss['signguCd']))
                            break
                        print(" ")

                    print("{0}의 지역코드 : {1}".format(w.split(' ')[1] + w.split(' ')[2] , addresss['signguCd']))
                    res2 = requests.get(
                        url=BUSINESS_URL + addresss['signguCd'] + TRAVEL_URL
                    )

                if res2.status_code == 200:
                    business = res2.json()
                    x = []
                    y = []
                    for businesss in business["body"]['items']:
                        b = businesss
                        # pprint.pprint(b)
                        if b['indsLclsNm'] == '음식':
                            print(b['bizesNm'] + "," + "주소 : " + b['lnoAdr'])
                            # z.append({i:(b['lnoAdr'],b['bizesNm'])})

                            x.append(b['lnoAdr'])
                            y.append(b['bizesNm'])
                            # print("x={0}".format(x))
                            # print("y={0}".format(y))
                    z[i]=y
                    v[i]=x
                    del x,y
                    print(i)
                    i = i + 1


            # print(z)
            # print(v)




    else:
        return '대시보드의 검색을 이용해주세요'

    return render_template("travel.html", nav_menu="travel", travels=travels["response"]['body']['items']['item'],
                           address=address["body"]['items'], business=business["body"]['items'],z=z,v=v)
