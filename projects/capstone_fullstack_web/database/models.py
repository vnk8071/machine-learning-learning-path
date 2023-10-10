import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=None):
    app.config.from_object('config')
    if database_path is not None:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    return db


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    drink_water = Drink(
        title='water',
        recipe='[{"name": "water", "color": "blue", "parts": 1}]'
    )

    drink_lemonade = Drink(
        title='lemonade',
        recipe='[{"name": "lemonade", "color": "yellow", "parts": 1}]'
    )

    ingredient_water = Ingredient(
        name='water',
        density='100%'
    )

    ingredient_lemonade = Ingredient(
        name='lemonade',
        density='80%'
    )

    new_property_water = Property.insert().values(
        drink_id=drink_water.id,
        ingredient_id=ingredient_water.id,
    )

    new_property_lemonade = Property.insert().values(
        drink_id=drink_water.id,
        ingredient_id=ingredient_water.id,
    )

    drink_water.insert()
    drink_lemonade.insert()
    ingredient_water.insert()
    ingredient_lemonade.insert()
    db.session.execute(new_property_water)
    db.session.execute(new_property_lemonade)
    db.session.commit()


Property = db.Table(
    'Property', db.Model.metadata,
    Column('drink_id', Integer, db.ForeignKey('drinks.id')),
    Column('ingredient_id', Integer, db.ForeignKey('ingredients.id'))
)

'''
Ingredient
a persistent ingredient entity, extends the base SQLAlchemy Model
'''


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    density = Column(String(4), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'density': self.density
        }


'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''


class Drink(db.Model):
    __tablename__ = 'drinks'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    recipe = Column(String(180), nullable=False)
    ingredients = db.relationship(
        'Ingredient',
        secondary=Property,
        backref=db.backref('drinks', lazy=True)
    )

    '''
    short()
        short form representation of the Drink model
    '''

    def short(self):
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']}
                        for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': self.recipe
        }
