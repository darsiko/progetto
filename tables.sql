create table if not exists users(
	id integer not null primary key,
	name varchar(20),
	email varchar(30),
	password varchar(20),
	role varchar(10)
);

create table if not exists products(
	id integer not null primary key,
	name varchar(20),
	description text,
	category varchar(20),
	price float,
	amount integer
);

create table if not exists shopping_cart(
	id integer not null primary key,
	idProduct integer,
	idUser integer,
	foreign key (idproduct) references products(id),
	foreign key (idUser) references users(id)
);

insert into users(id,name, email, password, role)
values(0,'leonardo', '891000@stud.unive.it', 'leonardo', 'admin');

insert into users(id,name, email, password, role)
values(1,'dario', '000000@stud.unive.it', 'dario', 'admin');

insert into users(id,name, email, password, role)
values(2,'andrea', '111111@stud.unive.it', 'andrea', 'admin');

