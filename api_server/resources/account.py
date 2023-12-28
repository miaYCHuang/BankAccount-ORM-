from flask_restful import Resource, reqparse
from flask import jsonify
from resources.models import accounts,db
from sqlalchemy import or_

#Only accept these fields
parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')
parser.add_argument('deleted')

# http://localhost:5000/user/<user_id>/account/<id>
class Account(Resource):

    #[GET]取得使用者的一個帳戶
    def get(self,user_id,id):
        #( deleted=0(False) or null ) and id=n
        data = accounts.query.filter(or_(accounts.deleted != True, accounts.deleted.is_(None)), accounts.id==id, accounts.user_id==user_id).first_or_404(description=f"No User ID = '{user_id}' and Account ID = '{id}'.")
        print(data)
        the_user_data = {
            'id': data.id,
            'balance': data.balance,
            'account_number': data.account_number,
            'user_id ': data.user_id,
            'deleted ': data.deleted
        }
        return jsonify(the_user_data)

    #[PATCH]修改使用者的一個帳戶資訊
    def patch(self,user_id, id):
        data = accounts.query.filter(accounts.id==id, accounts.user_id==user_id).first_or_404(description=f"No User ID = '{user_id}' and Account ID = '{id}'.")
        print(data)
        arg=parser.parse_args()
        if arg['account_number'] == None:
            arg['account_number']=''
        user_to_update ={
            'balance':arg['balance'],
            'account_number':arg['account_number'].zfill(20)
        }
        #可只修改其一
        for key, value in user_to_update.items():
            if value != None:
                setattr(data, key, value) #動態設置
        db.session.commit()#保存入資料庫
        return jsonify({'message': 'Account updated successfully'}) #200
    
    #[GET]刪除使用者的一個帳戶
    def delete(self,user_id, id):
        data = accounts.query.filter(accounts.id==id, accounts.user_id==user_id).first_or_404(description=f"No User ID = '{user_id}' and Account ID = '{id}'.")
        data.deleted = True
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully'})#200




# http://localhost:5000//user/<user_id>/accounts
class Accounts(Resource):
    
    #[GET]取得使用者的所有帳戶 
    def get(self,user_id):
        #( deleted=0(False) or null ) and user_id=n
        data = accounts.query.filter(or_(accounts.deleted != True, accounts.deleted.is_(None)), accounts.user_id == user_id).all()
        if data :
            print(data)
            account_list=[]
            for account in data:
                account_data = {
                    'id':account.id,
                    'balance': account.balance,
                    'account_number': account.account_number,
                    'user_id': account.user_id,
                    'deleted': account.deleted
                }
                account_list.append(account_data)
            return jsonify(account_list)
        else:
            return {'message': 'Account no user_id = '+user_id+''}, 404
    
    #[POST]新增一個使用者的帳戶
    def post(self,user_id):
        arg=parser.parse_args()
        data = accounts.query.filter(accounts.account_number == arg['account_number'].zfill(20)).all()
        if data:
            return {'message': 'account_number existed'}, 400
        else:
            account = accounts(
                balance=arg['balance'],
                account_number=arg['account_number'].zfill(20),
                user_id = user_id
            )
            print(account.account_number)
            db.session.add(account)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
