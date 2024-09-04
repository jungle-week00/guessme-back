from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient
from flask_jwt_extended import *
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter
import os, uuid

import base64, random, datetime

client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config.update(
    JWT_SECRET_KEY = "TEST"
)

jwt = JWTManager(app)

### Page Container

# Main Page
@app.route('/')
def home():
    # 쿠키에서 JWT 토큰 가져오기
    token = request.cookies.get('access_token')

    name = ''
    profile_image = ''
    logged_in = False
    
    if token:
        # 토큰이 유효한지 확인
        try:
            decoded_token = decode_token(token)
            identity = decoded_token['sub'] # JWT에서 identity 추출
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            logged_in = True
        except Exception as e:
            logged_in = False
    else:
        logged_in = False

    return render_template('index.html', logged_in=logged_in, name=name, profile_image=profile_image)

# Sign In Page
@app.route('/signin')
def signin():
    return render_template('signin.html')

# Signup Page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# 자기소개 입력 페이지
@app.route('/introduce/edit')
def introduceEdit():
    return 'Introduce Edit'

# 자기소개 결과 페이지
@app.route('/introduce/result')
def introudceResult():
    return 'Introduce Result'

# 자기소개 페이지
@app.route('/introduce')
def showIntroduce():
    return 'Introduce Show'



### API

# 회원가입 기능
@app.route('/api/signup', methods=['POST'])
def register():
    # ID
    userID = request.form['id']
    # PW
    userPW = request.form['pw']
    # Profile Image
    userProfile = request.files['profile_image']    
    
    if userProfile.filename == '':
        return jsonify({'result' : 'failed', 'msg' : '현재 이미지가 비어있습니다. '})
    
    # 고유한 파일 이름 생성
    filename = str(uuid.uuid4())
    # origin 이미지와 blur 이미지
    origin_profile_img = f"{filename}_origin.jpg"
    blur_profile_img = f"{filename}_blur.jpg"
    
    # 원본 저장
    origin_path = os.path.join(app.config['UPLOAD_FOLDER'], origin_profile_img)
    userProfile.save(origin_path)
    
    # 이미지 열고 블러 처리
    with Image.open(origin_path) as img:
        
        blurred_img = img.rotate(90)
        blurred_img = img.filter(ImageFilter.GaussianBlur(50))
        
        # 블러 이미지 저장
        blurred_path = os.path.join(app.config['UPLOAD_FOLDER'], blur_profile_img)
        blurred_img.save(blurred_path)
    
    # nickname
    userNickname = request.form['nickname']
    
    # DB에서 입력받은 ID와 동일한 값이 있을 경우 Return
    existing_entry = db.userInfo.find_one({'id' : userID})
    if existing_entry:
        return jsonify({'result' : 'failed', 'msg' : '중복된 값이 존재합니다.'})
    
    # DB에서 입력받은 NickName과 동일한 값이 있을 경우 Return
    duple_nick_name = db.userInfo.find_one({'nickName' : userNickname})
    if duple_nick_name:
        return jsonify({'result' : 'failed', 'msg' : '중복된 값이 존재합니다.'})
    
    new_userInfo = {
        "id" : userID,
        "pw" : userPW,
        "profile" : filename,
        "nickName" : userNickname,
        "hasIntroduce" : False,
        "question1" : "",
        "correctAnswer1" : "",
        "incorrectAnswers1" : [],
        
        "question2" : "",
        "correctAnswer2" : "",
        "incorrectAnswers2" : [],
        
        "question3" : "",
        "correctAnswer3" : "",
        "incorrectAnswers3" : [],
        
        "question4" : "",
        "correctAnswer4" : "",
        "incorrectAnswers4" : [],
        
        "question5" : "",
        "correctAnswer5" : "",
        "incorrectAnswers5" : [],
    }
    
    db.userInfo.insert_one(new_userInfo)
    return jsonify({'result' : 'success', 'msg' : '정상 값이 입력되었습니다.'})
    

