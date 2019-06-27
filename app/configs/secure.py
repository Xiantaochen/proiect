
__author__ = "gaowenfeng"

HOSTNAME = "127.0.0.1"
PORT = '3306'
DATABASE = 'ginger'
USERNAME = 'root'
PASSWORD = "302811"
DB_URL = "mysql+cymysql://{}:{}@{}:{}/{}".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URL
SECRET_KEY = 'ix4En7l1Hau10aPq8kv8tuzcVl1s2Zo6eA+5+R+CXor8G3Jo0IJvcj001jz3XuXl'

