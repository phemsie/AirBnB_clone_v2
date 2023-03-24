#!/usr/bin/python3
""" a script that starts a Flask web application """
from flask import Flask, render_template, abort

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def home():
    ''' returns a simple page '''
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    ''' returns a string '''
    return 'HBNB'


@app.route('/c/<text>')
def c_is_fun(text):
    ''' returns c page '''
    text = text.replace('_', ' ')
    return 'C ' + text


@app.route('/python')
@app.route('/python/<text>')
def python_is_magic(text='is cool'):
    ''' returns python page '''
    text = text.replace('_', ' ')
    return 'Python ' + text


@app.route('/number/<int:n>')
def number(n):
    ''' returns a number page '''
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    ''' returns an html page '''
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
