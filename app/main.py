from ariadne import gql, QueryType, make_executable_schema
from ariadne.wsgi import GraphQL

query = QueryType()

type_defs = gql("""
    type Query {
        hello: String!
        goodbye: String!
        farewell: String!
    }
""")


# Correct type returned
@query.field("hello")
def resolve_hello(*_):
    return "heyo"


# Incorrect type returned. GraphQL returns error on method call
@query.field("goodbye")
def buhbye(*_):
    return {"I": "am not a string"}


# Incorrect type returned. mypy sees no errors. GraphQL returns error on method call
@query.field("farewell")
def solong(*_) -> object:
    result: object = {"I": "am an object"}
    return result


schema = make_executable_schema(type_defs, query)

app = GraphQL(schema, debug=True)
