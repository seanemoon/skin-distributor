create table account (
  id          integer primary key autoincrement,
  email       varchar(320) unique,
  salt        varchar,
  pass_hash   varchar
);

create table template (
  id          integer primary key autoincrement,
  event_id    integer references event(id) ON DELETE CASCADE,
  sender      varchar,
  subject     varchar,
  header      varchar,
  body        text,
  code_types  varchar[]
);

create table event (
  id          integer primary key autoincrement,
  name        varchar,
  account_id  integer references account(id) ON DELETE CASCADE,
  has_sent    BOOLEAN
);

CREATE TABLE recipient (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id    INTEGER REFERENCES event(id) ON DELETE CASCADE,
  email       VARCHAR(320),
  success     BOOLEAN,
  should_send BOOLEAN,
  time_sent   TIMESTAMP
);

CREATE TABLE code (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id    INTEGER REFERENCES event(id) ON DELETE CASCADE,
  name        VARCHAR,
  code        VARCHAR
);

CREATE TABLE code_assignment (
  recipient_id INTEGER REFERENCES recipient(id) ON DELETE CASCADE,
  code_id      INTEGER REFERENCES code(id) ON DELETE CASCADE
);
