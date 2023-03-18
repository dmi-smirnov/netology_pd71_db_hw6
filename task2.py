import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from task1 import Publisher, Book, Stock, Sale, Shop

def get_publisher_sales(engine):
  input_str = input('Введите id или имя издателя:\n')

  Session = sa_orm.sessionmaker(bind=engine)
  with Session() as session:
    query =session.query(
      Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale
    ).join(Publisher).join(Stock).join(Shop).join(Sale)
    if input_str.isdigit():
      publisher_id = int(input_str)
      query = query.filter(Publisher.id == publisher_id)
    else:
      publisher_name = input_str
      query = query.filter(Publisher.name == publisher_name)

    query_result = query.all()
  
    max_len_book = Book.title.type.length
    max_len_shop = Shop.name.type.length
    max_len_amt = 10

    for book, shop, price, count, date in query_result:
      amt_str = str(price * count)
      date_str = str(date)[:19]
      print(f'{book.ljust(max_len_book)} | '
            f'{shop.ljust(max_len_shop)} | '
            f'{amt_str.ljust(max_len_amt)} | '
            f'{date_str}')

def main():
  db_type = 'postgresql'
  db_host_addr = '192.168.60.11'
  db_host_port = '5432'
  db_name = 'netology_pd71_db_hw6'
  db_user = 'postgres'
  db_pwd = 'pgpg'

  dsn = \
    f'{db_type}://{db_user}:{db_pwd}@{db_host_addr}:{db_host_port}/{db_name}'
  engine = sa.create_engine(dsn)

  get_publisher_sales(engine)

main()