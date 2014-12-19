CREATE TABLE account (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  email       VARCHAR(320) UNIQUE,
  salt        VARCHAR,
  pass_hash   VARCHAR
);

CREATE TABLE template (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id    INTEGER REFERENCES event(id),
  sender      VARCHAR,
  subject     VARCHAR,
  header      VARCHAR,
  body        TEXT,
  code_types  VARCHAR[]
);

CREATE TABLE event (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        VARCHAR,
  account_id  INTEGER REFERENCES account(id)
);

CREATE TABLE recipient (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id    INTEGER REFERENCES event(id),
  email       VARCHAR(320),
  success     BOOLEAN,
  should_send BOOLEAN,
  time_sent   TIMESTAMP
);

CREATE TABLE code (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id    INTEGER REFERENCES event(id),
  name        VARCHAR,
  code        VARCHAR
);

CREATE TABLE code_assignment (
  recipient_id INTEGER REFERENCES recipient(id),
  code_id      INTEGER REFERENCES code(id)
);
