import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import task1 as models

def get_publisher_sales(engine):
  input_str = input('Введите id или имя издателя:\n')

  Session = sa_orm.sessionmaker(bind=engine)
  with Session() as session:
    query = session.query(models.Sale)\
                   .join(models.Stock)\
                   .join(models.Shop)\
                   .join(models.Book)\
                   .join(models.Publisher)
    if input_str.isdigit():
      publisher_id = int(input_str)
      query = query.filter(models.Publisher.id == publisher_id)
    else:
      publisher_name = input_str
      query = query.filter(models.Publisher.name == publisher_name)

    query_result = query.all()
  
    max_len_book_name = 0
    max_len_shop_name = 0
    max_len_sale_price = 0
    for sale in query_result:
      book_name = sale.stock.book.title
      shop_name = sale.stock.shop.name
      sale_price_str = str(sale.price)
      sale_date = sale.date_sale
      if len(book_name) > max_len_book_name:
        max_len_book_name = len(book_name)
      if len(shop_name) > max_len_shop_name:
        max_len_shop_name = len(shop_name)
      if len(sale_price_str) > max_len_sale_price:
        max_len_sale_price = len(sale_price_str)

    for sale in query_result:
      book_name = sale.stock.book.title
      shop_name = sale.stock.shop.name
      sale_price_str = str(sale.price)
      sale_date = sale.date_sale
      print(f'{book_name.ljust(max_len_book_name)} | '
            f'{shop_name.ljust(max_len_shop_name)} | '
            f'{sale_price_str.ljust(max_len_sale_price)} | '
            f'{sale_date}')

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