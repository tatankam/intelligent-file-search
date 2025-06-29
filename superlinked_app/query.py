from collections import namedtuple
from superlinked import framework as sl
from superlinked_app.index import (
    index,
    file_schema,
    content_space,
    filename_space,
    size_space,
    creation_date_space,
    modified_date_space,
)
from superlinked_app.nlq import (
    content_description,
    filename_description,
    filetype_description,
    tags_description,
    size_description,
    creation_date_description,
    modified_date_description,
    system_prompt,
    openai_config,
    get_cat_options,
)

# Get categorical options
cat_options = get_cat_options()

# Debug query (optional)
query_debug = sl.Query(index).find(file_schema).limit(3).select_all()

# Main semantic search query
query = (
    sl.Query(
        index,
        weights={
            content_space: sl.Param("content_weight", description=content_description),
            filename_space: sl.Param("filename_weight", description=filename_description),
            size_space: sl.Param("size_weight", description=size_description),
            creation_date_space: sl.Param("creation_date_weight", description=creation_date_description),
            modified_date_space: sl.Param("modified_date_weight", description=modified_date_description),
        },
    )
    .find(file_schema)
    .similar(
        content_space.text,
        sl.Param("content_query", description=content_description),
        weight=sl.Param("similar_content_weight", default=1.0),
    )
    .similar(
        filename_space.text,
        sl.Param("filename_query", description=filename_description),
        weight=sl.Param("similar_filename_weight", default=1.0),
    )
)

# Limit and return all fields and metadata
query = query.limit(sl.Param("limit", default=5))
query = query.select_all()
query = query.include_metadata()

# Numerical filter: file size
query = query.filter(file_schema.Size_kB >= sl.Param("min_size_kb"))
query = query.filter(file_schema.Size_kB <= sl.Param("max_size_kb"))

# Temporal filters: creation & modification
query = query.filter(file_schema.Creation_Date >= sl.Param("min_creation_date"))
query = query.filter(file_schema.Creation_Date <= sl.Param("max_creation_date"))
query = query.filter(file_schema.Last_Modified_Date >= sl.Param("min_modified_date"))
query = query.filter(file_schema.Last_Modified_Date <= sl.Param("max_modified_date"))

# Categorical filters for File Type and Tags
CategoryFilter = namedtuple(
    "CategoryFilter", ["operator", "param_name", "category_name", "description"]
)

filters = [
    CategoryFilter(
        operator=file_schema.File_Type.contains_all,
        param_name="filetype_include_all",
        category_name="FileType",
        description="File must match all of these file types",
    ),
    CategoryFilter(
        operator=file_schema.File_Type.contains,
        param_name="filetype_include_any",
        category_name="FileType",
        description="File can match any of these file types",
    ),
    CategoryFilter(
        operator=file_schema.File_Type.not_contains,
        param_name="filetype_exclude",
        category_name="FileType",
        description="File must not match any of these file types",
    ),
    CategoryFilter(
        operator=file_schema.Tags.contains_all,
        param_name="tags_include_all",
        category_name="Tags",
        description="Files must contain all of these tags",
    ),
    CategoryFilter(
        operator=file_schema.Tags.contains,
        param_name="tags_include_any",
        category_name="Tags",
        description="Files must contain at least one of these tags",
    ),
    CategoryFilter(
        operator=file_schema.Tags.not_contains,
        param_name="tags_exclude",
        category_name="Tags",
        description="Files must not contain any of these tags",
    ),
]

for filter_item in filters:
    param = sl.Param(
        filter_item.param_name,
        description=filter_item.description,
        options=cat_options.get(filter_item.category_name, []),
    )
    query = query.filter(filter_item.operator(param))

# Natural language interface
query = query.with_natural_query(
    natural_query=sl.Param("natural_query"),
    client_config=openai_config,
    system_prompt=system_prompt,
)
