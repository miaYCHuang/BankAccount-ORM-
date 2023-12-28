from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 定義資料表模型
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(45), nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    birth = db.Column(db.Date, nullable=True)
    note = db.Column(db.Text, nullable=True)
    deleted = db.Column(db.Boolean, nullable=True)

class accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    balance = db.Column(db.Integer, nullable=True)
    account_number = db.Column(db.String(20), nullable=True, unique=True)
    user_id = db.Column(db.Integer, nullable=True)
    deleted = db.Column(db.Boolean, nullable=True)

# 創建定義中的表格，如果資料庫有對應則不影響
# with app.app_context():
#     db.create_all()