from superlinked import framework as sl

from superlinked_app.index import file_schema, index
from superlinked_app.query import query, query_debug
from superlinked_app.config import settings

rest_source_speech = sl.RestSource(file_schema)

vector_database = sl.QdrantVectorDatabase(
    url=settings.qdrant_url, api_key=settings.qdrant_api_key,timeout=settings.qdrant_timeout
)

config = sl.DataLoaderConfig(
    settings.path_dataset,
    sl.DataFormat.JSON,
    pandas_read_kwargs={"lines": True, "chunksize": settings.chunk_size},
)
loader_source_speech = sl.DataLoaderSource(file_schema, config)

executor = sl.RestExecutor(
    sources=[
        rest_source_speech,
        loader_source_speech,
    ],
    indices=[index],
    queries=[
        sl.RestQuery(sl.RestDescriptor("file-search"), query),
        sl.RestQuery(sl.RestDescriptor("file-search-debug"), query_debug),
    ],
    vector_database=vector_database,
)

sl.SuperlinkedRegistry.register(executor)