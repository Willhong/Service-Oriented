import requests
import pprint
from keys import KAKAO_ADMIN_KEY
KAKAO_BASE_URL = "https://dapi.kakao.com"

if __name__ == "__main__":
    headers ={"Authorization" : 'KakaoAK '+KAKAO_ADMIN_KEY}
    res = requests.get(
        url=KAKAO_BASE_URL+"/v3/search/book?target=title&query=파피용",
        headers = headers
    )
    if res.status_code ==200:
        books = res.json()
        for book in books['documents']:
            # print(book['title']
            print("{0:50s} - {1:>20s}".format(book['title'] ,str(book['authors'])))
    else:
        print("Error {0} ".format(res.status_code))

    res1 = requests.get(
        url=KAKAO_BASE_URL + "/v2/search/image?query=설현",
        headers=headers
    )
    if res.status_code == 200:
        images=res1.json()

        for image in images['documents']:
            print("{0}".format(image['image_url']))
    else:
        print("Error {0} ".format(res1.status_code))


