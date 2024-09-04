from flask import Flask, jsonify, request, render_template, url_for, redirect
from pymongo import MongoClient
from flask_jwt_extended import *
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter
from werkzeug.security import generate_password_hash, check_password_hash
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

### Function 

# PW 해싱
def hash_password(password):
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

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
            id = decoded_token.get('id','')
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            # introduced = decoded_token.get('introduced','')
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
            id1 = decoded_token.get('id1','')
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            # introduced = decoded_token.get('introduced','')
            logged_in = True
        except Exception as e:
            logged_in = False
    else:
        logged_in = False
    return render_template('quiz-form.html', logged_in=logged_in, name=name, profile_image=profile_image, id=id1)

# 자기소개 결과 페이지
@app.route('/introduce/result')
def introudceResult():
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
            id = decoded_token.get('id','')
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            logged_in = True
        except Exception as e:
            logged_in = False
    else:
        logged_in = False

    return render_template('result.html', logged_in=logged_in, name=name, profile_image=profile_image)

# 자기소개 페이지
@app.route('/introduce')
def showIntroduce():
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
            id = decoded_token.get('id','')
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            # introduced = decoded_token.get('introduced','')
            logged_in = True
        except Exception as e:
            logged_in = False
    else:
        logged_in = False

    return render_template('quiz.html', logged_in=logged_in, name=name, profile_image=profile_image)

# 자기소개 수정 선택 페이지
@app.route('/edit/select')
def editQuizSelection():
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
            id = decoded_token.get('id','')
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            # introduced = decoded_token.get('introduced','')
            logged_in = True
        except Exception as e:
            logged_in = False
    else:
        logged_in = False

    return render_template('edit-selection.html', logged_in=logged_in, name=name, profile_image=profile_image)


# 자기소개 퀴즈 수정 페이지
@app.route('/edit/quiz')
def editQuiz():
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
            id = decoded_token.get('id','')
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            # introduced = decoded_token.get('introduced','')
            logged_in = True
        except Exception as e:
            logged_in = False
    else:
        logged_in = False

    return render_template('edit-quiz.html', logged_in=logged_in, name=name, profile_image=profile_image)


# 자기소개 퀴즈 수정 페이지
@app.route('/edit/intro')
def editIntro():
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
            id = decoded_token.get('id','')
            name = decoded_token.get('name','')
            profile_image = decoded_token.get('profile_image', '')
            # introduced = decoded_token.get('introduced','')
            logged_in = True
        except Exception as e:
            logged_in = False
    else:
        logged_in = False

    return render_template('edit-intro.html', logged_in=logged_in, name=name, profile_image=profile_image)


### API

# 회원가입 기능
@app.route('/api/signup', methods=['POST'])
def register():
    # ID
    userID = request.form['id']
    if len(userID) < 4:
        return jsonify({'result' : 'failed', 'msg' : 'ID를 4글자 이상 작성해주세요.'})
    
    # PW
    userPW = request.form['pw']
    if len(userPW) < 12:
        return jsonify({'result' : 'failed', 'msg' : 'PW를 12글자 이상 작성해주세요.'})
    
    hashed_pw = hash_password(userPW)
    
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
        "pw" : hashed_pw,
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
    user = db.userInfo.find_one({'id' : userId})
    if user:
        if not verify_password(user['pw'], userPw):
            return jsonify({'result' : 'failed', 'msg' : '로그인이 실패했습니다.'})
        
        # JWT 토큰 생성 (유효시간 60분)
        expires = datetime.timedelta(minutes=60)
        access_token = create_access_token(
            identity = userId, 
            expires_delta = expires,
            additional_claims={
                'id1': userId,
                'name': user['nickName'],
                'profile_image':user.get('profile',''),
                # 'introduced': dupleUser['hasIntroduce']
            }
        )
        response = jsonify({'result' : 'success', 'msg' : '정상적으로 로그인이 되었습니다.', "token" : access_token})
        response.set_cookie('access_token', access_token, secure=True, samesite='Lax') # 쿠키 보안 설정
        return response
    else:
        return jsonify({'result' : 'failed', 'msg' : '로그인이 실패했습니다.'})
    
# 로그아웃 기능
@app.route('/api/logout', methods=['POST'])
def logout():
    response = jsonify({'msg': '로그아웃 되었습니다.'})
    response.delete_cookie('access_token')  # 쿠키에서 JWT 토큰 삭제
    return response

# 자기소개 작성한 회원들 정보 넘겨주는 api
@app.route('/api/quizs', methods=['GET'])
def get_quizs():
    try:
        # DB에서 hasIntroduce가 True인 사용자 정보 조회
        users_with_introduced = list(db.userInfo.find({'hasIntroduce': True}, {'_id': 0, 'id': 1, 'nickName': 1, 'profile': 1}))
        
        return jsonify({'result': 'success', 'quizs': users_with_introduced})
    except Exception as e:
        return jsonify({'result': 'fail', 'msg': str(e)})


# 비공개 데이터 ( Masking, Blur )
@app.route('/api/private/data', methods=['GET'])
def privateData():
    nicknames = get_nicknames_with_true_value()
    data = []
    masking_nickanmes = []
    
    for name in nicknames:
        masking_nickanmes.append(masking(name))
    
    data.append(masking_nickanmes)
    profile_images_url = get_profile_image_with_true_value(0)
    data.append(profile_images_url)
    id_datas = get_id_with_true_value()
    data.append(id_datas)
    
    return jsonify({'result' : 'success', 'msg' : '데이터를 정상적으로 수행 했습니다.', 'data' : data})

