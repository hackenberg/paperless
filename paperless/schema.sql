DROP TRIGGER IF EXISTS t_search_ins;
DROP TRIGGER IF EXISTS t_search_upd;
DROP TRIGGER IF EXISTS t_search_del;

DROP TABLE IF EXISTS document;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS search;

CREATE TABLE account (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);

CREATE TABLE document (
  id         INTEGER   PRIMARY KEY AUTOINCREMENT,
  title      TEXT      NOT NULL UNIQUE,
  content    TEXT      NOT NULL,
  account_id INTEGER   NOT NULL,
  created    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES account (id) ON DELETE CASCADE
);

CREATE VIRTUAL TABLE search
USING FTS5 (title, content, id UNINDEXED);

CREATE TRIGGER t_search_ins
  AFTER INSERT
  ON document
BEGIN
  INSERT INTO search (title, content, id)
  VALUES (NEW.title, NEW.content, NEW.id);
END;

CREATE TRIGGER t_search_upd
  AFTER UPDATE
  ON document
BEGIN
  UPDATE search SET
    title = NEW.title,
    content = NEW.content
  WHERE id = OLD.id;
END;

CREATE TRIGGER t_search_del
  AFTER DELETE
  ON document
BEGIN
  DELETE FROM search
  WHERE id = OLD.id;
END;
