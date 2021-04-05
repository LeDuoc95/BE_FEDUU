from abc import ABC

from rest_framework import serializers
from django.db import transaction
from utils import exception
from .models import User as UserModel
from .models import PhotoModel
from django.contrib.auth.hashers import make_password, identify_hasher, check_password
from django.contrib.auth.models import User as User_auth


def validate_password(value: str) -> str:
    """
    Hash value passed by user.

    :param value: password of a user
    :return: a hashed version of the password
    """
    return make_password(value, 'salt')


class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            'email',
            'name',
            'username',
            'position',
            'phone',
            'account_type',
            'photo'
        ]

    def validate(self, attrs):
        return self.initial_data

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            'email',
            'name',
            'username',
            'position',
            'phone',
            'account_type'
        ]

    def validate(self, attrs):
        required_fields = ['email', 'username']
        for field in required_fields:
            if self.initial_data.get(field, None) is None:
                raise exception.RequireValue(detail=f"{field} is require!")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            password = self.initial_data.get('password', None)
            if password is None:
                password = 'Test@123'
            validated_data['password'] = validate_password(password)
            user = UserModel.objects.create(**validated_data)
            user.save()
            return user


class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model = UserModel
        fields = []
    """
    Serializer for password change endpoint.
    """

    def validate(self, attrs):
        if self.initial_data.get('old_password', None) is None:
            raise exception.RequireValue(detail=f"old_password is require!!!")
        is_correct_password = self.instance.check_password(
            self.initial_data.get('old_password'))
        if is_correct_password is False:
            raise exception.APIException(detail="password is wrong!!!")
        if self.initial_data.get('old_password', None) is not None:
            attrs['new_password'] = self.initial_data.get('new_password')
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            if validated_data.get('new_password', None) is not None:
                instance.password = validate_password(
                    validated_data.get('new_password'))
            else:
                instance.password = validate_password('Fedu@12345')
            instance.save()
            return {}


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'phone', 'name', 'email', 'photo']

    def validate(self, attrs):
        required_fields = ['username', 'phone', 'name', 'email', 'photo']
        for field in required_fields:
            if self.initial_data.get(field, None) is None:
                raise exception.RequireValue(detail=f"{field} is require")
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr_user in validated_data:
                setattr(instance, attr_user, validated_data.get(attr_user, None))
            instance.save()
            return instance

    def to_representation(self, instance):
        data = super(UpdateUserSerializer, self).to_representation(instance)
        if hasattr(instance.photo, 'id') is not False:
            photo_user = PhotoModel.objects.filter(id=instance.photo.id).first()
            data['photo'] = {
                'id': photo_user.id,
                'name': "image.png",
                'status': "done",
                'path': photo_user.photo.name,
            }
        return data


class UploadPhotoSerializer(serializers.Serializer):
    class Meta:
        model = PhotoModel
        fields = '__all__'

    def validate(self, attrs):
        images_user = self.initial_data.get('imagesUser', None)
        if images_user is None:
            raise exception.RequireValue(detail="imagesUser is require!")
        attrs['photo'] = images_user
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            file_image = PhotoModel.objects.create(**validated_data)
            file_image.save()
            return file_image

    def to_representation(self, instance):
        return {'id': instance.id, 'photo': instance.photo.name}
