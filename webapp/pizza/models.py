from webapp import db


pizza_topping = db.Table(
    'pizza_topping',
    db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id')),
    db.Column('topping_id', db.Integer, db.ForeignKey('topping.id')),
    info={'bind_key': 'pizza'}
)


class Topping(db.Model):
    __bind_key__ = 'pizza'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return self.name


class Pizza(db.Model):
    __bind_key__ = 'pizza'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    toppings = db.relationship('Topping', secondary=pizza_topping, backref='pizzas')

    def __repr__(self):
        return self.name

    def get_toppings(self):
        return self.toppings
