#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

## use bleach module to sanitize the input of username
import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS num FROM players")
    """Get first columen of the first row"""
    num = cursor.fetchall()[0][0]
    conn.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    sanitizedName = bleach.clean(name) ## avoid script injection attack
    conn = connect()
    cursor = conn.cursor()
    ## avoid SQL injection attack
    cursor.execute("INSERT INTO players (name) VALUES (%s)", (sanitizedName,))
    conn.commit()
    conn.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    ## Create two views, one for id, name and wins; the other for matches.
    ## Then create a third view to combine the query results from the two views.
    ## The code here directly select results from the combined view.
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player_standings")
    results = cursor.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO matches (player_a, player_b) VALUES (%s, %s)",\
        (winner, loser))
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ps = playerStandings()
    pairings = []
    ## use the adjacent two rows to make a pair
    for i in range(0, len(ps), 2):
        pairings.append((ps[i][0], ps[i][1], ps[i+1][0], ps[i+1][1]))
    return pairings


