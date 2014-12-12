CREATE TABLE account (
  id         INTEGER PRIMARY KEY,
  email      VARCHAR(320),
  salt       VARCHAR,
  pass_hash  VARCHAR
);

CREATE TABLE event (
  id         INTEGER PRIMARY KEY,
  account_id INTEGER REFERENCES account(id)
);

CREATE TABLE recipient (
  id         INTEGER PRIMARY KEY,
  event_id   INTEGER REFERENCES event(id),
  email      VARCHAR(320),
  success    BOOLEAN,
  time_sent  TIMESTAMP
);

CREATE TABLE code (
  recipient  integer REFERENCES recipient(id),
  name       VARCHAR,
  code       VARCHAR
);
