CREATE TABLE "users" (
  id SERIAL PRIMARY KEY,
  email VARCHAR,
  created_at TIMESTAMP
);

CREATE TABLE "rss" (
  id SERIAL PRIMARY KEY,
  name VARCHAR
);

CREATE TABLE "rss_items" (
  pub_date DATE,
  title VARCHAR,
  description VARCHAR,
  link VARCHAR,
  rss_id INTEGER REFERENCES users(id)
);

CREATE TABLE "users_rss" (
  user_id INTEGER REFERENCES users(id),
  rss_id INTEGER REFERENCES rss(id)
);

CREATE TABLE "user_logins" (
  login_date DATE,
  user_id INTEGER REFERENCES users(id)
);