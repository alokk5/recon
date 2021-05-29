from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


'''
CREATE TABLE user (
    id          INTEGER NOT NULL Primary Key AUTO_INCREMENT,
    client_code VARCHAR(20) not null,
    client_id   INTEGER not null references client,
	username    VARCHAR(20) not null unique,
	password    VARCHAR(60) not null unique,
	email       VARCHAR(120) not null unique,
	image_file  VARCHAR(20) not null default 'default.jpg'
);

create table post
(
	id          INTEGER not null primary key AUTO_INCREMENT,
	title       VARCHAR(100) not null,
	date_posted DATETIME not null,
	content     TEXT not null,
	user_id     INTEGER not null references user
);

create table address
(
    id          INTEGER not null primary key AUTO_INCREMENT,
    line_1      varchar(250) not null,
    line_2      varchar(250),
    line_3      varchar(250),
    city        varchar(250),
    state       varchar(250),
    country_code varchar(2) default 'US',
    postal_code varchar(10)
);

create table client
(
	id          INTEGER not null primary key AUTO_INCREMENT,
	code        varchar(10) not null,
	name        varchar(250) not null,
	legal_name  VARCHAR(250) not null,
	address_id  INTEGER references address
);

'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client_code = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.client_id}', '{self.client_code}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    legal_name = db.Column(db.String(250), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)

    def __repr__(self):
        return f"Client('{self.code}', '{self.name}', '{self.legal_name}', '{self.address_id}')"

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_1 = db.Column(db.String(250), nullable=False)
    line_2 = db.Column(db.String(250), nullable=False)
    line_3 = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    state = db.Column(db.String(250), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Post('{self.line_1}', '{self.line_2}', '{self.line_3}', '{self.city}',"\
               f" '{self.state}', '{self.country_code}', '{self.postal_code}')"


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"Bank('{self.id}', '{self.client_id}', '{self.name}')"


class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)
    aba_routing_no = db.Column(db.Integer, nullable=False)
    number = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    currency = db.Column(db.String(3), nullarble=False, default='USD')
    iban = db.Column(db.String(34), nullable=False)  #iban can be 34 characters

    def __repr__(self):
        return f"Bank Account('{self.id}', '{self.client_id}', '{self.bank_id}', "\
        f"'{self.aba_routing_no}', '{self.number}', '{self.name}', '{self.currency}', "\
        f"'{self.iban}')"

class BankAccountTxn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account_number = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(3), nullarble=False, default='USD')
    iban = db.Column(db.String(34), nullable=False)  #iban can be 34 characters
    date_value = db.Column(db.DateTime, nullable=False)
    date_transaction = db.Column(db.DateTime, nullable=False)
    bai_type_code = db.Column(db.Integer, nullable=True)
    bai_type_description = db.Column(db.String(250), nullable=True)
    amount = db.Column(db.Numeric(12,2), nullable=True)
    credit_debit = db.Column(db.String(1), nullable=True)
    amount_debit = db.Column(db.Numeric(12,2), nullable=True)
    amount_credit = db.Column(db.Numeric(12,2), nullable=True)
    liquidity_immediate = db.Column(db.Numeric(12,2), nullable=True)
    amount_day0_float = db.Column(db.Numeric(12,2), nullable=True)
    amount_day1_float = db.Column(db.Numeric(12,2), nullable=True)
    amount_day2_float = db.Column(db.Numeric(12,2), nullable=True)
    amount_day3_float = db.Column(db.Numeric(12,2), nullable=True)
    customer_ref_no = db.Column(db.String(100), nullable=True)
    bank_ref_no = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    text01 = db.Column(db.String(100), nullable=True)
    text02 = db.Column(db.String(100), nullable=True)
    text03 = db.Column(db.String(100), nullable=True)
    text04 = db.Column(db.String(100), nullable=True)
    text05 = db.Column(db.String(100), nullable=True)
    text06 = db.Column(db.String(100), nullable=True)
    text07 = db.Column(db.String(100), nullable=True)
    text08 = db.Column(db.String(100), nullable=True)
    text09 = db.Column(db.String(100), nullable=True)
    text10 = db.Column(db.String(100), nullable=True)
    text11 = db.Column(db.String(100), nullable=True)
    text12 = db.Column(db.String(100), nullable=True)
    text13 = db.Column(db.String(100), nullable=True)
    text14 = db.Column(db.String(100), nullable=True)
    text15 = db.Column(db.String(100), nullable=True)
    ach_addenda = db.Column(db.String(1000), nullable=True)
    sec_code = db.Column(db.String(100), nullable=True)
    cpty_bank_name = db.Column(db.String(100), nullable=True)
    cpty_name = db.Column(db.String(100), nullable=True)
    cpty_ach_id = db.Column(db.String(100), nullable=True)
    cpty_discretionary_data = db.Column(db.String(100), nullable=True)
    cpty_individual_id = db.Column(db.String(100), nullable=True)
    item_trace = db.Column(db.String(100), nullable=True)
    entry_description = db.Column(db.String(100), nullable=True)
    transaction_code = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        s = ""
        for attr in dir(self):
            s += f"obj.{attr} = '{getattr(obj, attr)}', "
        return f"Account Transaction({s})"

class BankAccountBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account_number = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(3), nullable=True, default='USD')
    iban = db.Column(db.String(34), nullable=False)  # iban can be 34 characters
    date_value = db.Column(db.DateTime, nullable=False)
    date_transaction = db.Column(db.DateTime, nullable=False)
    bai_type_code = db.Column(db.Integer, nullable=True)
    bai_type_description = db.Column(db.String(250), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=True)

    def __repr__(self):
        s = ""
        for attr in dir(self):
            s += f"obj.{attr} = '{getattr(obj, attr)}', "
        return f"Account Transaction({s})"

