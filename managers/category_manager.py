from database.database_manager import DatabaseManager
from utils.queries import USER_CATEGORY_QUERIES, CATEGORY_QUERIES
from models.category import Category

# We create an instance of class when User got successful authentication

class CategoryManager():
  def __init__(self, db: DatabaseManager, user_id):
    self.db = db
    self.user_id = user_id
    self.categories = self.get_categories()
  
  def get_categories(self):
    result_set = self.db.fetch_data(USER_CATEGORY_QUERIES.get('GET_CATEGORIES_BY_USER_ID'), (self.user_id,))
    return Category.to_categories_list(result_set)

  def get_categories_names_list(self):
    return Category.to_categories_names_list(self.get_categories())

  def add_category(self, category_name):
    insert_category_query = CATEGORY_QUERIES.get('ADD_CATEGORY')
    category_id = self.db.execute_query(insert_category_query, (category_name,))
    if category_id:
      # category_id = self.get_category_id_by_name(category_name)
      insert_user_category_query = USER_CATEGORY_QUERIES.get('ADD_CATEGORY')
      self.update(self.db.execute_query(insert_user_category_query, (self.user_id, category_id)))

  def update_category_name(self, category_id, new_name):
    update_category_query = USER_CATEGORY_QUERIES.get('UPDATE_CATEGORY')
    self.update(self.db.execute_query(update_category_query, (new_name, category_id, self.user_id)))

  def delete_category(self, category_id):
    delete_category_query = USER_CATEGORY_QUERIES.get('DELETE_CATEGORY')
    self.update(self.db.execute_query(delete_category_query, (category_id, self.user_id)))

  def get_all_categories(self):
    select_all_categories_query = CATEGORY_QUERIES.get('GET_CATEGORIES')
    result_set = self.db.fetch_data(select_all_categories_query)
    return Category.to_categories_list(result_set)
  
  def update(self, flag):
    if flag:
      self.categories = self.get_categories()
    return flag
  
  def __find_cat_id(self, cat_name):
    cat: Category
    for cat in self.get_all_categories():
      if cat.name == cat_name:
        return cat.id
    return -1
  
  def __find_cat_name(self, cat_id):
    cat: Category
    for cat in self.get_all_categories():
      if cat.id == cat_id:
        return cat.id
    return -1
  
  def get_category_id_by_name(self, cat_name):
    return self.__find_cat_id(cat_name)  

  def get_category_name_by_id(self, cat_id):
    return self.__find_cat_name(cat_id)  