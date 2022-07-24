from django.contrib.auth import authenticate
from rest_framework import serializers
from profile_api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    date_of_birth = serializers.DateField(input_formats=['%Y-%m-%d'], allow_null=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'password', 'password2', 'gender', 'date_of_birth']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        user_profile = UserProfile(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            gender=self.validated_data['gender'],
            date_of_birth=self.validated_data['date_of_birth']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password2 != password:
            raise serializers.ValidationError({'password': 'password does not match'})

        user_profile.set_password(password)
        user_profile.save()
        return user_profile


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        print('hey from validate')
        email = attrs.get('email')
        password = attrs.get('password')
        print(password)
        print(email)
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('wrong email or password')
        else:
            raise serializers.ValidationError('email and password is required')

        attrs['user'] = user
        return user
