import pytz
import sqlalchemy
from sqlalchemy import create_engine, and_, or_, Unicode, DateTime, Boolean
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

print(sqlalchemy.__version__)

engine = create_engine('sqlite:///database/customers.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    age = Column(Integer)


def print_all_customers(customers):
    for customer in customers:
        print_customer(customer)


def print_customer(customer):
    print("[ID: {0}] Name: {1} Address: {2}, Email: {3}, Age: {4}".format(
        customer.id,
        customer.name,
        customer.address,
        customer.email,
        customer.age
    ))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode(128), nullable=False)
    name = Column(Unicode(128))
    password = Column(Unicode(128))
    affiliation = Column(Unicode(512))

    created_on_datetime = datetime.now(pytz.timezone('Asia/Seoul'))
    created_on = Column(DateTime, default=created_on_datetime)
    created_on_str = Column(Unicode(128), default=created_on_datetime.strftime('%Y년 %m월 %d일 %H시 %M분'.encode('unicode-escape').decode()))

    is_active = Column(Boolean, default=True)

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'affiliation': self.affiliation,
            'created_on': self.created_on_str,
            'is_active': self.is_active
        }

    def __repr__(self):
        r = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'affiliation': self.affiliation,
            'created_on': self.created_on_str,
            'is_active': self.is_active
        }
        return str(r)


Base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
db_session = db_session()


## USER
user_email = "hong@gmail.com"
q = db_session.query(User).filter(User.email == user_email)
user = q.first()
if user is None:
    user = User(name="홍길동", email=user_email, affiliation="KOREATECH")
    user.set_password("1234")
    db_session.add(user)
    db_session.commit()
    print("Admin User (Name: {0}) is inserted".format(user.name))


def main():
    count = db_session.query(Customer).count()
    print("### There are {0} rows in the table.".format(count))

    if count != 0:
        db_session.query(Customer).delete()
        count = db_session.query(Customer).count()
        print("### There are {0} rows in the table after performing 'delete'.".format(count))


    ## INSERT (POST)
    print("\n### db_session.add()")
    customer = Customer(name='김철수', address='서울 송파구', email='cskim@gmail.com', age=20)
    db_session.add(customer)
    db_session.commit()

    print("### db_session.add_all()")
    db_session.add_all([
        Customer(name='이나라', address='대전 유성구', email='nrlee@gmail.com', age=21),
        Customer(name='나길동', address='대구 달서구', email='gdna@gmail.com', age=22),
        Customer(name='배칠수', address='인천 부평구', email='csbae@gmail.com', age=19)]
    )
    db_session.commit()

    count = db_session.query(Customer).count()
    print("### There are {0} rows in the table after performing 'add' and 'add_all'.".format(count))


    ## SELECT (GET)
    print("\n### db_session.query(Customer).all()")
    customers = db_session.query(Customer).all()
    print_all_customers(customers)

    print("\n### db_session.query(Customer).filter(Customer.id == 2)")
    customers = db_session.query(Customer).filter(Customer.id == 2)
    print_all_customers(customers)

    print("\n### db_session.query(Customer).filter(Customer.id != 2)")
    customers = db_session.query(Customer).filter(Customer.id != 2)
    print_all_customers(customers)

    print("\n### db_session.query(Customer).first()")
    customer = db_session.query(Customer).first()
    print_customer(customer)

    print("\n### db_session.query(Customer).filter(Customer.name.like('%수%'))")
    customers = db_session.query(Customer).filter(Customer.name.like('%수%'))
    print_all_customers(customers)

    print("\n### db_session.query(Customer).filter(Customer.id.in_([2, 3]))")
    customers = db_session.query(Customer).filter(Customer.id.in_([2, 3]))
    print_all_customers(customers)

    print("\n### and_")
    customers = db_session.query(Customer).filter(and_(Customer.id >= 3, Customer.name.like('%수%')))
    print_all_customers(customers)

    print("\n### or_")
    customers = db_session.query(Customer).filter(or_(Customer.id >= 3, Customer.name.like('%수%')))
    print_all_customers(customers)

    print("\n### db_session.query(Customer).get(3)")
    customer = db_session.query(Customer).get(3)
    print_customer(customer)


    ## UPDATE (PUT)
    customer.age = 25
    db_session.commit()

    print("\n### db_session.query(Customer).get(3) after update")
    customer = db_session.query(Customer).get(3)
    print_customer(customer)

    db_session.query(Customer).update({Customer.age: 23}, synchronize_session=False)
    db_session.commit()

    print("\n### db_session.query(Customer).all() after bulk update")
    customers = db_session.query(Customer).all()
    print_all_customers(customers)


    ## DELETE (DELETE)
    print("\n### delete the customer with id=3")
    db_session.query(Customer).filter(Customer.id == 3).delete()
    db_session.commit()

    print("\n### db_session.query(Customer).all() after deleting")
    customers = db_session.query(Customer).all()
    print_all_customers(customers)

    ## USER
    user_email = "hong@gmail.com"
    q = db_session.query(User).filter(User.email == user_email)
    user = q.first()
    print(user)
    if user is None:
        user = User(name="홍길동", email=user_email, affiliation="KOREATECH")
        user.set_password("1234")
        db_session.add(user)
        db_session.commit()
        print("Admin User (Name: {0}) is inserted".format(user.name))


if __name__ == "__main__":
    main()