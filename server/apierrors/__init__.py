import pathlib
from . import autogen

from .apierror import APIError


""" Error codes """
_error_codes = {
    (400, 'bad_request'): {
        1: ('not_supported', 'endpoint is not supported'),
        2: ('request_path_has_invalid_version', 'request path has invalid version'),
        5: ('invalid_headers', 'invalid headers'),
        6: ('impersonation_error', 'impersonation error'),

        10: ('invalid_id', 'invalid object id'),
        11: ('missing_required_fields', 'missing required fields'),
        12: ('validation_error', 'validation error'),
        13: ('fields_not_allowed_for_role', 'fields not allowed for role'),
        14: ('invalid fields', 'fields not defined for object'),
        15: ('fields_conflict', 'conflicting fields'),
        16: ('fields_value_error', 'invalid value for fields'),
        17: ('batch_contains_no_items', 'batch request contains no items'),
        18: ('batch_validation_error', 'batch request validation error'),
        19: ('invalid_lucene_syntax', 'malformed lucene query'),
        20: ('fields_type_error', 'invalid type for fields'),
        21: ('invalid_regex_error', 'malformed regular expression'),
        22: ('invalid_email_address', 'malformed email address'),
        23: ('invalid_domain_name', 'malformed domain name'),
        24: ('not_public_object', 'object is not public'),

        # Tasks
        100: ('task_error', 'general task error'),
        101: ('invalid_task_id', 'invalid task id'),
        102: ('task_validation_error', 'task validation error'),
        110: ('invalid_task_status', 'invalid task status'),
        111: ('task_not_started', 'task not started (invalid task status)'),
        112: ('task_in_progress', 'task in progress (invalid task status)'),
        113: ('task_published', 'task published (invalid task status)'),
        114: ('task_status_unknown', 'task unknown (invalid task status)'),
        120: ('invalid_task_execution_progress', 'invalid task execution progress'),
        121: ('failed_changing_task_status', 'failed changing task status. probably someone changed it before you'),
        122: ('missing_task_fields', 'task is missing expected fields'),
        123: ('task_cannot_be_deleted', 'task cannot be deleted'),
        125: ('task_has_jobs_running', "task has jobs that haven't completed yet"),
        126: ('invalid_task_type', "invalid task type for this operations"),
        127: ('invalid_task_input', 'invalid task output'),
        128: ('invalid_task_output', 'invalid task output'),
        129: ('task_publish_in_progress', 'Task publish in progress'),
        130: ('task_not_found', 'task not found'),


        # Models
        200: ('model_error', 'general task error'),
        201: ('invalid_model_id', 'invalid model id'),
        202: ('model_not_ready', 'model is not ready'),
        203: ('model_is_ready', 'model is ready'),
        204: ('invalid_model_uri', 'invalid model URI'),
        205: ('model_in_use', 'model is used by tasks'),
        206: ('model_creating_task_exists', 'task that created this model exists'),

        # Users
        300: ('invalid_user', 'invalid user'),
        301: ('invalid_user_id', 'invalid user id'),
        302: ('user_id_exists', 'user id already exists'),
        305: ('invalid_preferences_update', 'Malformed key and/or value'),

        # Projects
        401: ('invalid_project_id', 'invalid project id'),
        402: ('project_has_tasks', 'project has associated tasks'),
        403: ('project_not_found', 'project not found'),
        405: ('project_has_models', 'project has associated models'),

        # Database
        800: ('data_validation_error', 'data validation error'),
        801: ('expected_unique_data', 'value combination already exists'),
    },

    (401, 'unauthorized'): {
        1:  ('not_authorized', 'unauthorized (not authorized for endpoint)'),
        2:  ('entity_not_allowed', 'unauthorized (entity not allowed)'),
        10: ('bad_auth_type', 'unauthorized (bad authentication header type)'),
        20: ('no_credentials', 'unauthorized (missing credentials)'),
        21: ('bad_credentials', 'unauthorized (malformed credentials)'),
        22: ('invalid_credentials', 'unauthorized (invalid credentials)'),
        30: ('invalid_token', 'invalid token'),
        31: ('blocked_token', 'token is blocked')
    },

    (403, 'forbidden'): {
        10: ('routing_error', 'forbidden (routing error)'),
        11: ('missing_routing_header', 'forbidden (missing routing header)'),
        12: ('blocked_internal_endpoint', 'forbidden (blocked internal endpoint)'),
        20: ('role_not_allowed', 'forbidden (not allowed for role)'),
        21: ('no_write_permission', 'forbidden (modification not allowed)'),
    },

    (500, 'server_error'): {
        0:   ('general_error', 'general server error'),
        1:   ('internal_error', 'internal server error'),
        2:   ('config_error', 'configuration error'),
        3:   ('build_info_error', 'build info unavailable or corrupted'),
        10:  ('transaction_error', 'a transaction call has returned with an error'),
        # Database-related issues
        100: ('data_error', 'general data error'),
        101: ('inconsistent_data', 'inconsistent data encountered in document'),
        102: ('database_unavailable', 'database is temporarily unavailable'),

        # Index-related issues
        201: ('missing_index', 'missing internal index'),

        9999: ('not_implemented', 'action is not yet implemented'),
    }
}


autogen.generate(pathlib.Path(__file__).parent, _error_codes)
