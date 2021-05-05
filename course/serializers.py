from abc import ABC

from rest_framework import serializers
from .models import CourseModel, FeelingStudentModel, VideosModel, KeyActiveModel
from django.db import transaction
import uuid

from utils import exception
from users import models as model_user
from users.serializers import GetAllPhotoSerializer, GetAllUserSerializer


class GetAllCourseSerializer(serializers.ModelSerializer):
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
    user = GetAllUserSerializer()
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


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ['id', 'photo', 'old_price', 'title',
                  'type', 'description', 'list_video']

    def validate(self, attrs):
        required_fields = ['photo', 'old_price',
                           'title', 'type', 'description']
        for field in required_fields:
            if self.initial_data.get(field, None) is None:
                raise exception.RequireValue(detail=f"{field} is require!")

        check_math = CourseModel.objects.filter(
            title=self.initial_data['title'].strip())
        if check_math.count() > 0:
            raise exception.ExistedValue
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context['request'].user
            instance = CourseModel.objects.create(**validated_data)
            id = instance.id
            for key_active in range(10):
                create_active_key = KeyActiveModel.objects.create(**{'course_id':id})
                create_active_key.save()
            instance.user = user
            instance.save()
            return instance


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ['id','photo', 'old_price', 'title',
                  'type', 'description', 'list_video']

    def validate(self, attrs):
        required_fields = ['photo', 'old_price',
                           'title', 'type', 'description']
        for field in required_fields:
            if self.initial_data.get(field, None) is None:
                raise exception.RequireValue(detail=f"{field} is require!")
        check_math = CourseModel.objects.filter(
            title=self.initial_data['title'].strip())
        if check_math.count() > 0:
            raise exception.ExistedValue
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            # for field in validated_data:
            #     setattr(instance, field, getattr(validated_data,field))
            instance.photo = validated_data['photo']
            instance.title = validated_data['title']
            instance.old_price = validated_data['old_price']
            instance.type = validated_data['type']
            instance.list_video = validated_data['list_video']
            instance.description = validated_data['description']
            instance.save()
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

class CheckDiscountSerializer(serializers.Serializer):
    class Meta:
        model = VideosModel
        fields = []

    def validate(self, attrs):
        code_discount = self.initial_data.get('discount', None)
        if code_discount is None:
            raise exception.RequireValue(detail="discount là bắt buộc!")
        attrs['discount'] = code_discount
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            print(validated_data,'validated_data')
            # file_video = VideosModel.objects.create(**validated_data)
            return {'result': False}

    def to_representation(self, instance):
        return {'is_valid': instance.get('result')}

class ActivateCourseSerializer(serializers.Serializer):
    class Meta:
        model = KeyActiveModel
        fields = []

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            code_activate = self.initial_data.get('key_active', None)
            match_course = KeyActiveModel.objects.filter(key_active__exact=code_activate).first()
            if match_course is None:
                raise exception.DoesNotExist(detail="Mã không tồn tại hoặc đã được sử dụng")
            course = match_course.course
            match_course.delete()
            id = course.id
            create_active_key = KeyActiveModel.objects.create(**{'course_id': id})
            create_active_key.save()
            return course

    def to_representation(self, instance):
        return {'id': instance.id, 'title': instance.title}
