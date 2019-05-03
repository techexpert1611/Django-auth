from users.models import User
from rest_framework import serializers


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'photo', 'password')

    def create(self, validated_data):
        user_data = validated_data
        user = User.objects.create_user(username=user_data['username'], first_name=user_data['first_name'],
                                        last_name=user_data['last_name'], email=user_data['email'],
                                        password=user_data['password'], is_active=True,phone=user_data['phone'],
                                        photo=user_data['photo'])
        user.save()
        return user

