from strawberry.schema import Schema
from python_clean_arch.adapter.graphql.schema.mutation import Mutation

from python_clean_arch.adapter.graphql.schema.query import Query


schema = Schema(query=Query, mutation=Mutation)