# 자기소개 페이지가 존재하는 사람들의 이름을 관리
def get_nicknames_with_true_value():
    nicknames = db.userInfo.find(
        { 'hasIntroduce' : True},
        {'nickName': 1, '_id': 0} 
    )
    return [nickname['nickName'] for nickname in nicknames]

def get_profile_image_with_true_value(type):
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
        # Type이 1이면 Origin / 2면 Blur
        if type == 1:
            images_url.append(list({ url_for('static', filename='uploads/{}_origin.jpg'.format(title)) }))
        else :
            images_url.append(list({ url_for('static', filename='uploads/{}_blur.jpg'.format(title)) }))
    return images_url

def get_id_with_true_value():
    ids = db.userInfo.find(
        { 'hasIntroduce' : True},
        { 'id' : 1, '_id' : 0}
    )
    return [id['id'] for id in ids]

# Text 마스킹
def masking(text):
    if len(text) > 1:
        return text[0] + 'X' * (len(text) - 1)
    return text

# 공개된 데이터
@app.route('/api/public/data', methods=['GET'])
def publicData():
    # 닉네임 List 전달
    
    nicknames = get_nicknames_with_true_value()
    images_url = get_profile_image_with_true_value(1)
    id_datas = get_id_with_true_value()
    
    data = []
    data.append(nicknames)
    data.append(images_url)
    data.append(id_datas)
    
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

### (2024-09-04) 20:00 // 박수호님 코드

@app.route('/quiz')
def quiz():
  return render_template('quiz.html')

@app.route('/quizform')
def quiz_form():
  return render_template('quiz-form.html')

@app.route('/introform')
def intro_form():
  return render_template('intro-form.html')
# api 
client = MongoClient('localhost', 27017)
quiz_db = client.quizdb
user_collection = quiz_db.userdb

# 자기소개 생성
@app.route('/api/submit_intro/<string:user_id>', methods=['POST'])
def submit_intro(user_id):
    data = request.get_json()

    print(user_id)
    # 자기소개 데이터가 있는지 확인
    quizzes = data.get("quizzes")
    intro = data.get("intro")

    # 데이터 검증
    if not quizzes or len(quizzes) != 5:
        return jsonify({"message": "5개의 퀴즈를 보내야 합니다."}), 400
    if not intro:
        return jsonify({"message": "자기소개가 필요합니다."}), 400

    user = user_collection.find_one({"user_id": user_id})

    if not user:
        # 새 사용자와 퀴즈 목록 및 자기소개 삽입
        user_collection.insert_one({
            "user_id": user_id,
            "quizzes": quizzes,
            "intro": intro
        })
    else:
        # 기존 사용자의 퀴즈와 자기소개 업데이트
        user_collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "quizzes": quizzes,
                "intro": intro
            }}
        )

    getUser = db.userInfo.find_one({'id' : user_id})
    getUser['hasIntroduce'] = True
    
    db.userInfo.update_one({'id' : user_id},
                           {'$set' : {'hasIntroduce' : True}})
    

    return jsonify({'result': 'success'}), 201


# 퀴즈 불러오기
@app.route('/api/quiz/<string:user_id>', methods=['GET'])
def get_quiz_data(user_id):
    # 사용자의 퀴즈 데이터를 MongoDB에서 찾음
    user = user_collection.find_one({"user_id": user_id})
    if not user or "quizzes" not in user:
        return jsonify({"message": "유저 또는 퀴즈를 찾을 수 없습니다."}), 404
    
    # 퀴즈 데이터를 가져오고 문제의 정답과 오답을 섞음
    quiz_data = user["quizzes"][:5]  # 5개의 퀴즈만 가져옴
    for quiz in quiz_data:
        options = quiz['answer']['wrong'] + [quiz['answer']['correct']]
        random.shuffle(options)  # 정답과 오답을 랜덤하게 섞음
        quiz['shuffled_options'] = options

    return jsonify(quiz_data), 200

@app.route('/quiz/<string:user_id>', methods=['GET'])
def get_all_quizzes(user_id):
    
  user = user_collection.find_one({"user_id": user_id})
  if not user:
    return jsonify({"message": "유저를 찾을 수 없습니다."}), 404

  #return jsonify(user["quizzes"]), 200
  return render_template('quiz.html', user = user_id)

@app.route('/quiz/<string:user_id>/<int:quiz_number>', methods=['GET'])
def get_quiz(user_id, quiz_number):
  user = user_collection.find_one({"user_id": user_id})
  
  if not user:
    return jsonify({"message": "유저를 찾을 수 없습니다."}), 404
  
  quiz = next((q for q in user["quizzes"] if q["number"] == quiz_number), None)
  if not quiz:
    return jsonify({"message": "퀴즈를 찾을 수 없습니다."}), 404
  
  return jsonify(quiz), 200

@app.route('/api/quiz/<string:user_id>/<int:quiz_number>', methods=['PUT'])
def update_quiz(user_id, quiz_number):
    data = request.get_json()
    user = user_collection.find_one({"user_id": user_id})

    if not user:
        return jsonify({"message": "유저를 찾을 수 없습니다."}), 404
    
    quizzes = user.get("quizzes", [])
    quiz_index = next((i for i, q in enumerate(quizzes) if q["number"] == quiz_number), None)

    if quiz_index is None:
        return jsonify({"message": "퀴즈를 찾을 수 없습니다."}), 404

    # 퀴즈 업데이트
    quizzes[quiz_index] = data
    user_collection.update_one(
        {"user_id": user_id},
        {"$set": {"quizzes": quizzes}}
    )

    return jsonify({"message": "퀴즈가 업데이트되었습니다."}), 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)