from wtforms_alchemy import ModelForm

from webapp.pizza.models import Topping


class ToppingForm(ModelForm):
    class Meta:
        model = Topping

