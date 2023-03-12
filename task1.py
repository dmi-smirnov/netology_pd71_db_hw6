import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

BaseClass = sa_orm.declarative_base()

class Publisher(BaseClass):
  __tablename__ = 'publisher'

  id = sa.Column(sa.Integer, primary_key=True)
  name = sa.Column(sa.String(length=50), nullable=False)

class Book(BaseClass):
  __tablename__ = 'book'

  id = sa.Column(sa.Integer, primary_key=True)
  title = sa.Column(sa.String(length=50), nullable=False)
  id_publisher = \
    sa.Column(sa.Integer, sa.ForeignKey('publisher.id'), nullable=False)
  
  publisher = sa_orm.relationship(Publisher, backref='book')

class Shop(BaseClass):
  __tablename__ = 'shop'

  id = sa.Column(sa.Integer, primary_key=True)
  name = sa.Column(sa.String(length=50), nullable=False)

class Stock(BaseClass):
  __tablename__ = 'stock'

  id = sa.Column(sa.Integer, primary_key=True)
  id_book = \
    sa.Column(sa.Integer, sa.ForeignKey('book.id'), nullable=False)
  id_shop = \
    sa.Column(sa.Integer, sa.ForeignKey('shop.id'), nullable=False)
  count = sa.Column(sa.Integer, nullable=False)
  
  
  book = sa_orm.relationship(Book, backref='stock')
  shop = sa_orm.relationship(Shop, backref='stock')

class Sale(BaseClass):
  __tablename__ = 'sale'

  id = sa.Column(sa.Integer, primary_key=True)
  price = sa.Column(sa.Numeric(precision=5, scale=2), nullable=False)
  date_sale = sa.Column(sa.DateTime, nullable=False)
  id_stock = \
    sa.Column(sa.Integer, sa.ForeignKey('stock.id'), nullable=False)
  count = sa.Column(sa.Integer, nullable=False)

  stock = sa_orm.relationship(Stock, backref='sale')


def create_tables(BaseClass, engine):
  BaseClass.metadata.drop_all(engine)
  BaseClass.metadata.create_all(engine)