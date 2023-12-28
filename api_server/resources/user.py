from flask_restful import Resource, reqparse
from flask import jsonify
from resources.models import users,db
from sqlalchemy import or_

#Only accept these fields
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

#http://localhost:5000/user/<id>
class User(Resource):
    #[GET]取得一筆使用者
    def get(self,id):
        #( deleted=0(False) or null ) and id=n
        data = users.query.filter(or_(users.deleted != True, users.deleted.is_(None)), users.id==id).first_or_404(description=f"No User ID = '{id}'.")
        print(data)
        the_user_data = {
            'id': data.id,
            'name': data.name,
            'gender': data.gender,
            'birth ': data.birth,
            'note ': data.note,
            'deleted': data.deleted
        }
        return jsonify(the_user_data)

    #[PATCH]修改一筆使用者資料
    def patch(self, id):
        data = users.query.filter_by(id=id).first_or_404(description=f"No User ID = '{id}'.")
        print(data)
        arg=parser.parse_args()
        user_to_update ={
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'],
            'note':arg['note'],
        }     
        for key, value in user_to_update.items():
            if value != None:
                setattr(data, key, value) #動態設置
        db.session.commit()#保存入資料庫
        return jsonify({'message': 'User updated successfully'})#200

    #[DELETE]刪除一筆使用者資料
    def delete(self, id):
        data = users.query.filter_by(id=id).first_or_404(description=f"No User ID = '{id}'.")
        data.deleted = True
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})#200




#http://localhost:5000/users
class Users(Resource):    
    #[GET]取得所有使用者
    def get(self):
        #data = users.query.all()
        data = users.query.filter(or_(users.deleted != True, users.deleted.is_(None))).all() #deleted=0(False) or null
        print(data)
        user_list=[]
        for user in data:
            user_data = {
                'id': user.id,
                'name': user.name,
                'gender': user.gender,
                'birth ': user.birth,
                'note ': user.note,
                'deleted': user.deleted
            }
            user_list.append(user_data)
        return jsonify(user_list)
    
    #[POST]增加一筆使用者
    def post(self):
        arg=parser.parse_args()
        user = users(
            name=arg['name'],
            gender=arg['gender'] or 0,
            birth=arg['birth'] or '1990-01-01',
            note=arg['note']
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201