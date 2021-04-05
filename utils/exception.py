from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class PageNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found.'
    default_code = 'not_found'


class RequireValue(APIException):
    status_code = 400
    default_detail = 'Required value'
    default_code = 'required_value'


class ExistedValue(APIException):
    status_code = 400
    default_detail = 'Existed value'
    default_code = 'existed_value'


class FormatErrorValue(APIException):
    status_code = 400
    default_detail = 'Format error value'
    default_code = 'format_error_value'


class UserTypeError(APIException):
    status_code = 400
    default_detail = 'user type error'
    default_code = 'user_type'


class DoesNotExist(APIException):
    status_code = 400
    default_detail = 'Does not exist'
    default_code = 'does_not_exist'


class MaxNumberOfItem(APIException):
    status_code = 400
    default_detail = 'max number of item'
    default_code = 'max_number_of_item'


class ParticipantUserError(APIException):
    status_code = 400
    default_detail = 'Participant user error'
    default_code = 'participant_user_error'


class PasswordIncorrect(APIException):
    status_code = 400
    default_detail = 'Password incorrect'
    default_code = 'password_incorrect'


class UseNotActive(APIException):
    status_code = 400
    default_detail = 'User not active'
    default_code = 'user_not_active'


class EventTimeSelected(APIException):
    status_code = 400
    default_detail = 'event time have already selected'
    default_code = 'event_time_selected'


class PermissionDenied(APIException):
    status_code = 400
    default_detail = 'You do not have permission to perform this action'
    default_code = 'permission_denied'
