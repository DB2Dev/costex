import sqlparse


def tokenise(sql):
    return sqlparse.parse(sql)[0].tokens


def get_tokens(sql):
    tokens = tokenise(sql)
    return [token for token in tokens if not token.is_whitespace]


def get_token_type(token):
    return token.ttype


def get_token_value(token):
    return token.value
