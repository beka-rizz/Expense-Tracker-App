class Expense():
  def __init__(self, id, user_id, category, amount, description, date):
    self.id = id
    self.user_id = user_id
    self.amount = amount
    self.description = description
    self.date = date
    self.category = category

  def __str__(self) -> str:
    return f'Expense(description: {self.description}, amount: W{self.amount}, date: {self.date})'

  @staticmethod
  def get_columns():
    return ['Id', 'Description', 'Amount', 'Date', 'Category']

  @classmethod
  def to_expenses_list(cls, result_set):
    expenses = []
    
    if result_set is None:
      return expenses
    for row in result_set:
      expense = cls(
        id=row[0],
        user_id=row[1],
        amount = row[2],
        description = row[3],
        date = row[4],
        category = row[5]
      )
      expenses.append(expense)
    return expenses