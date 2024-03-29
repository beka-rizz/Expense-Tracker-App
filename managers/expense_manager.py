import pandas as pd

from database.database_manager import DatabaseManager
from models.expense import Expense
from utils.queries import EXPENSE_QUERIES, QUERY_FOR_PLOT

from managers.category_manager import CategoryManager

class ExpenseManager():
  def __init__(self, db: DatabaseManager, user_id):
    self.db = db
    self.user_id = user_id
    self.expenses = self.get_expenses()
    self.cm = CategoryManager(db, user_id)
    self.categories = self.cm.get_categories_names_list()

  def get_category_name_by_id(self, category_id):
    return self.cm.get_category_name_by_id(category_id)
  
  def get_total_for_plot(self):
    result_set = self.db.fetch_data(QUERY_FOR_PLOT.get('GET_CATEGORIES_TOTAL'), (self.user_id,))
    to_list = [[row[0], float(row[1])] for row in result_set if result_set]
    return to_list

  def get_expenses(self):
    result_set = self.db.fetch_data(EXPENSE_QUERIES.get('GET_EXPENSES_BY_USER_ID'), (self.user_id,))
    return Expense.to_expenses_list(result_set)

  def add_expense(self, description, amount, date, category):
    insert_expense_query = EXPENSE_QUERIES.get('ADD_EXPENSE')
    self.__update(self.db.execute_query(insert_expense_query, (self.user_id, amount, description, date, self.user_id, category)))

  def delete_expense(self, expense_id):
    delete_expense_query = EXPENSE_QUERIES.get('DELETE_EXPENSE')
    self.__update(self.db.execute_query(delete_expense_query, (expense_id, self.user_id)))

  def delete_expenses(self):
    delete_expenses_query = EXPENSE_QUERIES.get('DELETE_EXPENSES')
    self.__update(self.db.execute_query(delete_expenses_query, (self.user_id,)))

  def __update(self, flag):
    if flag:
      self.expenses = self.get_expenses()
    return flag 
  
  def to_df(self):
    expenses: list[Expense] = self.get_expenses()
    data = {
      'id': [expense.id for expense in expenses],
      'description': [expense.description for expense in expenses],
      'amount': [expense.amount for expense in expenses],
      'category': [expense.category for expense in expenses],
      'date': [expense.date for expense in expenses]
    }
    df = pd.DataFrame(data)
    return df