from flask import Blueprint, render_template, url_for, request, redirect, jsonify

from webapp import db
from webapp.pizza.forms import ToppingForm
from webapp.pizza.models import Topping, Pizza

pizza = Blueprint('pizza', __name__, template_folder='templates')


@pizza.route('/pizza', methods=['GET', 'POST'])
def index():
    toppings = Topping.query.all()
    pizzas = Pizza.query.all()
    return render_template(
        'pizza/index.html',
        toppings=toppings,
        pizzas=pizzas,
    )

# @pizza.route('/get_modal', methods=['GET', 'POST'])
# def get_modal():
#     action = request.form.get('action')
#     print(action)
#     return jsonify({
#         'data': 'test'
#     })

@pizza.route('/add_topping', methods=['GET', 'POST'])
def add_topping():
    topping = Topping(name=request.form.get('name').lower())
    topping_exists = db.session.query(Topping).filter_by(name=topping.name).first()
    if not topping_exists:
        db.session.add(topping)
        db.session.commit()
    return redirect(url_for('pizza.index'))


@pizza.route('/edit_topping', methods=['GET', 'POST'])
def edit_topping():
    name = request.form.get('name').lower()
    topping_id = request.form.get('toppingId')
    topping = Topping.query.filter_by(id=topping_id).first()
    topping.name = name
    db.session.commit()
    return redirect(url_for('pizza.index'))


@pizza.route('/delete_topping', methods=['GET', 'POST'])
def delete_topping():
    topping_id = request.form.get('toppingId')
    topping = Topping.query.filter_by(id=topping_id).first()
    db.session.delete(topping)
    db.session.commit()
    return redirect(url_for('pizza.index'))


@pizza.route('/add_pizza', methods=['GET', 'POST'])
def add_pizza():
    pizza = Pizza(name=request.form.get('name').lower())
    pizza_exists = db.session.query(Pizza).filter_by(name=pizza.name).first()
    if pizza_exists:
        return redirect(url_for('pizza.index'))

    toppings = request.form.getlist('topping')
    toppings.sort()
    all_pizzas = Pizza.query.all()
    for p in all_pizzas:
        pizza_toppings = [str(topping.id) for topping in p.toppings]
        pizza_toppings.sort()
        if pizza_toppings == toppings:
            return redirect(url_for('pizza.index'))

    for topping_id in toppings:
        topping = db.session.query(Topping).filter_by(id=topping_id).first()
        pizza.toppings.append(topping)

    db.session.add(pizza)
    db.session.commit()
    return redirect(url_for('pizza.index'))


@pizza.route('/edit_pizza', methods=['GET', 'POST'])
def edit_pizza():
    pizza = Pizza.query.filter_by(id=request.form.get('pizzaId').lower()).first()
    pizza_exists = db.session.query(Pizza).filter_by(name=pizza.name).first()
    if pizza_exists:
        return redirect(url_for('pizza.index'))

    toppings = request.form.getlist('topping')
    toppings.sort()
    all_pizzas = Pizza.query.all()
    for p in all_pizzas:
        pizza_toppings = [str(topping.id) for topping in p.toppings]
        pizza_toppings.sort()
        if pizza_toppings == toppings:
            return redirect(url_for('pizza.index'))

    pizza.toppings.clear()
    for topping_id in toppings:
        topping = db.session.query(Topping).filter_by(id=topping_id).first()
        pizza.toppings.append(topping)

    db.session.add(pizza)
    db.session.commit()
    return redirect(url_for('pizza.index'))


@pizza.route('/delete_pizza', methods=['GET', 'POST'])
def delete_pizza():
    pizza_id = request.form.get('pizzaId')
    pizza = Pizza.query.filter_by(id=pizza_id).first()
    pizza.toppings.clear()
    db.session.delete(pizza)
    db.session.commit()
    return redirect(url_for('pizza.index'))


@pizza.route('/pizza_info', methods=['POST'])
def pizza_info():
    pizza = Pizza.query.filter_by(id=request.form.get('pizza_id')).first()
    return jsonify({
        'toppings': [topping.name for topping in pizza.toppings],
        'topping_ids': [topping.id for topping in pizza.toppings]
    })
