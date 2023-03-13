#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    animal_response = f'<ul><li>ID: {animal.id}</li><li>Name: {animal.name}</li><li>Species: {animal.species}</li><li>Zookeeper: {animal.zookeeper.name}</li><li>Enclosure: {animal.enclosure.environment}</li></ul>'
    response = make_response(
        animal_response,
        200
    )
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    zookeeper_response = f'<ul><li>ID: {zookeeper.id}</li><li>Name: {zookeeper.name}</li><li>Birthday: {zookeeper.birthday}</li>'
    # import ipdb; ipdb.set_trace()
    animals = Animal.query.filter(Animal.zookeeper_id == id).all()
    for each in animals:
        zookeeper_response += f'<li>Animal: {each.name}</li>'
    zookeeper_response += '</ul>'
    response = make_response(
        zookeeper_response,
        200
    )
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    enclosure_response = f'<ul><li>ID: {enclosure.id}</li><li>Environment: {enclosure.environment}</li><li>Open to Visitors: {enclosure.open_to_visitors}</li>'
    # import ipdb; ipdb.set_trace()
    animals = Animal.query.filter(Animal.enclosure_id == id).all()
    for each in animals:
        enclosure_response += f'<li>Animal: {each.name}</li>'
    enclosure_response += '</ul>'
    response = make_response(
        enclosure_response,
        200
    )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
