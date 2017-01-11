# tournament
This tiny project Tournament is to solve the Swiss-system planning problem using database. This project is actually from the Udacity relational database course.

For Swiss-system, please refer to WIKI https://en.wikipedia.org/wiki/Swiss-system_tournament. The core of Swiss-system is to pair two opponents based on their rankings right now. This project assumes that there are even players registered.

The database used in this project is PostgreSQL and python module psycopg2 to interact with the database. Note that the module bleach is used as well to sanitize the player name. Maybe in a real case, this is done by the upstream code. But here assume the player name is directly from user input.

BTW, supporting multiple tournaments without deleting the previous record is easy, just create another table called tournaments with id (serial), tournament_name (text) and date (date) and all the players are referencing the id from the newly added tournaments table. So that all the players are related to a specific tournament and so are the matches. Just a little bit work will be done in the CREATE VIEW act.
