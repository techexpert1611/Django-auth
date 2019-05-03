from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, \
    HTTP_401_UNAUTHORIZED, HTTP_201_CREATED

from .constants import SUCCESS, ERROR


def create_response(message, data):
    data['result'] = SUCCESS
    data['message'] = message
    return Response(data, status=HTTP_201_CREATED)


def error_response(message, data):
    data['result'] = ERROR
    data['message'] = message
    return Response(data, status=HTTP_400_BAD_REQUEST)


def unauthorized_response(message, data):
    data['result'] = ERROR
    data['message'] = message
    return Response(data, status=HTTP_401_UNAUTHORIZED)


def successful_response(message,data):
    data['result'] = SUCCESS
    data['message'] = message
    return Response(data, status=HTTP_200_OK)


def invalid_server_response(message,data):
    data['result'] = ERROR
    data['message'] = message
    return Response(data, status=HTTP_500_INTERNAL_SERVER_ERROR)
