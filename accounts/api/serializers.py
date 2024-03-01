from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from accounts.models import User,Student


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_student',
                  'is_lecturer', 'gender', 'phone', 'address', 'picture')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user







class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'student', 'level', 'program')
