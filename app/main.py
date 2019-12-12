from ariadne import gql, QueryType, make_executable_schema
from ariadne.wsgi import GraphQL
from graphql import GraphQLResolveInfo
from typing import Union

query = QueryType()

type_defs = gql("""
    type Query {
        hello: String!
        goodbye: String!
        farewell: String!
    }
""")


class NotAString:
    text: str

    def __init__(self, text: str = '') -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text


# Correct type returned
@query.field("hello")
def resolve_hello(_: Union[object, None], info: GraphQLResolveInfo) -> str:
    user_agent = info.context["HTTP_USER_AGENT"]
    return f"heyo, {user_agent}!"


# Incorrect type returned. GraphQL returns error on method call
@query.field("goodbye")
def buhbye(*_: Union[object, None]) -> dict:
    return {"I": "am not a string"}


# Incorrect type returned. mypy sees no errors. GraphQL returns error on method call
@query.field("farewell")
def solong(*_: Union[object, None]) -> NotAString:
    return NotAString(text='Not a string tho')


schema = make_executable_schema(type_defs, query)

app = GraphQL(schema, debug=True)
