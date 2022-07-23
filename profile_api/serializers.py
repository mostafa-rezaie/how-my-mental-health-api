from rest_framework import serializers
from profile_api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    date_of_birth = serializers.DateField(input_formats=['%Y-%m-%d'],allow_null=True)

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

