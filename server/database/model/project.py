from mongoengine import StringField, DateTimeField, ListField

from database import Database, strict
from database.fields import OutputDestinationField, StrippedStringField
from database.model import AttributedDocument
from database.model.base import GetMixin


class Project(AttributedDocument):

    get_all_query_options = GetMixin.QueryParameterOptions(
        pattern_fields=("name", "description"), list_fields=("tags", "id")
    )

    meta = {
        "db_alias": Database.backend,
        "strict": strict,
        "indexes": [
            {
                "name": "%s.project.main_text_index" % Database.backend,
                "fields": ["$name", "$id", "$description"],
                "default_language": "english",
                "weights": {"name": 10, "id": 10, "description": 10},
            }
        ],
    }

    id = StringField(primary_key=True)
    name = StrippedStringField(
        required=True,
        unique_with=AttributedDocument.company.name,
        min_length=3,
        sparse=True,
    )
    description = StringField(required=True)
    created = DateTimeField(required=True)
    tags = ListField(StringField(required=True), default=list)
    default_output_destination = OutputDestinationField()
    last_update = DateTimeField()
