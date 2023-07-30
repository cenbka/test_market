from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

   # def __repr__(self):
        #return 'Цена:' + str(self.price) + ' ' +'Название:' + self.name


class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
