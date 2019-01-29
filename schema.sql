drop table if exists users;
create table users (
        id integer not null,
        name varchar not null
);

drop table if exists illusts;
create table illusts (
        id integer not null,
        number integer not null,
        name varchar not null,
        user integer not null,
        url varchar not null,
        downloaded integer not null
);

drop table if exists dailyrank;
create table dailyrank (
        id integer not null,
        ranktime date not null
);

drop table if exists bookmarks;
create table bookmarks (
        id integer not null,
        restrict integer not null,
        downloaded integer not null
);

drop table if exists options;
create table options (
        name varchar not null,
	value varchar not null
);

INSERT INTO options(name,value) values('software_version','1.0.0');
INSERT INTO options(name,value) values('database_version','1.0.0');
