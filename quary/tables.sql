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
    amount INTEGER,
    FOREIGN KEY (seller_id) REFERENCES "User"(id)
);

CREATE TABLE IF NOT EXISTS "Order"(
    id SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    date DATE,
    state TEXT,
    total INTEGER,
    amount INTEGER,
    FOREIGN KEY (user_id) REFERENCES "User"(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);

create table if not exists Cart(
    id serial not null primary key,
    user_id integer,
    date date,
    FOREIGN KEY (user_id) REFERENCES "User"(id)
);

create table if not exists CartItem(
    cart_id integer,
    product_id integer,
    amount integer,
    foreign key (cart_id) references Cart(id),
    FOREIGN KEY (product_id) REFERENCES Product(id),
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
    FOREIGN KEY (product_id) REFERENCES Product(id),
    foreign key (category_id) references Category(id),
    primary key (product_id,category_id)
);

create table if not exists Rewie(
    id serial not null primary key,
    user_id integer,
    product_id integer,
    score integer,
    rewie text,
    date date,
    FOREIGN KEY (user_id) REFERENCES "User"(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);