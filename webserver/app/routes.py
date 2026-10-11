
from flask import Blueprint, render_template, request
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', result=None)


@main.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    result = execute_command(command)
    return render_template('index.html', result=result)