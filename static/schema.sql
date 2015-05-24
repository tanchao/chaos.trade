-- stock info
drop table if exists stocks;
create table stocks (
  id integer primary key autoincrement,
  symbol text not null,
  name text not null,
  type text not null,
  area text,
  concept text,
  other text
);

-- daily price info
drop table if exists prices;
create table stocks (
  id integer primary key autoincrement,
  symbol text not null,
  name text not null,
  price float not null,
  date text not null,
  time text not null,
  yest_end float not null,
  today_start float not null,
  today_end float not null,
  high float not null,
  low float not null,
  price float not null,
  yest_end float not null,
  other text
);

-- history price info
create table stock_symbol (
  id integer primary key autoincrement,
  symbol text not null,
  name text not null,
  date text not null,
  time text not null,
  price float not null,
  yest_end float not null,
  today_start float not null,
  today_end float not null,
  high float not null,
  low float not null,
  price float not null,
  yest_end float not null,
  ,
  other text
);