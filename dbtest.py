from app import db
from app.models import User,Post

# u = User(username='duke', email='duke@126.com')
# u.set_password('123456')
# db.session.add(u)
# db.session.commit()
posts = Post.query.all()
for p in posts:
    db.session.delete(p)
db.session.commit()