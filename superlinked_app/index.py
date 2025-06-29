from superlinked import framework as sl
from superlinked_app.config import settings
from datetime import timedelta


@sl.schema
class FileDocument:
    # Unique file identifier
    id: sl.IdField

    # Semantic content
    Content: sl.String

    # Categorical filter fields
    File_Type: sl.StringList
    Tags: sl.StringList

    # Metadata fields
    Filename: sl.String
    Path: sl.String
    Size_kB: sl.Float

    # Dates as datetime for recency
    Creation_Date: sl.Timestamp
    Last_Modified_Date: sl.Timestamp


file_schema = FileDocument()

# Semantic space
content_space = sl.TextSimilaritySpace(
    text=file_schema.Content,
    model=settings.text_embedder_name,
)

filename_space = sl.TextSimilaritySpace(
    text=file_schema.Filename,
    model=settings.text_embedder_name,
)


# Numeric space for size
size_space = sl.NumberSpace(
    file_schema.Size_kB,
    min_value=0,
    max_value=20000,
    mode=sl.Mode.MINIMUM,
)



from datetime import timedelta

YEAR_IN_DAYS = 365

creation_date_space = sl.RecencySpace(
    timestamp=file_schema.Creation_Date,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), weight=1),            # last 1 month
        sl.PeriodTime(timedelta(days=365), weight=2),           # last year
        sl.PeriodTime(timedelta(days=365 * 5), weight=3),       # last 5 years
        sl.PeriodTime(timedelta(days=365 * 20), weight=4),      # last 20 years
        sl.PeriodTime(timedelta(days=365 * 50), weight=5),      # last 50 years
    ],
    negative_filter=0.0,
)

modified_date_space = sl.RecencySpace(
    timestamp=file_schema.Last_Modified_Date,
    period_time_list=[
        sl.PeriodTime(timedelta(days=30), weight=1),            # last 1 month
        sl.PeriodTime(timedelta(days=365), weight=2),           # last year
        sl.PeriodTime(timedelta(days=365 * 5), weight=3),       # last 5 years
        sl.PeriodTime(timedelta(days=365 * 20), weight=4),      # last 20 years
        sl.PeriodTime(timedelta(days=365 * 50), weight=5),      # last 50 years
    ],
    negative_filter=0.0,
)


# Compose index
index = sl.Index(
    spaces=[
        content_space,
        filename_space,
        size_space,
        creation_date_space,
        modified_date_space,
    ],
    fields=[
        file_schema.Filename,
        file_schema.Path,
        file_schema.Size_kB,
        file_schema.Creation_Date,
        file_schema.Last_Modified_Date,
        file_schema.File_Type,
        file_schema.Tags,
        file_schema.Content,
    ],
)
