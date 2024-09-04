from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from flask_jwt_extended import *

import base64, random

client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)
app.config.update(
    JWT_SECRET_KEY = "TEST"
)
jwt = JWTManager(app)


### Page Container

# Main Page
@app.route('/')
def home():
    return render_template('index.html')

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
        "profile" : userProfile.filename,
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
    
    db.userInfo.insert_one(new_userInfo);
    return jsonify({'result' : 'success', 'msg' : '정상 값이 입력되었습니다.'})
    

# 로그인 기능
@app.route('/api/signin', methods=['POST'])
def login():
    userId = request.form['id']
    userPw = request.form['pw']
    
    # DB에 있는 데이터와 비교하기
    dupleUser = db.userInfo.find_one({'id' : userId, "pw" : userPw})
    if dupleUser:
        return jsonify({'result' : 'success', 'msg' : '정상적으로 로그인이 되었습니다.', "token" : create_access_token(identity = userId, expires_delta=60)})
    else:
        return jsonify({'result' : 'failed', 'msg' : '로그인이 실패했습니다.'})


# 비공개 데이터 ( Masking, Blur )
@app.route('/api/private/data', methods=['GET'])
def privateData():
    nicknames = get_nicknames_with_true_value()
    masking_nickanmes = []
    
    for name in nicknames:
        masking_nickanmes.append(masking(name))
        
    return jsonify({'result' : 'success', 'msg' : '데이터를 정상적으로 수행 했습니다.', 'nicknames' : masking_nickanmes})

# 자기소개 페이지가 존재하는 사람들의 이름을 관리
def get_nicknames_with_true_value():
    nicknames = db.userInfo.find(
        { 'hasIntroduce' : True},
        {'nickName': 1, '_id': 0} 
    )
    return [nickname['nickName'] for nickname in nicknames]

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
    return jsonify({'result' : 'success', 'msg' : '데이터를 정상적으로 수행 했습니다.', 'nicknames' : nicknames})

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