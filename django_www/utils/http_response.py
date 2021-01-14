from django.http import JsonResponse

from . import messages

RESP_STATUS_SUCCESS_CODE = '0000'
RESP_STATUS_FAILURE_CODE = '9999'

BASIC__RESPONSE = {'result': '', 'status_code': '', 'content': '', 'msg': ''}


def json_response_bad_request(request):
    return json_response_error_code(request, RESP_STATUS_FAILURE_CODE, messages.ERROR__BAD_REQUEST)


def json_response_server_error(request):
    return json_response_error_code(request, RESP_STATUS_FAILURE_CODE, messages.ERROR__SERVER_ERROR)


def json_response_forbidden(request):
    return json_response_error_code(request, RESP_STATUS_FAILURE_CODE, messages.ERROR__FORBIDDEN)


def json_response_error_code(_, code=RESP_STATUS_FAILURE_CODE, msg=messages.ERROR__SERVER_ERROR):
    result = {'result': 'failed', 'status_code': code, 'content': [], 'msg': msg}
    return JsonResponse(result)


def json_response_success(content, code=RESP_STATUS_SUCCESS_CODE, msg=''):
    result = {'result': 'success', 'status_code': code, 'content': content, 'msg': msg}
    return JsonResponse(result)


def json_response(_, data=None):
    if not data:
        data = {}
    return JsonResponse(data)
