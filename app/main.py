from os.path import dirname, join

from ariadne import QueryType, MutationType
from ariadne.asgi import GraphQL
from ariadne_extensions import federation

from app.status import get_current_status as get_current_status_from_mongo
from app.status import set_current_status as set_current_status_in_mongo
from app.user.index import get_user_first_name

from graphql import GraphQLResolveInfo

from typing import Optional, Dict

query = QueryType()
mutation = MutationType()

# type_defs = load_schema_from_path(join(dirname(__file__), 'schema.graphql'))


def addInts(a: int, b: int) -> int:
    return a + b


# Correct type returned
@query.field("hello")
def resolve_hello(parent: Optional[object], info: GraphQLResolveInfo) -> str:
    name = get_user_first_name()
    name = name if name is not None else "anonymous person"
    return f"Hello, {name}, welcome to GraphQL!"


@query.field("echo")
def echo(*_: Optional[object], s: str = None) -> str:
    if s is None or s == "":
        # Note that, as implemented, this is an anti-pattern. This will populate "errors" property, which should
        # be reserved for developer debugging information
        raise ValueError("Cannot echo an empty/missing string")
    return s


@query.field("fail")
def fail(*_: Optional[object]) -> None:
    raise ValueError("This API was destined for failure")


@query.field("add")
def add(*_: Optional[object], a: int, b: int) -> int:
    return addInts(a, b)


@query.field("currentStatus")
def current_status(*_: Optional[object]) -> str:
    # TODO: check info for a userId and raise an Exception if not
    return get_current_status_from_mongo()


@mutation.field("setStatus")
def set_current_status(*_: Optional[object], input: Dict[str, str]) -> Dict[str, str]:
    # TODO: check info for a userId and raise an Exception if not
    set_current_status_in_mongo(input["status"])
    return {"status": input["status"]}


manager = federation.FederatedManager(
    schema_sdl_file=join(dirname(__file__), 'schema.graphql'),
    query=query
)

schema = manager.get_schema()

# schema = make_executable_schema(type_defs, query, mutation)

app = GraphQL(schema, debug=True)
