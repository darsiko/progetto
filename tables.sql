create table if not exists users(
	id serial not null primary key,
	name varchar(20),
	email varchar(30),
	password varchar(20),
	roles varchar(10)
);

create table if not exists products(
	id serial not null primary key,
	name varchar(20),
	description text,
	category varchar(20),
	price float,
	amount integer
);

create table if not exists shopping_cart(
	id serial not null primary key,
	last_edit date,
	userid integer,
	foreign key (userid) references users(id)
);

create table if not exists orders(
	id serial not null primary key,
	idProduct integer,
	idUser integer,
	stato text,
	dataEsecuzione date,
	dataConsegna date,
	foreign key (idproduct) references products(id),
	foreign key (idUser) references users(id)
);

create table if not exists cart_item(
	id serial not null primary key,
	name varchar(20),
	description text
);

create table if not exists category(
	id serial not null primary key,
	name varchar(20),
	description text
);

create table if not exists product_category(
	idproduct integer not null,
	idcategory integer not null,
	foreign key (idproduct) references products(id),
	foreign key (idcategory) references category(id)
);

create table if not exists reviews(
	id serial not null primary key,
	score integer,
	comment text,
	data date,
	idproduct integer,
	iduser integer,
	foreign key (idproduct) references products(id),
	foreign key (iduser) references users(id)
);

alter table users
add constraint role check (role = 'admin' or role = 'seller' or role = 'buyer');

alter table orders
add constraint data check(dataEsecuzione < dataConsegna);

alter table users
add column address text;

alter table products
add column seller serial;

alter table products
add constraint fk_id_seller
foreign key(seller)
references users(id);
