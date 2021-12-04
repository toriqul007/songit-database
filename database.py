# improt the sqlite module
import sqlite3

database_name = 'music.db'

# helper function to update database

def query(query, values={}):
  if query.strip().upper().startswith('SELECT'):
    return get(query, values)
  else:
    return run(query, values)

def run(query, values={}):
    '''
      Helper function to update database.

      :param: query: The SQL-query to execute.
      :param: values: The values to be used with the query. (default = {})
      :return: The autoincremented 'id' from an INSERT
    '''
    # connect to database (creates if not exists)
    conn = sqlite3.connect(database_name)
    # open a cursor to the database
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    if query.strip().upper().startswith('DELETE'):
      cur.execute('PRAGMA foreign_keys = ON')

    # run query with values and execute
    result = cur.execute(query, values)
    # must commit queries that does changes to the database
    conn.commit()
    # close connection
    conn.close()
    # return autoincremented id
    return result.lastrowid


def get(query, values={}):
    '''
      Helper function to get data from database.

      :param: query: The SQL-query to execute.
      :param: values: The values to be used with the query. (default = {})
      :return: The results from the query as a list of Rows
    '''
    # connect to database (creates if not exists)
    conn = sqlite3.connect(database_name)
    # convert results to dict-like objects
    conn.row_factory = sqlite3.Row
    # open a cursor to the database
    cur = conn.cursor()
    # run query with values and execute as a prepared statement
    cur.execute(query, values)
    # get results from executed query
    results = cur.fetchall()
    # close connection
    conn.close()
    # return results as a list of Rows
    return results
