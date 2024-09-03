from flask import Flask, jsonify
from flask import request
from pymongo import MongoClient
import base64

client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)


### Page Container

# Main Page
@app.route('/')
def home():
    return 'This is Home!'

# Sign In Page
@app.route('/signin')
def loginPage():
    return 'Sign In Page'

# Signup Page
@app.route('/signup')
def registerPage():
    return 'Sign Up Page'

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
        return jsonify({'result' : 'success', 'msg' : '정상적으로 로그인이 되었습니다.'})
    else:
        return jsonify({'result' : 'failed', 'msg' : '로그인이 실패했습니다.'})


# 비공개 데이터 ( Masking, Blur )
@app.route('/api/private/data', methods=['POST'])
def privateData():
    return 'Masking and Blur'

# Text 마스킹

# 공개된 데이터
@app.route('/api/public/data', methods=['POST'])
def publicData():
    return 'None Masking and Blur'

# 랜덤 유저 전달
@app.route('/api/randUser', methods=['POST'])
def randUser():
    return 'rand user'

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