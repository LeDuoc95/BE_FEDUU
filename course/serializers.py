from abc import ABC

from rest_framework import serializers
from .models import CourseModel, FeelingStudentModel, VideosModel
from django.db import transaction
from utils import exception
from users import models as model_user
from users.serializers import GetAllPhotoSerializer, GetAllUserSerializer, UpdateUserSerializer

class GetAllCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = [
            'id',
            'deleted',
            'title',
            'new_price',
            'old_price',
            'type',
            'description',
            'photo',
            'status',
            'reason',
            'list_video',
        ]

    def to_representation(self, instance):
        data = super(GetAllCourseSerializer, self).to_representation(instance)
        user = model_user.User.objects.filter(id=instance.user.id).first()
        data['user'] = user.username
        return data

class GetDetailCourseSerializer(serializers.ModelSerializer):
    photo = GetAllPhotoSerializer()
    class Meta:
        model = CourseModel
        fields = [
            'id',
            'deleted',
            'title',
            'new_price',
            'old_price',
            'type',
            'description',
            'photo',
            'user',
            'status',
            'reason',
            'list_video',
        ]

    def to_representation(self, instance):
        data = super(GetDetailCourseSerializer, self).to_representation(instance)
        user = model_user.User.objects.filter(id=instance.user.id).first()
        data['user'] = user.username
        return data

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ['id', 'photo', 'old_price', 'title', 'type', 'description', 'list_video']

    def validate(self, attrs):
        user_id = self.context.get('request').user.id
        print(user_id,'user_id')
        user = model_user.User.objects.filter(id=user_id).first()
        print(user,'user')
        required_fields = ['photo', 'old_price', 'title', 'type', 'description']
        for field in required_fields:
            if self.initial_data.get(field, None) is None:
                raise exception.RequireValue(detail=f"{field} is require!")

        check_math = CourseModel.objects.filter(
            title=self.initial_data['title'].strip())
        if check_math.count() > 0:
            raise exception.ExistedValue
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            print(validated_data,'validated_data')
            instance = CourseModel.objects.create(**validated_data)
            instance.save()
            return instance


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = "__all__"

    def validate(self, attrs):
        check_math = CourseModel.objects.filter(
            title=self.initial_data['title'].strip())
        if check_math.count() > 0:
            raise exception.ExistedValue
        return self.initial_data

    def update(self, instance, validated_data):
        with transaction.atomic():
            # validated_data['id'] = instance.id
            # instance.title = validated_data['title']
            # instance.price = validated_data['price']
            # instance.des = validated_data['des']
            # instance.is_basic = validated_data['is_basic']
            # instance.limited_study = validated_data['limited_study']
            # instance.registration_number = validated_data['registration_number']
            # instance.save()
            return instance


class DeleteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = [
            'id',
        ]

    def validate(self, attrs):
        return self.initial_data

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.delete()
            instance.save()
            return instance


class CreateFeelingStudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeelingStudentModel
        fields = "__all__"

    def validate(self, attrs):
        return self.initial_data

    def create(self, validated_data):
        with transaction.atomic():
            # instance = FeelingStudentModel.objects.create(**validated_data)
            return validated_data


class UploadVideosSerializer(serializers.Serializer):
    class Meta:
        model = VideosModel
        fields = '__all__'

    def validate(self, attrs):
        file = self.initial_data.get('file', None)
        if file is None:
            raise exception.RequireValue(detail="videoCourse is require!")
        attrs['video'] = file
        attrs['title'] = file.name
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            file_video = VideosModel.objects.create(**validated_data)
            file_video.save()
            return file_video

    def to_representation(self, instance):
        return {'id': instance.id, 'video': instance.video.name, 'uid': instance.uid, "title": instance.title}
