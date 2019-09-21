from blogs import db, bcrypt, User , Post 

user_1 = User(username='admin',image_file='img1.jpg',email='admin@123.com',name='Admin',password=bcrypt.generate_password_hash('123').decode('utf-8'))
db.session.add(user_1)
user_2 = User(username='admin1',image_file='img2.jpg',email='admin@1234.com',name='Admin 2',password=bcrypt.generate_password_hash('123').decode('utf-8'))
db.session.add(user_2)
db.session.commit()