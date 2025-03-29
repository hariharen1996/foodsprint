from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','username','email','password','phone','address']
        extra_kwargs = { 'password': {'write_only': True} }

    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone',''),
            address=validated_data.get('address',''),
        )

        Token.objects.create(user=user)

        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()

            if user:
                if not user.check_password(password):
                    msg = 'Unable to login with provided credentials'
                    raise serializers.ValidationError(msg,code='authorization')
            else:
                msg = 'user with this email does not exist'
                raise serializers.ValidationError(msg,code='authorization')
            
            attrs['user'] = user 
            return attrs

        else:
            msg = 'email amd password is mandetory'
            raise serializers.ValidationError(msg,code='authorization')
        