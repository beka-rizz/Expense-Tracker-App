from ui.app.app import start
from database.conf import config
from database.database_manager import DatabaseManager

def main():
  db = DatabaseManager(config)
  start(db)

if __name__ == '__main__':
  main()