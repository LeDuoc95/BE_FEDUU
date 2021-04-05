from django.shortcuts import render
from rest_framework.views import APIView
from utils import exception, permissions
from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.response import Response
from .models import CourseModel, FeelingStudentModel
from .serializers import GetAllCourseSerializer, CreateCourseSerializer, DeleteCourseSerializer, UpdateCourseSerializer, \
    CreateFeelingStudentModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import CursorPagination, PageNumberPagination
from django.contrib.auth.models import User


class GetCourseForLecturerAndAdminView(generics.GenericAPIView):
    queryset = CourseModel.objects.all()
    serializer_class = GetAllCourseSerializer
    # pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'new_price']

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            list_course = CourseModel.objects.filter(deleted=False)
        else:
            list_course = CourseModel.objects.select_related('user').filter(user_id=request.user.id, deleted=False)
            if request.user.position == 2:
                list_course = CourseModel.objects.all()
        queryset = self.filter_queryset(list_course)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetAllCourseSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllCourseView(generics.GenericAPIView):
    queryset = CourseModel.objects.all()
    serializer_class = GetAllCourseSerializer
    authentication_classes = []
    permission_classes = []
    # pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'new_price']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = GetAllCourseSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DetailCourseView(generics.ListAPIView):
    queryset = CourseModel.objects.all()
    serializer_class = GetAllCourseSerializer

    def get_object(self):
        pk = self.kwargs['id']
        data = CourseModel.objects.filter(pk=pk)
        if data.count() < 1:
            raise exception.DoesNotExist(
                detail=f"course with id {pk} does not exist")
        return data

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        serializer = GetAllCourseSerializer(item, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateCourseView(generics.CreateAPIView):
    serializer_class = CreateCourseSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        raise exception.APIException()


class UpdateCourseView(generics.GenericAPIView):
    serializer_class = UpdateCourseSerializer
    permission_classes = []

    def get_object(self):
        pk = self.kwargs['id']
        course = CourseModel.objects.filter(pk=pk)
        if course.count() > 0:
            return course.first()
        raise exception.DoesNotExist(
            detail=f"course with id {pk} does not exist")

    def put(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        raise exception.APIException()


class DeleteCourseView(generics.DestroyAPIView):
    serializer_class = DeleteCourseSerializer
    queryset = CourseModel.objects.all()
    permission_classes = []

    def get_object(self):
        pk = self.kwargs['id']
        course = CourseModel.objects.filter(id=pk)
        if course.count() > 0:
            return course.first()
        raise exception.DoesNotExist(
            detail=f"course with id {pk} does not exist")

    def delete(self, request, *args, **kwargs):
        obj_delete = self.get_object()
        serializer = self.get_serializer(obj_delete, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        raise exception.APIException()


class CreateFeelingStudentModelView(generics.ListAPIView):
    serializer_class = CreateFeelingStudentModelSerializer
    queryset = FeelingStudentModel.objects.all()

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        raise exception.APIException()
