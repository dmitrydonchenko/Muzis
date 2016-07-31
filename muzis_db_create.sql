CREATE TABLE users (id varchar(100) NOT NULL, user_name varchar(100) NOT NULL, PRIMARY KEY(id));
CREATE TABLE events (id bigint NOT NULL AUTO_INCREMENT, event_name varchar(100) NOT NULL, url varchar(200), city varchar(50), PRIMARY KEY(id));
CREATE TABLE artists(id varchar(100) NOT NULL, PRIMARY KEY(id));
CREATE TABLE users_events (id bigint NOT NULL AUTO_INCREMENT, user_id varchar(100) NOT NULL, event_id bigint NOT NULL, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (event_id) REFERENCES events(id));
CREATE TABLE users_artists (id bigint NOT NULL AUTO_INCREMENT, user_id varchar(100) NOT NULL, artist_id varchar(100) NOT NULL, PRIMARY KEY(id), FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (artist_id) REFERENCES artists(id));


