from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    reviews = db.relationship(
        'Review',
        back_populates='customer',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    items = db.relationship(
        'Item',
        secondary='reviews',
        back_populates='customers',
        viewonly=True
    )

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    reviews = db.relationship(
        'Review',
        back_populates='item',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    customers = db.relationship(
        'Customer',
        secondary='reviews',
        back_populates='items',
        viewonly=True
    )

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=False)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey('customers.id', ondelete='CASCADE'),
        nullable=False
    )
    item_id = db.Column(
        db.Integer,
        db.ForeignKey('items.id', ondelete='CASCADE'),
        nullable=False
    )

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')