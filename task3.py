import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import os
import json
import task1 as models

def import_json_data(BaseClass, engine, json_file_path):
  if not os.path.exists(json_file_path):
    print(f'Ошибка: не найден файл {json_file_path}')
    return

  with open(json_file_path) as json_file:
    json_data = json.load(json_file)

  Session = sa_orm.sessionmaker(bind=engine)
  with Session() as session:
    for record in json_data:
      table_name = record['model']
      for TableClass in BaseClass.__subclasses__():
        if TableClass.__tablename__ == table_name:
          record_fields = {'id': record['pk']}
          record_fields.update(record['fields'])
          session.add(TableClass(**record_fields))
          break
    session.commit()

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

  BaseClass = models.BaseClass
  models.create_tables(BaseClass, engine)

  code_dir_path = os.path.dirname(__file__)
  json_file_dir_name = 'fixtures'
  json_file_name = 'tests_data.json'
  json_file_path = os.path.join(
    code_dir_path,
    json_file_dir_name,
    json_file_name
  )
  
  import_json_data(BaseClass, engine, json_file_path)

main()