from superlinked import framework as sl
from superlinked_app.config import settings
from datetime import timedelta


class FileDocument(sl.Schema):
    # Unique file identifier
    id: sl.IdField

    # Semantic content (left blank if no content)
    ContentType: sl.String           # Use ContentType as string
    Kind: sl.String                  # Use Kind as string

    # Filename and path
    Name: sl.String                  # Filename equivalent
    Path: sl.String

    # Size in bytes as float (converted from int)
    Size: sl.Float

    # Dates as datetime for recency (timestamps as Unix epoch int)
    CreationDate: sl.Timestamp
    ContentChangeDate: sl.Timestamp


file_schema = FileDocument()
import json
with open("./dataset/categories.json", "r", encoding="utf-8") as file:
    ALL_CATEGORIES = json.load(file)["Kind"]

print("Loaded categories:", ALL_CATEGORIES)
category_space = sl.CategoricalSimilaritySpace(
    category_input=file_schema.ContentType,
    categories=ALL_CATEGORIES,
    uncategorized_as_category=True,
    negative_filter=-1.0,
)
# Semantic spaces (can be adjusted as needed)
contenttype_space = sl.TextSimilaritySpace(
    text=file_schema.ContentType,
    model=settings.text_embedder_name,
)

kind_space = sl.TextSimilaritySpace(
    text=file_schema.Kind,
    model=settings.text_embedder_name,
)

name_space = sl.TextSimilaritySpace(
    text=file_schema.Name,
    model=settings.text_embedder_name,
)

# Numeric space for size in bytes, adjust max_value according to expected max size
size_space = sl.NumberSpace(
    file_schema.Size,
    min_value=0,
    max_value=1000000000,  # e.g. up to 1GB files
    mode=sl.Mode.MINIMUM,
)

creation_date_space = sl.RecencySpace(
    timestamp=file_schema.CreationDate,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), weight=1),
        sl.PeriodTime(timedelta(days=365), weight=2),
        sl.PeriodTime(timedelta(days=365 * 5), weight=3),
        sl.PeriodTime(timedelta(days=365 * 20), weight=4),
        sl.PeriodTime(timedelta(days=365 * 50), weight=5),
    ],
    negative_filter=0.0,
)

modified_date_space = sl.RecencySpace(
    timestamp=file_schema.ContentChangeDate,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), weight=1),
        sl.PeriodTime(timedelta(days=365), weight=2),
        sl.PeriodTime(timedelta(days=365 * 5), weight=3),
        sl.PeriodTime(timedelta(days=365 * 20), weight=4),
        sl.PeriodTime(timedelta(days=365 * 50), weight=5),
    ],
    negative_filter=0.0,
)

file_index = sl.Index(
    spaces=[
        contenttype_space,
        kind_space,
        category_space,
        name_space,
        size_space,
        creation_date_space,
        modified_date_space,
    ],
    fields=[
        file_schema.id,
        file_schema.ContentType,
        file_schema.Kind,
        file_schema.Name,                  # Filename equivalent
        file_schema.Path,
        file_schema.Size,
        file_schema.CreationDate,
        file_schema.ContentChangeDate,
    ],
)
