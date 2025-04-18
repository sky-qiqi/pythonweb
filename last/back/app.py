import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy <- Remove this line
from extensions import db # <- Add this line

# 加载 .env 文件中的环境变量
load_dotenv()

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') # <- Changed from DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
# db = SQLAlchemy(app) <- Remove this line
db.init_app(app) # <- Add this line

# 启用 CORS
CORS(app)

# 导入蓝图 (在 db 初始化之后)
from routes import main_bp
app.register_blueprint(main_bp)

if __name__ == '__main__':
    # 在应用上下文中创建数据库表
    with app.app_context():
        db.create_all()
    app.run(debug=True)