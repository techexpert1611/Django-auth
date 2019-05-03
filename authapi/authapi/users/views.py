from django.contrib import auth
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .constants import API_ERROR, REGISTER_SUCCESSFUL, PHOTO_EMPTY, PHONE_EXISTS, PHONE_EMPTY, PASSWORD_EMPTY, \
    INVALID_USERNAME_OR_PASSWORD,INVALID_CREDENTIALS, TOKEN_CREATED_SUCCESSFULLY, USERS_RETRIVED_SUCCESSFULLY, \
    NO_USERS, USERNAME_EXISTS, USERNAME_EMPTY, FIRST_NAME_EMPTY, LAST_NAME_EMPTY, EMAIL_EXISTS, EMAIL_EMPTY,\
    USERNAME_FEILD, FIRST_NAME_FEILD, LAST_NAME_FEILD, EMAIL_FEILD, PASSWORD_FEILD, PHONE_FEILD, PHOTO_FEILD
from .response_builder import create_response, error_response, invalid_server_response, successful_response,\
    unauthorized_response
from users.models import User
from .serializers import UserSerializer, UserSigninSerializer
from .authentication import token_expire_handler, expires_in


@api_view(["POST"])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def signin(request):
    response_data = {'data': {'expires_in': [], 'Token': [], 'username': []} }
    try:
        signin_serializer = UserSigninSerializer(data=request.data)
        if not signin_serializer.is_valid():
            return error_response(INVALID_USERNAME_OR_PASSWORD, response_data)
        user = auth.authenticate(username=signin_serializer.data['username'],
                                 password=signin_serializer.data['password'])
        if user is None:
            return unauthorized_response(INVALID_CREDENTIALS, response_data)
        else:
            # TOKEN STUFF
            token, _ = Token.objects.get_or_create(user=user)

            # token_expire_handler will check, if the token is expired it will generate new one
            is_expired, token = token_expire_handler(token)  # The implementation will be described further
            expire = expires_in(token)

            response_data['data']['expires_in'].append(expire)
            response_data['data']['Token'].append(token.key)
            response_data['data']['username'].append(request.data['username'])
            return successful_response(TOKEN_CREATED_SUCCESSFULLY, response_data)
    except:
        return invalid_server_response(API_ERROR, response_data)


@api_view(["GET"])
def user_info(request):
    response_data = {'data': []}
    try:
        users = User.objects.all()
        if users is not None:
            serializer = UserSerializer(users, many=True)
            response_data['data'].append(serializer.data)
            return create_response(USERS_RETRIVED_SUCCESSFULLY, response_data)
        else:
            return create_response(NO_USERS, response_data)
    except:
        return invalid_server_response(API_ERROR, response_data)


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_entry(request):
    response_data = {'data': []}
    try:
        if 'username' not in request.data:
            return error_response(USERNAME_FEILD, response_data)
        elif 'first_name' not in request.data:
            return error_response(FIRST_NAME_FEILD, response_data)
        elif 'last_name' not in request.data:
            return error_response(LAST_NAME_FEILD, response_data)
        elif 'email' not in request.data:
            return error_response(EMAIL_FEILD, response_data)
        elif 'password' not in request.data:
            return error_response(PASSWORD_FEILD, response_data)
        elif 'phone' not in request.data:
            return error_response(PHONE_FEILD, response_data)
        elif 'photo' not in request.data:
            return error_response(PHOTO_FEILD, response_data)
        elif request.data.get('username') is None:
            return error_response(USERNAME_EMPTY, response_data)
        elif request.data.get('first_name') is None:
            return error_response(FIRST_NAME_EMPTY, response_data)
        elif request.data.get('last_name') is None:
            return error_response(LAST_NAME_EMPTY, response_data)
        elif request.data.get('email') is None:
            return error_response(EMAIL_EMPTY, response_data)
        elif request.data.get('password') is None:
            return error_response(PASSWORD_EMPTY, response_data)
        elif request.data.get('phone') is None:
            return error_response(PHONE_EMPTY, response_data)
        elif request.data.get('photo') is None:
            return error_response(PHOTO_EMPTY, response_data)
        elif User.objects.filter(username=request.data['username']).exists():
            return error_response(USERNAME_EXISTS, response_data)
        elif User.objects.filter(email=request.data['email']).exists():
            return error_response(EMAIL_EXISTS, response_data)
        elif User.objects.filter(phone=request.data['phone']).exists():
            return error_response(PHONE_EXISTS, response_data)
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data['data'].append(serializer.data)
                return create_response(REGISTER_SUCCESSFUL, response_data)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    except:
        return invalid_server_response(API_ERROR, response_data)
