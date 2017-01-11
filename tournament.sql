-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP VIEW IF EXISTS player_standings;
DROP VIEW IF EXISTS wins_view;
DROP VIEW IF EXISTS matches_view;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
	id serial PRIMARY KEY,
	name text
);

CREATE TABLE matches (
	id serial PRIMARY KEY,
	player_a int REFERENCES players (id),
	player_b int REFERENCES players (id)
);

-- View for id, name and wins
CREATE VIEW wins_view AS
SELECT p.id, p.name, COUNT(m.player_a) AS wins
FROM players AS p LEFT JOIN matches AS m
ON p.id = m.player_a
GROUP BY p.id;

-- View for id and games played
CREATE VIEW matches_view AS
SELECT p.id, COUNT(m.player_a + m.player_b) AS games
FROM players AS p LEFT JOIN matches AS m
ON p.id = m.player_a OR p.id = m.player_b
GROUP BY p.id;

-- Combined view to hold id, name, wins and games played, that is player_standings
CREATE VIEW player_standings AS
SELECT w.id, w.name, w.wins, m.games
FROM wins_view AS w, matches_view AS m
WHERE w.id = m.id
ORDER BY w.wins DESC;