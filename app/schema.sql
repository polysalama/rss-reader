CREATE TABLE IF NOT EXISTS "users" (
  id SERIAL PRIMARY KEY,
  email VARCHAR,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "rss" (
  id SERIAL PRIMARY KEY,
  name VARCHAR
);

CREATE TABLE IF NOT EXISTS "rss_items" (
  pub_date DATE,
  title VARCHAR,
  description VARCHAR,
  link VARCHAR,
  rss_id INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS "users_rss" (
  user_id INTEGER REFERENCES users(id),
  rss_id INTEGER REFERENCES rss(id)
);

CREATE TABLE IF NOT EXISTS "user_logins" (
  login_date DATE,
  user_id INTEGER REFERENCES users(id)
);