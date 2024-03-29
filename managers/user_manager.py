from database.database_manager import DatabaseManager
from models.user import User
from utils.input_status import INPUT_STATUS
from utils.queries import USER_QUERIES
from utils.hash_password import hash_password, check_password

class UserManager():
  def __init__(self, db: DatabaseManager):
    self.db = db
    self.users = self.get_users()

  def get_users(self):
    result_set = self.db.fetch_data(USER_QUERIES.get('GET_USERS'))
    return User.to_users_list(result_set)
  
  def get_username_by_id(self, user_id):
    user: User
    for user in self.users:
      if user.id == user_id:
        return user.username
    return None

  def create_user(self, username, password):
    """
    Creates a new user in the system.
    """
    is_valid_input_message, code = self.check_input(username, password)
    if code == 1:
      return [is_valid_input_message, code]
    if self.user_exists(username) is None:
      password = hash_password(password)
      insert_user_query = USER_QUERIES.get('ADD_USER')
      if self.__update(self.db.execute_query(insert_user_query, (username, password))):
        return INPUT_STATUS.get('USER_INSERT_SUCCESS')
      return INPUT_STATUS.get('USER_INSERT_ERROR')
    return INPUT_STATUS.get('USERNAME_EXISTS_ERROR')        

  def authenticate_user(self, username, password):
    """
    Authenticates a user based on the provided username and password.
    Returns True if authentication is successful, False otherwise.
    """
    user = self.user_exists(username)
    # print(f'Checking for existence of username: {username} -> {user}')
    if user:
      # print(f'Found user during authentication: {user.username}')
      if check_password(password, user.password.encode('utf-8')):
        return INPUT_STATUS.get('WELCOME_SUCCESS')
      return INPUT_STATUS.get('INVALID_PASSWORD_ERROR')
    return INPUT_STATUS.get('INVALID_USER_ERROR')

  def delete_user(self, user_id):
    """
    Deletes a user based on the provided user_id.
    """
    delete_user_query = USER_QUERIES.get('DELETE_USER')
    if self.__update(self.db.execute_query(delete_user_query, (user_id,))):
      return INPUT_STATUS.get('USER_DELETE_SUCCESS')
    return INPUT_STATUS.get('USER_DELETE_ERROR')

  def check_input(self, username, password):
    """
    Checks the user input
    """
    if len(username) == 0:
      return INPUT_STATUS.get('USERNAME_LENGTH_ERROR')
    if len(password) < 8:
      return INPUT_STATUS.get('PASSWORD_LENGTH_ERROR')
    return INPUT_STATUS.get('VALID_USER_INPUT')
  
  def user_exists(self, username) -> User | None:
    """
    Returns User Object if user exists, None otherwise.
    """
    for user in self.users:
      if user.username == username:
        return user
    return None
  
  def __update(self, flag):
    if flag:
      self.users = self.get_users()
    return flag 
  
  # Operations with users list saved locally
  def __find_user(self, username):
    user: User
    for user in self.users:
      if username == user.username:
        return user.id
    return -1

  def get_user_id_by_username(self, username):
    return self.__find_user(username)  

# def get_user_details(self, user_id):
  # """
  # Retrieves details of a user based on the provided user_id.
  # Returns a dictionary with user details.
  # """
  # select_user_details_query = "SELECT user_id, username FROM users WHERE user_id = %s"
  # result = self.db_manager.fetch_data(select_user_details_query, (user_id,))
  # if result:
  #     user_details = {
  #         "user_id": result[0][0],
  #         "username": result[0][1],
  #         "email": result[0][2],
  #     }
  #     return user_details
  # return None