from rest_framework import serializers
from .models import CourseModel, FeelingStudentModel
from django.db import transaction
from utils import exception
from users import models as model_user


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
            'reason'
        ]


class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ['id', 'photo', 'new_price', 'title', 'type', 'description']

    def validate(self, attrs):
        user_id = self.context.get('request').user.id
        user = model_user.User.objects.filter(id=user_id).first()
        required_fields = ['photo', 'new_price', 'title', 'type', 'description']
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
            print(validated_data, 'validated_datavalidated_datavalidated_data')
            # instance = FeelingStudentModel.objects.create(**validated_data)
            return validated_data
