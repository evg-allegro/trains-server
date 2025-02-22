from enum import Enum

from mongoengine import (
    StringField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    DateTimeField,
    IntField,
    ListField,
)

from database import Database, strict
from database.fields import StrippedStringField, SafeMapField, SafeDictField
from database.model import AttributedDocument
from database.model.model_labels import ModelLabels
from database.model.project import Project
from database.utils import get_options
from .metrics import MetricEvent
from .output import Output

DEFAULT_LAST_ITERATION = 0


class TaskStatus(object):
    created = 'created'
    in_progress = 'in_progress'
    stopped = 'stopped'
    publishing = 'publishing'
    published = 'published'
    closed = 'closed'
    failed = 'failed'
    unknown = 'unknown'


class TaskStatusMessage(object):
    stopping = 'stopping'


class TaskTags(object):
    development = 'development'


class Script(EmbeddedDocument):
    binary = StringField(default='python')
    repository = StringField(required=True)
    tag = StringField()
    branch = StringField()
    version_num = StringField()
    entry_point = StringField(required=True)
    working_dir = StringField()
    requirements = SafeDictField()


class Execution(EmbeddedDocument):
    test_split = IntField(default=0)
    parameters = SafeDictField(default=dict)
    model = StringField(reference_field='Model')
    model_desc = SafeMapField(StringField(default=''))
    model_labels = ModelLabels()
    framework = StringField()

    queue = StringField()
    ''' Queue ID where task was queued '''


class TaskType(object):
    training = 'training'
    testing = 'testing'


class Task(AttributedDocument):
    meta = {
        'db_alias': Database.backend,
        'strict': strict,
        'indexes': [
            'created',
            'started',
            'completed',
            {
                'name': '%s.task.main_text_index' % Database.backend,
                'fields': [
                    '$name',
                    '$id',
                    '$comment',
                    '$execution.model',
                    '$output.model',
                    '$script.repository',
                    '$script.entry_point',
                ],
                'default_language': 'english',
                'weights': {
                    'name': 10,
                    'id': 10,
                    'comment': 10,
                    'execution.model': 2,
                    'output.model': 2,
                    'script.repository': 1,
                    'script.entry_point': 1,
                },
            },
        ],
    }

    id = StringField(primary_key=True)
    name = StrippedStringField(
        required=True, user_set_allowed=True, sparse=False, min_length=3
    )

    type = StringField(required=True, choices=get_options(TaskType))
    status = StringField(default=TaskStatus.created, choices=get_options(TaskStatus))
    status_reason = StringField()
    status_message = StringField()
    status_changed = DateTimeField()
    comment = StringField(user_set_allowed=True)
    created = DateTimeField(required=True, user_set_allowed=True)
    started = DateTimeField()
    completed = DateTimeField()
    published = DateTimeField()
    parent = StringField()
    project = StringField(reference_field=Project, user_set_allowed=True)
    output = EmbeddedDocumentField(Output, default=Output)
    execution: Execution = EmbeddedDocumentField(Execution, default=Execution)
    tags = ListField(StringField(required=True), user_set_allowed=True)
    script = EmbeddedDocumentField(Script)
    last_update = DateTimeField()
    last_iteration = IntField(default=DEFAULT_LAST_ITERATION)
    last_metrics = SafeMapField(field=SafeMapField(EmbeddedDocumentField(MetricEvent)))


class TaskVisibility(Enum):
    active = 'active'
    archived = 'archived'
