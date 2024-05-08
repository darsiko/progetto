create table if not exists users(
	id integer not null primary key,
	name varchar(20),
	email varchar(30),
	password varchar(20),
	role varchar(10)
)

