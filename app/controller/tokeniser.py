# import sqlparse


def tokenise(sql):
    pass


# def validate_sql_syntax(sql_query):
#     try:
#         # Parse the SQL query using sqlparse
#         parsed = sqlparse.parse(sql_query)
#         statements = parsed[0]
#         # If there are any parsing errors, the query is not valid
#         for token in statements.tokens:
#             if (
#                 token.ttype not in sqlparse.tokens.Whitespace
#                 and token.ttype not in sqlparse.tokens.Newline
#             ):
#                 print(token, token.ttype)
#             if (
#                 isinstance(token, sqlparse.sql.Token)
#                 and token.ttype in sqlparse.tokens.Error
#             ):
#                 return False

#         # If no parsing errors are found, the query is valid
#         return True
#     except Exception as e:
#         # An exception occurred during parsing, indicating an invalid query
#         print(e)
#         return False


# Example usage
# sql_query = (
#     "select * from my_table WHERE column_name = 'value' and column_name2 = 'value2';"
# )
# sql_query = """
# selECT
#     employees.employee_id, employees.employee_name,
#     departments.department_name
# FROM
#     employees JOIN
#     departments
# ON employees.department_id = departments.department_id;
# """
# is_valid = validate_sql_syntax(
#     sqlparse.format(sql_query, reindent=True, keyword_case="upper")
# )
# if is_valid:
#     print("SQL query has valid syntax.")
# else:
#     print("SQL query has syntax errors.")

# first = sql_query
# print()


# import sqlparse


# def tokenise(sql):
#     return sqlparse.parse(sql)[0].tokens


# def get_tokens(sql):
#     tokens = tokenise(sql)
#     return [token for token in tokens if not token.is_whitespace]


# def get_token_type(token):
#     return token.ttype


# def get_token_value(token):
#     return token.value
