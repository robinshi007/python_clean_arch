from strawberry.fastapi import GraphQLRouter
from python_clean_arch.adapter.graphql.context import get_graphql_context

from python_clean_arch.adapter.graphql.schema import schema

router = GraphQLRouter(
    schema,
    graphiql=True,
    context_getter=get_graphql_context,
)
