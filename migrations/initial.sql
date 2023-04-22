create table if not exists users
(
    id serial primary key,
    username text unique not null,
    password text not null
);
create table if not exists product
(
    id serial primary key,
    name text unique not null,
    price int not null,
    foto_loc text
);
create table if not exists follow
(
    user_id int references users (id) on delete cascade not null,
    prod_id int references product (id) on delete cascade not null,
    unique (user_id,prod_id)
);


