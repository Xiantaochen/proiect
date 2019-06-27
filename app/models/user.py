from sqlalchemy import Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db,BaseModel

class User(Base,BaseModel):
    id=db.Column(db.Integer,primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    email = Column(String(50), unique=True, nullable=False) #用户邮箱
    phone_num = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    auth = Column(SmallInteger, default=1)
    nickname = Column(String(24), nullable=False)
    password = Column('password', String(128))
    avatar_url = db.Column(db.String(128))  # 用户头像路径
    real_name = db.Column(db.String(32))  # 真实姓名
    id_card = db.Column(db.String(20))  # 身份证号

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'email', 'nickname']

    def keys(self):
        return self.fields

    def hide(self, *keys):
        [self.fields.remove(key) for key in keys]

    def append(self, *keys):
        [self.fields.append(key) for key in keys]

    @property
    def password_hash(self):
        raise AttributeError(u'不能访问该属性')

    @password_hash.setter
    def password_hash(self, raw):
        self.password = generate_password_hash(raw)

    # 从面向对象的角度考虑，在一个对象中创建一个对象本身这个是不合理的。
    # 但是如果将他声明为一个静态方法，那么就是合理的
    @staticmethod
    def register_by_email(nikename, account, secert):
        with db.auto_commit():
            user = User()
            user.nickname = nikename
            user.email = account
            user.password = secert
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'SuperScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self.password:
            return False
        return check_password_hash(self._password, raw)

    def to_dict(self):
        # 返回一个用户信息字典接口，使外界方便调用
        user_info = {
            'user_id': self.id,
            'name': self.name,
            'phone_num': self.phone_num,
            'avatar_url': self.avatar_url
        }

    def to_auth_dict(self):
        """实名认证数据"""
        return {
            'real_name':self.real_name,
            'id_card':self.id_card
        }
