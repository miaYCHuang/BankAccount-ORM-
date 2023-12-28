import os
from flask import Flask,request, jsonify,send_from_directory, abort
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api
from resources.user import User,Users
from resources.account import Accounts,Account
from resources.models import db,accounts
from sqlalchemy import or_

app= Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@127.0.0.1:80/api'#database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/api'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 不追蹤 減少性能消耗
db.init_app(app)
api = Api(app)

api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')
api.add_resource(Accounts,'/user/<user_id>/accounts')
api.add_resource(Account,'/user/<user_id>/account/<id>')

#swagger
#http://localhost/swagger/
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python API - Swagger"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

#[POST]使用者一個帳戶存錢
@app.route('/user/<user_id>/account/<id>/deposit',methods=['POST'])    
def deposit(user_id,id):
    account_data = get_account(user_id,id)
    if account_data:
        money = request.get_json().get('money')  # JSON 中的金額
        if money and isinstance(money, int) and money > 0:# money正整數且>0
            #修改餘額
            account_data.balance += money
            db.session.commit()
            return {'message': 'Account eposited successfully'}, 201
        else:
            return {'message': 'money must be greater than 0'}, 400
    else:
        abort(jsonify(message=f"No User ID = '{user_id}' and Account ID = '{id}'."), 404)

#[POST]使用者一個帳戶領錢
@app.route('/user/<user_id>/account/<id>/withdraw',methods=['POST'])
def withdraw(user_id,id):
    account_data = get_account(user_id,id)
    #account_data = accounts.query.filter(or_(accounts.deleted != True, accounts.deleted.is_(None)), accounts.id==id, accounts.user_id==user_id).first()
    if account_data:
        money = request.get_json().get('money')  # JSON 中的金額
        if money and isinstance(money, int) and money > 0:# money正整數且>0
            #修改餘額
            if account_data.balance >= money:  # 確認餘額足夠提款
                account_data.balance -= money
                db.session.commit()
                return {'message': 'Account withdrawn successfully'}, 201
            else:
                return {'message': 'Insufficient funds'}, 400
    else:
        abort(jsonify(message=f"No User ID = '{user_id}' and Account ID = '{id}'."), 404)
 

def get_account(user_id,id):#取得單筆 id=n, user_id=m 的資料
    #( deleted=0(False) or null ) and id=n and user_id=m
    data = accounts.query.filter(or_(accounts.deleted != True, accounts.deleted.is_(None)), accounts.id==id, accounts.user_id==user_id).first()
    return data


#測試資料庫
@app.route('/test')
def index():
    data = accounts.query.all()
    print(data)
    user_ids = [user.account_number for user in data]
    return jsonify(user_ids)


#測試API
@app.route('/')
def hello_world():
    ip_addr = request.remote_addr
    return '<h1> Your IP address is:' + ip_addr
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', debug=True, threaded=True, port=3000)
