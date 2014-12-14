CREATE TABLE account (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  email      VARCHAR(320) UNIQUE,
  salt       VARCHAR,
  pass_hash  VARCHAR
);

CREATE TABLE event (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       VARCHAR,
  account_id INTEGER REFERENCES account(id)
);

CREATE TABLE recipient (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id   INTEGER REFERENCES event(id),
  email      VARCHAR(320),
  success    BOOLEAN,
  time_sent  TIMESTAMP
);

CREATE TABLE code (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  recipient  INTEGER REFERENCES recipient(id),
  name       VARCHAR,
  code       VARCHAR
);
