from ariadne import gql, QueryType, make_executable_schema, MutationType
from ariadne.asgi import GraphQL

from app.status import get_current_status as get_current_status_from_mongo
from app.status import set_current_status as set_current_status_in_mongo
from app.user.index import get_user_first_name

query = QueryType()
mutation = MutationType()

type_defs = gql('''
type Query {
    """
    Use strings like this to document your methods.
    This description will automatically be reflected into the introspection schema for tooling.
    This method will greet you by name if you're logged in, otherwise greet you as anonymous.
    
    If the user service is not available, this method will fail.
    """
    hello: String

    echo(s: String): String

    fail: String

    """
    Add two integers together.
    """
    add(a: Int!, b: Int!): Int!

    """
    The current world status, as determined by users. This may be null in normal operation.
    """
    currentStatus: String
  }

  input SetStatusInput {
    status: String
  }

  type SetStatusPayload {
    status: String
  }

  type Mutation {
    """
    Set the current world status. This method is only available to logged-in users.
    """
    setStatus(input: SetStatusInput!): SetStatusPayload
  }
''')


def addInts(a, b):
    return a + b


# Correct type returned
@query.field("hello")
def resolve_hello(parent, info):
    name = get_user_first_name()
    name = name if name is not None else "anonymous person"
    return f"Hello, {name}, welcome to GraphQL!"


@query.field("echo")
def echo(*_, s=None):
    if s is None or s == "":
        # Note that, as implemented, this is an anti-pattern. This will populate "errors" property, which should
        # be reserved for developer debugging information
        raise ValueError("Cannot echo an empty/missing string")
    return s


@query.field("fail")
def fail(*_):
    raise ValueError("This API was destined for failure")


@query.field("add")
def add(*_, a, b):
    return addInts(a, b)


@query.field("currentStatus")
def current_status(*_):
    # TODO: check info for a userId and raise an Exception if not
    return get_current_status_from_mongo()


@mutation.field("setStatus")
def set_current_status(*_, input):
    # TODO: check info for a userId and raise an Exception if not
    set_current_status_in_mongo(input["status"])
    return {"status": input["status"]}


schema = make_executable_schema(type_defs, query, mutation)

app = GraphQL(schema, debug=True)
