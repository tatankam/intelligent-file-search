import json
from superlinked import framework as sl
from superlinked_app.config import settings

openai_config = sl.OpenAIClientConfig(
    api_key=settings.openai_api_key.get_secret_value(),
    model=settings.openai_model,
    base_url=settings.open_ai_base_url,
)

def get_cat_options() -> dict[str, list[str]]:
    """
    Loads categorical options for filters such as file type and tags from a local JSON file.
    The JSON should map category names to lists of valid options.
    Example structure:
    {
        "FileType": ["pdf", "docx", "md"],
        "Tags": ["sport", "fashion", "cinema"]
    }
    """
    with open(settings.path_categories, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------------------
# Parameter descriptions for NLQ
# ------------------------------

content_description = (
    "'Content' refers to the actual text content of the file. "
    "It can include subject matter, topics, or keywords such as 'tennis', 'fashion', 'award', etc. "
    "Used to match documents with semantically similar content."
)

filename_description = (
    "'Filename' refers to the name of the file. "
    "You may refer to keywords or file names like 'tennis.pdf', 'report.docx', or 'runway'."
)

filetype_description = (
    "'File Type' refers to the format of the file, such as PDF, DOCX, TXT, etc. "
    "Examples: 'show me only PDF files', 'I want Word documents'."
)

tags_description = (
    "'Tags' refer to thematic labels applied to the file, like 'sport', 'fashion', 'cinema', 'cars'. "
    "You can use them to filter for specific types of content."
)

size_description = (
    "'Size' refers to the file size in kilobytes. "
    "You can express preferences such as 'small files', 'under 10MB', or 'very large files'."
)

creation_date_description = (
    "'Creation Date' is when the file was originally created. "
    "You can use it to prioritize older or newer files, e.g., 'recent files only', 'files from 2015'."
)

modified_date_description = (
    "'Last Modified Date' refers to the most recent date the file was edited. "
    "Used to find files that were recently updated or edited a long time ago."
)

system_prompt = (
    "Extract search parameters from the user's natural language query about files.\n"
    "Guidelines:\n"
    "- Identify semantic queries about content or file name.\n"
    "- Use file type and tags as categorical filters.\n"
    "- Size in kilobytes may be specified as small/large or by value.\n"
    "- Creation and modification dates may indicate recency.\n"
    "- If no preference is mentioned for a field, use None.\n"
    "- Examples:\n"
    "  1. User query: 'Recent PDF files about fashion or sport' -> file_type: 'pdf', tags: ['fashion', 'sport'], prioritize modified_date.\n"
    "  2. User query: 'Large Word documents about tennis' -> file_type: 'docx', content: 'tennis', size: high.\n"
    "  3. User query: 'Old reports about cinema and cars' -> tags: ['cinema', 'cars'], prioritize old creation_date.\n"
    "  4. User query: 'Documents mentioning basketball' -> content: 'basketball'\n"
)
