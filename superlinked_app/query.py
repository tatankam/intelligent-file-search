from superlinked import framework as sl
from superlinked_app.index import (
    file_index,
    file_schema,
    contenttype_space,
    kind_space,
    category_space,
    name_space,
    size_space,
    creation_date_space,
    modified_date_space,
)

query_debug = (
    sl.Query(file_index)
    .find(file_schema)
    .limit(3)
    .select_all()
    .include_metadata()
    )




# Main semantic search query
query = (
    sl.Query(
        file_index,
        weights={
            contenttype_space: sl.Param("contenttype_weight", default=1.0),
            kind_space: sl.Param("kind_weight", default=1.0),
            category_space: sl.Param("category_weight", default=1.0),
            name_space: sl.Param("name_weight", default=1.0),
            size_space: sl.Param("size_weight", default=1.0),
            creation_date_space: sl.Param("creation_date_weight", default=1.0),
            modified_date_space: sl.Param("modified_date_weight", default=1.0),
        },
    )
    .find(file_schema)
    .similar(contenttype_space, sl.Param("contenttype_query"))
    .similar(kind_space, sl.Param("kind_query"))
    .similar(category_space, sl.Param("category_query"))
    .similar(name_space, sl.Param("name_query"))
    # REMOVE .similar() for size_space, creation_date_space, modified_date_space
    # Instead, use filters for those fields if needed:
    .filter(file_schema.Size > 0)  # Exclude zero-size files
    .filter(file_schema.Size >= sl.Param("min_size_kb", default=0))
    .filter(file_schema.Size <= sl.Param("max_size_kb", default=1_000_000_000))
    .filter(file_schema.CreationDate >= sl.Param("min_creation_date", default=0))
    .filter(file_schema.CreationDate <= sl.Param("max_creation_date", default=4102444800))  # e.g. year 2100
    .filter(file_schema.ContentChangeDate >= sl.Param("min_modified_date", default=0))
    .filter(file_schema.ContentChangeDate <= sl.Param("max_modified_date", default=4102444800))
    .limit(sl.Param("limit", default=5))
    .select_all()
    .include_metadata()
)

# Limit and return all fields and metadata
# query = query.limit(sl.Param("limit", default=5))
# query = query.select_all()
# query = query.include_metadata()


# # Numerical filter: file size
# query = query.filter(file_schema.Size >= sl.Param("min_size_kb"))
# query = query.filter(file_schema.Size <= sl.Param("max_size_kb"))


# # Temporal filters: creation & modification using declared params
# query = query.filter(file_schema.CreationDate >= sl.Param("min_creation_date"))
# query = query.filter(file_schema.CreationDate <= sl.Param("max_creation_date"))
# query = query.filter(file_schema.ContentChangeDate >= sl.Param("min_modified_date"))
# query = query.filter(file_schema.ContentChangeDate <= sl.Param("max_modified_date"))


# Categorical filters for File Type and Tags
# CategoryFilter = namedtuple(
#     "CategoryFilter", ["operator", "param_name", "category_name", "description"]
# )

# filters = [
#     CategoryFilter(
#         operator=file_schema.Kind.contains_all,
#         param_name="filetype_include_all",
#         category_name="FileType",
#         description="File must match all of these file types",
#     ),
#     CategoryFilter(
#         operator=file_schema.Kind.contains,
#         param_name="filetype_include_any",
#         category_name="FileType",
#         description="File can match any of these file types",
#     ),
#     CategoryFilter(
#         operator=file_schema.Kind.not_contains,
#         param_name="filetype_exclude",
#         category_name="FileType",
#         description="File must not match any of these file types",
#     ),
# ]

# for filter_item in filters:
#     param = sl.Param(
#         filter_item.param_name,
#         description=filter_item.description,
#         options=cat_options.get(filter_item.category_name, []),
#     )
#     query = query.filter(filter_item.operator(param))


# Declare simple_query param explicitly (optional)
# simple_query_param = sl.Param(
#     "simple_query",
#     description="Simple natural language query to parse into structured filters",
# )

# # Natural language interface
# query = query.with_natural_query(
#     natural_query=sl.Param("natural_query"),
#     client_config=openai_config,
#     system_prompt=system_prompt,
# )
