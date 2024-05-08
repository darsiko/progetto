create table if not exists users(
	id serial not null primary key,
	name varchar(20),
	email varchar(30),
	password varchar(20),
	role varchar(10)
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
	idProduct integer,
	idUser integer,
	foreign key (idproduct) references products(id),
	foreign key (idUser) references users(id)
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

alter table users
add constraint role check (role = 'admin' or role = 'seller' or role = 'buyer');

alter table orders
add constraint data check(dataEsecuzione < dataConsegna);

insert into users(name, email, password, role)
values('leonardo', '891000@stud.unive.it', 'leonardo', 'admin');

insert into users(name, email, password, role)
values('dario', '000000@stud.unive.it', 'dario', 'admin');

insert into users(name, email, password, role)
values('andrea', '111111@stud.unive.it', 'andrea', 'admin');

