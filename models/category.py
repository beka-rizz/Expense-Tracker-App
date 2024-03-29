class Category():
  def __init__(self, id, name):
    self.id = id
    self.name = name

  @staticmethod
  def get_columns():
    return ['Id', 'Name']

  def __str__(self) -> str:
    return f'Category(name: {self.name})'

  @classmethod
  def to_categories_list(cls, result_set):
    categories = []
    
    if result_set is None:
      return categories
    for row in result_set:
      category = cls(
        id=row[0],
        name=row[1],
      )
      categories.append(category)
    return categories
  
  @classmethod
  def to_categories_names_list(cls, result_set):
    names: list[Category] = []
    
    if result_set is None:
      return names
    category: Category
    for category in result_set:
      names.append(category.name)
    return names
  
  