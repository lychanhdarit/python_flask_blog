pip3 install flask
pip3 install flask-mysqldb
pip3 install pyyaml 
pip3 install flask-restful
pip3 install flask-wtf

//---------------
Tạo SECRET_KEY
python
import secrets
secrets.token_hex(16)
//------------------
from flash_bcrypt import Bcrypt
bcrypt = Bcrypt()
bcrypt.generate_password_hash('test')

bcrypt.generate_password_hash('test').decode('utf-8')
//Mã hash mỗi lần tạo ko giống nhau
hashed_pw = bcrypt.generate_password_hash('test').decode('utf-8')
//Hàm check pass
bcrypt.check_password_hash(hashed_pw,'password')
//
pip install flask-login

pip install SQLAlchemy


db.createall()