create database MyZone;
use MyZone;

# 实体集
create table user(
    id char(10) primary key,
    name varchar(50) not null,
    password varchar(50) not null,
    introduction varchar(400)
);

create table comment(
    id char(10) primary key,
    text varchar(400) not null,
    time timestamp not null
);

create table message(
    id char(10) primary key,
    text varchar(400) not null,
    time timestamp not null
);

create table article(
    id char(10) primary key,
    title varchar(100) not null,
    text varchar(10000) not null,
    time timestamp not null,
    authority int not null
);

create table moment(
    id char(10) primary key,
    text varchar(400) not null,
    time timestamp not null,
    authority int not null
);

create table tag(
    id char(10) primary key,
    text varchar(50) not null
);

create table image(
    id char(10) primary key,
    text varchar(400)
);

create table album(
    id char(10) primary key,
    title varchar(50) not null
);


# 联系集
create table com_editor(
    com_id char(10) primary key references comment(id),
    user_id char(10) not null references user(id)
);

create table mess_editor(
    mess_id char(10) primary key references message(id),
    user_id char(10) not null references user(id)
);

create table friend(
    id char(10) primary key  references user(id),
    friend_id char(10) not null references user(id)
);

create table arti_com(
    com_id char(10) primary key references comment(id),
    arti_id char(10) not null references article(id)
);

create table mom_mess(
    mess_id char(10) primary key references message(id),
    mom_id char(10) not null references moment(id)
);

create table arti_editor(
    arti_id char(10) primary key references article(id),
    user_id char(10) not null references user(id)
);

create table mom_editor(
    mom_id char(10) primary key references moment(id),
    user_id char(10) not null references user(id)
);

create table arti_tag(
    id char(10) primary key,
    arti_id char(10) not null references article(id),
    tag_id char(10) not null references tag(id)
);

create table mom_tag(
    id char(10) primary key,
    mom_id char(10) not null references moment(id),
    tag_id char(10) not null references tag(id)
);

create table album_editor(
    album_id char(10) primary key references album(id),
    user_id char(10) not null references user(id)
);

create table album_image(
    image_id char(10) primary key references image(id),
    album_id char(10) not null references album(id)
);