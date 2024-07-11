CREATE SEQUENCE esempio_id_seq;

CREATE TABLE IF NOT EXISTS "User"(
    id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(20),
    email VARCHAR(30),
    password TEXT,
    address VARCHAR(20),
    role VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS Product(
    id SERIAL NOT NULL PRIMARY KEY,
    seller_id INTEGER,
    name VARCHAR(20),
    description TEXT,
    price FLOAT,
    amount INTEGER
);

CREATE TABLE IF NOT EXISTS "Order"(
    id SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    date DATE,
    state TEXT,
    total INTEGER,
    amount INTEGER
);

create table if not exists Cart(
    id serial not null primary key,
    user_id integer,
    date date
);

create table if not exists CartItem(
    cart_id integer,
    product_id integer,
    amount integer,
    primary key (cart_id, product_id)
);

create table if not exists Category(
    id serial not null primary key,
    name varchar(20),
    description text
);

create table if not exists ProductCategory(
    product_id integer,
    category_id integer,
    primary key (product_id,category_id)
);

create table if not exists Rewie(
    id serial not null primary key,
    user_id integer,
    product_id integer,
    score integer,
    rewie text,
    date date
);

insert into category (name, description)
values ('Electronics', 'Televisions, smartphones, computers and accessories, cameras and camcorders'),
       ('Clothing','Men, Women, Children, Accessories'),
       ('Home and kitchen', 'Furnishings, kitchenware, home decor, lighting'),
       ('Books', 'Fiction, non-fiction, children books, textbooks'),
       ('Health and beauty','Skin care products, hair products, nutritional supplements, fitness products'),
       ('Toys','Educational toys, board games, dolls and soft toys, outdoor games'),
       ('Sport and free time','Sports equipment, sportswear, outdoor activities, camping accessories'),
       ('Car and motorcycle','Car parts, accessories for cars, motorcycles and scooters, motorcycle accessories');


