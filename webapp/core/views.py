import os

from flask import Blueprint, render_template
from flask_login import login_required

# import RPi.GPIO as gpio

main = Blueprint('main', __name__, template_folder='templates')

# INPUT20 = 20
# INPUT21 = 21


# gpio.setmode(gpio.BCM)
# gpio.setup(INPUT20, gpio.OUT)
# gpio.setup(INPUT21, gpio.OUT)
#
# gpio.output(INPUT20, False)
# gpio.output(INPUT21, True)


@main.route('/')
def index():
    return render_template(
        'main/index.html',
        email=os.getenv('EMAIL')
    )


@main.route('/controls')
@login_required
def controls():
    return render_template('main/controls.html')


@main.route('/open_door')
@login_required
def open_door():
    # gpio.output(INPUT20, True)
    # gpio.output(INPUT21, True)
    return render_template('main/controls.html')


@main.route('/close_door')
@login_required
def close_door():
    # gpio.output(INPUT20, False)
    # gpio.output(INPUT21, False)
    return render_template('main/controls.html')


@main.route('/stop')
@login_required
def stop():
    # gpio.output(INPUT20, False)
    # gpio.output(INPUT21, True)
    return render_template('main/controls.html')
