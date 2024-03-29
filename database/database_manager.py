import psycopg2

class DatabaseManager():    
  def __init__(self, config):
    self.conn = psycopg2.connect(**config)
    self.cur = self.conn.cursor()
    print("Successfully connected to the database!")

  # select
  def fetch_data(self, query, values = None):
    try:
      if values:
        self.cur.execute(query, values)
      else:
        self.cur.execute(query)
      result = self.cur.fetchall()
      return result
    except Exception as e:
      print(f"Error fetching data: {e}")
      return None

  # insert, delete, update
  def execute_query(self, query, values = None):
    try:
      if values:
        self.cur.execute(query, values)
      else:
        self.cur.execute(query)
      self.conn.commit()

      # Check if the query contains "RETURNING" keyword
      if "RETURNING" in query:
        return self.cur.fetchone()[0]  # Assuming the first column contains the returned value
      return True
    except Exception as e:
      print(f"Error executing query: {e}")
      self.conn.rollback()
      return False

  def close_connection(self):
    try:
      print("Connection closed successfully!")
      self.conn.close()
    except Exception as e:
      print(f"Error closing connection: {e}")