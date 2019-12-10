from flask import Blueprint, redirect, render_template, request, flash, session
import pprint

from database import base
from database.base import User
from forms import UserForm, LoginForm, MyPageUserForm
from flask_login import login_required, login_user, logout_user, current_user
import requests

from keys import KAKAO_REST_API_KEY

auth_blueprint = Blueprint('auth', __name__)

kakao_oauth = {}

@auth_blueprint.route('/my_page', methods=['GET', 'POST'])
@login_required
def _user():
    form = MyPageUserForm()

    q = base.db_session.query(User).filter(User.email == current_user.email)
    user = q.first()

    if request.method == 'POST':
        if form.validate_on_submit():
            user.email = request.form['email']
            user.name = request.form['name']
            user.set_password(request.form['password'])
            user.affiliation = request.form['affiliation']
            base.db_session.commit()
            flash('귀하의 회원정보가 수정 되었습니다.')
            return redirect('/auth/my_page')

    return render_template("my_page.html", user=user, form=form, kakao_oauth=kakao_oauth)


def login_process(email, password):
    q = base.db_session.query(User).filter(User.email == email)
    user = q.first()

    if user:
        if user.authenticate(password):
            login_result = login_user(user)
            if login_result:
                print("사용자(사용자 이메일:{0})의 로그인 성공!".format(current_user.email))
            return '/'
        else:
            flash('비밀번호를 다시 확인하여 입력해주세요.')
            return '/auth/login'
    else:
        flash('이메일 및 비밀번호를 다시 확인하여 입력해주세요.')
        return '/auth/login'


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            redirect_url = login_process(form.data['email'], form.data['password'])
            return redirect(redirect_url)

    return render_template('login.html', form=form, current_user=current_user, KAKAO_REST_API_KEY=KAKAO_REST_API_KEY, kakao_oauth=kakao_oauth)


@auth_blueprint.route('kakao_oauth_redirect')
def kakao_oauth_redirect():
    code = str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    data = "grant_type=authorization_code" \
           "&client_id={0}&redirect_uri=http://localhost:8080/auth/kakao_oauth_redirect&code={1}" \
        .format(KAKAO_REST_API_KEY, code)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Cache-Control": "no-cache"
    }
    response = requests.post(
        url=url,
        data=data,
        headers=headers
    )

    pprint.pprint(response.json())

    kakao_oauth["access_token"] = response.json()["access_token"]
    kakao_oauth["expires_in"] = response.json()["expires_in"]
    kakao_oauth["refresh_token"] = response.json()["refresh_token"]
    kakao_oauth["refresh_token_expires_in"] = response.json()["refresh_token_expires_in"]
    kakao_oauth["scope"] = response.json()["scope"]
    kakao_oauth["token_type"] = response.json()["token_type"]

    if "kaccount_email" not in kakao_oauth or kakao_oauth['kaccount_email'] is None:
        kakao_me_and_signup()

    redirect_url = login_process(kakao_oauth["kaccount_email"], "1234")
    return redirect(redirect_url)


def kakao_me_and_signup():
    url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": "Bearer {0}".format(kakao_oauth["access_token"]),
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    response = requests.post(
        url=url,
        headers=headers
    )

    pprint.pprint(response.json())

    kakao_oauth["kaccount_email"] = response.json()["kakao_account"]["email"]
    kakao_oauth["id"] = response.json()["id"]
    kakao_oauth["kakao_profile_image"] = response.json()["properties"]["profile_image"]
    kakao_oauth["nickname"] = response.json()["properties"]["nickname"]
    kakao_oauth["kakao_thumbnail_image"] = response.json()["properties"]["thumbnail_image"]

    c = base.db_session.query(User).filter(User.email == kakao_oauth["kaccount_email"]).count()
    if c == 0:
        user = User(name=kakao_oauth["nickname"], email=kakao_oauth["kaccount_email"], affiliation=None)
        user.set_password("1234")
        base.db_session.add(user)
        base.db_session.commit()


def kakao_logout():
    url = "https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Authorization": "Bearer {0}".format(kakao_oauth["access_token"])
    }
    response = requests.post(
        url=url,
        headers=headers
    )

    if response.status_code == 200:
        kakao_oauth["kaccount_email"] = None
        kakao_oauth["id"] = None
        kakao_oauth["kakao_profile_image"] = None
        kakao_oauth["nickname"] = None
        kakao_oauth["kakao_thumbnail_image"] = None


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    if kakao_oauth and "kaccount_email" in kakao_oauth:
        kakao_logout()

    return redirect('/')


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            new_user.email = request.form['email']
            new_user.name = request.form['name']
            new_user.set_password(request.form['password'])
            new_user.affiliation = request.form['affiliation']

            base.db_session.add(new_user)
            base.db_session.commit()
            flash('귀하는 회원가입이 성공적으로 완료되었습니다. 가입하신 정보로 로그인을 다시 하시기 바랍니다.')
            return redirect('/auth/login')

    return render_template("signup.html", form=form)