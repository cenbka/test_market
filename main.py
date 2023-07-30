from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from Database import db, Basket, Items
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/order', methods = ['POST', 'GET'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        item = Items(name=name, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/product')
        except:
            return 'Ошибка'
    else:
        return render_template('order.html')


@app.route('/product/<int:id>')
def change(id):
    item_id = Items.query.get(id)
    return render_template('change.html', item_id=item_id)


@app.route('/product/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    item_id = Items.query.get(id)
    if request.method == 'POST':
        item_id.name = request.form['name']
        item_id.price = request.form['price']

        try:
            db.session.commit()
            return redirect('/product')
        except:
            return 'Ошибка'
    else:
        return render_template('update.html', item_id=item_id)


@app.route('/product/<int:id>/del')
def delete(id):
    item_id = Items.query.get_or_404(id)
    basket_id = Basket.query.get_or_404(id)

    try:
        db.session.delete(item_id)
        db.session.delete(basket_id)
        db.session.commit()
        return redirect('/product')
    except:
        return 'Ошибка'


@app.route('/product')
def product():
    items = Items.query.order_by(Items.id).all()
    return render_template('product.html', items=items)


@app.route('/product/<int:id>', methods=['POST', 'GET'])
def basket_add(id):
    item_id = Items.query.get(id)
    if request.method == 'POST':
        #item_id.id = request.form['id']
        #item_id.name = request.form['name']
        #item_id.price = request.form['price']

        basket = Basket(id=item_id.id, name=item_id.name, price=item_id.price)

        try:
            db.session.add(basket)
            db.session.commit()
            return redirect('/basket')
        except:
            return redirect('/basket')
    else:
        return render_template('product.html')


@app.route('/basket')
def basket():
    basket1 = Basket.query.order_by(Basket.id).all()
    return render_template('basket.html', basket1=basket1)


@app.route('/basket/<int:id>/del')
def basket_delete(id):
    basket_id = Basket.query.get_or_404(id)

    try:
        db.session.delete(basket_id)
        db.session.commit()
        return redirect('/basket')
    except:
        return 'Ошибка'


with app.app_context():
    db.create_all()
app.run(debug=True)