CREATE TABLE IF NOT EXISTS "users" (
  user_id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password  bytea NOT NULL,
  created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS "rss" (
  rss_id SERIAL PRIMARY KEY,
  title TEXT,
  link TEXT
);

CREATE TABLE IF NOT EXISTS "rss_items" (
  pub_date DATE,
  title VARCHAR,
  description VARCHAR,
  link VARCHAR,
  rss_id INTEGER REFERENCES rss(rss_id)
);

CREATE TABLE IF NOT EXISTS "users_rss" (
  user_id INTEGER REFERENCES users(user_id),
  rss_id INTEGER REFERENCES rss(rss_id)
);

CREATE TABLE IF NOT EXISTS "user_logins" (
  login_date DATE,
  user_id INTEGER REFERENCES users(user_id)
);