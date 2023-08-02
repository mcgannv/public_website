from flask import Blueprint, render_template, url_for, request, redirect, jsonify

from webapp import db
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


@pizza.route('/add_topping', methods=['GET', 'POST'])
def add_topping():
    topping = Topping(name=request.form.get('name').lower())
    if not is_exists(Topping, topping.name):
        db.session.add(topping)
        db.session.commit()
    return redirect(url_for('pizza.index'))


@pizza.route('/edit_topping', methods=['GET', 'POST'])
def edit_topping():
    name = request.form.get('name').lower()
    if is_exists(Topping, name):
        return redirect(url_for('pizza.index'))
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
    name = request.form.get('name').lower()

    # Check if there isn't a pizza already with this name
    if is_exists(Pizza, name):
        return redirect(url_for('pizza.index'))

    pizza = Pizza(name=name)
    toppings = request.form.getlist('topping')
    toppings.sort()

    # Loop through every pizza to check if there isn't a pizza with this combination already
    pizzas = Pizza.query.all()
    is_duplicate = check_for_duplicate_toppings(pizzas, toppings)
    if is_duplicate:
        return redirect(url_for('pizza.index'))

    save(pizza, toppings)
    return redirect(url_for('pizza.index'))


@pizza.route('/edit_pizza', methods=['GET', 'POST'])
def edit_pizza():
    name = request.form.get('name').lower()
    pizza = Pizza.query.filter_by(id=request.form.get('pizzaId')).first()
    pizza_exists = db.session.query(Pizza).filter_by(name=name).first()

    # Check if there is already pizza with the same other than itself
    if pizza_exists and pizza.id != pizza_exists.id:
        return redirect(url_for('pizza.index'))

    toppings = request.form.getlist('topping')
    toppings.sort()
    pizzas = Pizza.query.filter(Pizza.id != pizza.id)
    is_duplicate = check_for_duplicate_toppings(pizzas, toppings)
    if is_duplicate:
        return redirect(url_for('pizza.index'))

    pizza.toppings.clear()
    pizza.name = name
    save(pizza, toppings)
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
    """
    Handles ajax call to get selected pizza's toppings
    :return: Pizza topping information
    """
    pizza = Pizza.query.filter_by(id=request.form.get('pizza_id')).first()
    return jsonify({
        'toppings': [topping.name for topping in pizza.toppings],
        'topping_ids': [topping.id for topping in pizza.toppings]
    })


def is_exists(model, name):
    """
    Checks to see if item already exists in database
    :param model: Model class
    :param name: Item name
    :return: Model class object
    """
    return db.session.query(model).filter_by(name=name).first()


def save(pizza, toppings):
    """
    Link many-to-many relationship and saves to database
    :param pizza: Pizza object
    :param toppings: Toppings associated with Pizza object
    """
    #
    for topping_id in toppings:
        topping = db.session.query(Topping).filter_by(id=topping_id).first()
        pizza.toppings.append(topping)

    db.session.add(pizza)
    db.session.commit()


def check_for_duplicate_toppings(pizzas, toppings):
    """
    Loop through every pizza and check if there isn't already a pizza with the same toppings
    :param pizzas: List of pizzas
    :param toppings: List of toppings
    :return: Boolean
    """
    #
    for pizza in pizzas:
        pizza_toppings = [str(topping.id) for topping in pizza.toppings]
        pizza_toppings.sort()
        if pizza_toppings == toppings:
            return True
    return False
