import sqlalchemy
import mysql.connector


db = sqlalchemy.create_engine(
    "mysql+mysqlconnector://root:password@localhost:3306/fastapi",
    echo=True,
    future=True)




