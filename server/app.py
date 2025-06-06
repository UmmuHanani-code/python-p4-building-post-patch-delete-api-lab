#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

@app.route('/baked_goods', methods=['POST'])
def new_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')


    if not name or not price:
        return jsonify({"error": "Missing name or price"}), 400

    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "Price must be a number"}), 400

    baked_good = BakedGood(name=name, price=price)
    db.session.add(baked_good)
    db.session.commit()

    return jsonify(baked_good.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_change_name(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404

    if request.method == 'PATCH':
        name = request.form.get('name')
        if name:
            bakery.name = name
            db.session.commit()

        return jsonify(bakery.to_dict()), 200

    return jsonify(bakery.to_dict()), 200


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)

    if not baked_good:
        return jsonify({"error": "Baked good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "record successfully deleted"}), 200






if __name__ == '__main__':
    app.run(port=5555, debug=True)