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
    animal_response = f'<ul>ID: {animal.id}</ul><ul>Name: {animal.name}</ul><ul>Species: {animal.species}</ul><ul>Zookeeper: {animal.zookeeper.name}</ul><ul>Enclosure: {animal.enclosure.environment}</ul>'
    response = make_response(
        animal_response,
        200
    )
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    zookeeper_response = f'<ul>ID: {zookeeper.id}</ul><ul>Name: {zookeeper.name}</ul><ul>Birthday: {zookeeper.birthday}</ul>'
    # import ipdb; ipdb.set_trace()
    animals = Animal.query.filter(Animal.zookeeper_id == id).all()
    for each in animals:
        zookeeper_response += f'<ul>Animal: {each.name}</ul>'
    response = make_response(
        zookeeper_response,
        200
    )
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    enclosure_response = f'<ul>ID: {enclosure.id}</ul><ul>Environment: {enclosure.environment}</ul><ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'
    # import ipdb; ipdb.set_trace()
    animals = Animal.query.filter(Animal.enclosure_id == id).all()
    for each in animals:
        enclosure_response += f'<ul>Animal: {each.name}</ul>'
    response = make_response(
        enclosure_response,
        200
    )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
