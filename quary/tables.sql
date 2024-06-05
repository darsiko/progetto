CREATE SEQUENCE esempio_id_seq;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(20),
    email VARCHAR(30),
    password TEXT,
    address VARCHAR(20),
    role VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL NOT NULL PRIMARY KEY,
    seller_id INTEGER,
    name VARCHAR(20),
    description TEXT,
    category VARCHAR(20),
    price FLOAT,
    amount INTEGER,
    aviable INTEGER,
    FOREIGN KEY (seller_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    date DATE,
    state TEXT,
    total INTEGER,
    amount INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

create table if not exists carts(
    id serial not null primary key,
    user_id integer,
    last_modify date,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

create table if not exists cart_elements(
    cart_id integer,
    product_id integer,
    amount integer,
    foreign key (cart_id) references carts(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    primary key (cart_id, product_id)
);

create table if not exists categories(
    id serial not null primary key,
    name varchar(20),
    description text
);

create table if not exists products_categories(
    product_id integer,
    category_id integer,
    FOREIGN KEY (product_id) REFERENCES products(id),
    foreign key (category_id) references categories(id),
    primary key (product_id,category_id)
);

create table if not exists rewies(
    id serial not null primary key,
    user_id integer,
    product_id integer,
    score integer,
    rewie text,
    date date,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);