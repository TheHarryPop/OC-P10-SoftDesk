from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User as Auth_User
from django.http import HttpRequest
from django.contrib.auth.password_validation import validate_password

from .models import Users, Contributors, Projects, Issues, Comments


class RegisterSerializer(ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Auth_User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Auth_User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        auth_user = Auth_User.objects.create(username=validated_data['username'], email=validated_data['email'],
                                             first_name=validated_data['first_name'],
                                             last_name=validated_data['last_name'])
        auth_user.set_password(validated_data['password'])
        auth_user.save()
        user = Users.objects.create(email=auth_user.email, first_name=auth_user.first_name, user=auth_user,
                                    last_name=auth_user.last_name, password=auth_user.password)
        user.save()
        return auth_user


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title']


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user']


class ContributorSerializer(ModelSerializer):
    project = ProjectDetailSerializer

    class Meta:
        model = Contributors
        fields = ['user']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ['title', 'desc', 'tag', 'priority', 'status']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['description']
