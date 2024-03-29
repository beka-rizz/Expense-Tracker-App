class User():
  def __init__(self, id, username, password):
    self.id = id
    self.username = username
    self.password = password

  def __str__(self) -> str:
    return f"User(id: {self.id}, username: {self.username})"

  @staticmethod
  def get_columns():
    return ['Id', 'Name', 'Password']

  @classmethod
  def to_users_list(cls, result_set):
    users = []
    
    if result_set is None:
      return users
    for row in result_set:
      user = cls(
        id=row[0],
        username=row[1],
        password=row[2],
      )
      users.append(user)
    return users
