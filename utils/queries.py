USER_QUERIES = {
  'ADD_USER' : "INSERT INTO users (username, password) VALUES (%s, %s);",
  # 'GET_USER' : "SELECT password FROM users WHERE username = %s",
  'GET_USERS' : "SELECT * FROM users",
  # 'GET_USERNAME' : "SELECT id FROM users WHERE username = %s",
  'DELETE_USER' : "DELETE FROM users WHERE id = %s",
}

EXPENSE_QUERIES = {
  'GET_EXPENSES_BY_USER_ID' : """
    SELECT
      expenses.id,
      expenses.user_id,
      expenses.amount,
      expenses.description,
      expenses.date,
      categories.name
    FROM
      expenses
    JOIN
      categories ON expenses.category_id = categories.id
    WHERE
      expenses.user_id = %s
  """,
  # 'GET_EXPENSE_BY_ID' : "SELECT * FROM expenses WHERE id = %s AND user_id = %s",
  'ADD_EXPENSE' : """
    INSERT INTO expenses (user_id, amount, description, date, category_id)
      VALUES (
        %s,
        %s,
        %s,
        %s,
        (SELECT category_id FROM user_categories uc, categories c WHERE c.id = uc.category_id and user_id = %s and c.name = %s)
    )
  """,
  # 'UPDATE_EXPENSE_NAME' : "UPDATE expenses SET description = %s WHERE id = %s AND user_id = %s",
  # 'UPDATE_EXPENSE_AMOUNT' : "UPDATE expenses SET amount = %s WHERE id = %s AND user_id = %s",
  # 'UPDATE_EXPENSE_DATE' : "UPDATE expenses SET date = %s WHERE id = %s AND user_id = %s",
  'DELETE_EXPENSE' : "DELETE FROM expenses WHERE id = %s AND user_id = %s",
  'DELETE_EXPENSES' : 'DELETE FROM expenses WHERE user_id = %s',
  'SORT_BY_DATE': """
    SELECT
      expenses.id,
      expenses.user_id,
      expenses.amount,
      expenses.description,
      expenses.date,
      categories.name
    FROM
      expenses
    JOIN
      categories ON expenses.category_id = categories.id
    WHERE
      expenses.user_id = %s
    ORDER BY
      date;
  """,
  'SORT_BY_AMOUNT': """
    SELECT
      expenses.id,
      expenses.user_id,
      expenses.amount,
      expenses.description,
      expenses.date,
      categories.name
    FROM
      expenses
    JOIN
      categories ON expenses.category_id = categories.id
    WHERE
      expenses.user_id = %s
    ORDER BY
      amount;
  """,
}

USER_CATEGORY_QUERIES = {
  'ADD_CATEGORY' : "INSERT INTO user_categories (user_id, category_id) VALUES (%s, %s)",
  'GET_CATEGORIES_BY_USER_ID' : """
    SELECT categories.id, categories.name
      FROM categories
      JOIN user_categories ON categories.id = user_categories.category_id
      WHERE user_categories.user_id = %s
  """,
  'UPDATE_CATEGORY': """
    UPDATE categories SET name = %s WHERE id = %s
      AND id IN (SELECT category_id FROM user_categories WHERE user_id = %s)
  """,
  'DELETE_CATEGORY' : """
    DELETE FROM categories WHERE id = %s 
      AND id IN (SELECT category_id FROM user_categories WHERE user_id = %s)
  """,
}


QUERY_FOR_PLOT = {
  "GET_CATEGORIES_TOTAL": """
    SELECT categories.name AS category_name, COALESCE(SUM(expenses.amount), 0) AS total_amount
    FROM categories
    LEFT JOIN expenses ON categories.id = expenses.category_id
    WHERE expenses.user_id = %s
    GROUP BY categories.name;
"""
}
# When we insert category:
# 1. We insert it to categories table;
# 2. Then insert it to user_categories passing the id from categories table;
CATEGORY_QUERIES = {
  'GET_CATEGORIES' : "SELECT id, name FROM categories",
  'GET_CATEGORY_BY_ID' : "SELECT * FROM categories WHERE id = %s",
  'ADD_CATEGORY' : "INSERT INTO categories (name) VALUES (%s) RETURNING id",
  'UPDATE_CATEGORY_NAME' : "UPDATE categories SET name = %s WHERE id = %s",
  'DELETE_CATEGORY' : "DELETE FROM categories WHERE id = %s",
}