# 로그인 기능
@app.route('/api/signin', methods=['POST'])
def login():
    userId = request.form['id']
    userPw = request.form['pw']
    
    # DB에 있는 데이터와 비교하기
    dupleUser = db.userInfo.find_one({'id' : userId, "pw" : userPw})
    if dupleUser:
        # JWT 토큰 생성 (유효시간 60분)
        expires = datetime.timedelta(minutes=60)
        access_token = create_access_token(
            identity = userId, 
            expires_delta = expires,
            additional_claims={
                'name': dupleUser['nickName'],
                'profile_image':dupleUser.get('profile','')
            }
        )
        response = jsonify({'result' : 'success', 'msg' : '정상적으로 로그인이 되었습니다.', "token" : access_token})
        response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax') # 쿠키 보안 설정
        return response
    else:
        return jsonify({'result' : 'failed', 'msg' : '로그인이 실패했습니다.'})
    
# 로그아웃 기능
@app.route('/api/logout', methods=['POST'])
def logout():
    response = jsonify({'msg': '로그아웃 되었습니다.'})
    response.delete_cookie('access_token')  # 쿠키에서 JWT 토큰 삭제
    return response


# 비공개 데이터 ( Masking, Blur )
@app.route('/api/private/data', methods=['GET'])
def privateData():
    nicknames = get_nicknames_with_true_value()
    data = []
    masking_nickanmes = []
    
    for name in nicknames:
        masking_nickanmes.append(masking(name))
    
    data.append(masking_nickanmes)
    profile_images_url = get_profile_image_with_true_value()
    data.append(profile_images_url)
    
    return jsonify({'result' : 'success', 'msg' : '데이터를 정상적으로 수행 했습니다.', 'data' : data})

# 자기소개 페이지가 존재하는 사람들의 이름을 관리
def get_nicknames_with_true_value():
    nicknames = db.userInfo.find(
        { 'hasIntroduce' : True},
        {'nickName': 1, '_id': 0} 
    )
    return [nickname['nickName'] for nickname in nicknames]

def get_profile_image_with_true_value():
    temp_profile_image_titles = db.userInfo.find(
        { 'hasIntroduce' : True},
        { 'profile' : 1, '_id' : 0}
    )    
    # profile images들의 Title Text를 가져온다.
    profile_images = [profile_image_title['profile'] for profile_image_title in temp_profile_image_titles]
    
    images_url = []
    # Title Text
    for title in profile_images:
        # title 데이터를 가져와서 상대 경로로 images 파일을 가져온다.
        images_url.append(list({ url_for('static', filename='uploads/{}'.format(title)) }))
    return images_url

# Text 마스킹
def masking(text):
    if len(text) > 1:
        return text[0] + 'X' * (len(text) - 1)
    return text

# 공개된 데이터
@app.route('/api/public/data', methods=['GET'])
@jwt_required()
def publicData():
    cur_user = get_jwt_identity()
    if cur_user is None:
        return jsonify({'result' : 'failed', 'msg' : '유효하지 않은 토큰 값'})
    
    # 닉네임 List 전달
    nicknames = get_nicknames_with_true_value()
    images_url = get_profile_image_with_true_value()
    
    data = []
    data.append(nicknames)
    data.append(images_url)
    
    return jsonify({'result' : 'success', 'msg' : '데이터를 정상적으로 수행 했습니다.', 'data' : data})

# 랜덤 유저 전달
@app.route('/api/randUser', methods=['GET'])
def randUser():
    
    # 닉네임 List 전달
    nicknames = get_nicknames_with_true_value()
    # 난수 추출
    random_nickname = random.choice(nicknames)
    random_user_id = db.userInfo.find_one({'nickName' : random_nickname}, {'_id' : 0})['id']
    
    return jsonify({'result' : 'success', 'msg' : '데이터를 정상적으로 수행 했습니다.', 'id' : random_user_id})

# 일반 질문 1
@app.route('/api/addQuestion/1')
def addQuestion1():
    return 'AddQuestion'

# 일반 질문 2
@app.route('/api/addQuestion/2')
def addQuestion2():
    return 'Add Question 2'

# 일반 질문 3
@app.route('/api/addQuestion/3')
def addQuestion3():
    return 'Add Question 3'

# 일반 질문 4
@app.route('/api/addQeustion/4')
def addQuestion4():
    return 'Add Question 4'

# 일반 질문 5
@app.route('/api/addQuestion/5')
def addQuestion5():
    return 'Add Question 5'

# 자기소개 입력
@app.route('/api/addIntroduce')
def addIntroduce():
    return 'Add Introduce'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)