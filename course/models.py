from django.db import models
import datetime
from users import models as user_model
import uuid
from django.contrib.postgres.fields import ArrayField
from utils import constant


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        # indexes = [
        #     models.Index(
        #         fields=[
        #             'deleted'
        #         ]
        #     )
        # ]

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(BaseModel, self).save(*args, **kwargs)


def upload_path(instance, file_name):
    return '/'.join(['video', file_name])


class VideosModel(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    video = models.FileField(upload_to='upload_path', blank=True, null=True)
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        db_table = 'tbl_video'
        ordering = ['id']


class CourseModel(BaseModel):
    photo = models.ForeignKey(user_model.PhotoModel, related_name='photo_course', on_delete=models.CASCADE, null=True,
                              blank=True)
    title = models.CharField(max_length=255)
    old_price = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(
        user_model.User, related_name='author_course_user', on_delete=models.CASCADE, null=True, blank=True)
    new_price = models.IntegerField(default=0, null=True, blank=True)
    background = models.ImageField(upload_to='background/', blank=True)
    registration_number = models.IntegerField(default=0)
    type = ArrayField(models.IntegerField(choices=constant.COURSE_TYPE_OPTION,
                                          default=constant.COURSE_OTHER), blank=True, null=True)
    description = models.CharField(max_length=500, default="")
    status = models.SmallIntegerField(choices=constant.STATUS_COURSE_OPTION,
                                      default=constant.STATUS_COURSE_IS_NEW, blank=True, null=True)
    reason = models.CharField(max_length=255, default="")
    list_video = models.CharField(
        blank=True, null=True, max_length=10000, default="")
    course_temporary = models.BooleanField(default=True)

    class Meta:
        db_table = 'tbl_course'
        ordering = ['id']


class KeyActiveModel(BaseModel):
    key_active = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        CourseModel, related_name='key_active_course', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_key_active'
        # ordering = ['id']


class FeelingStudentModel(BaseModel):
    description = models.CharField(max_length=255, blank=False, null=False)
    course = models.ForeignKey(
        CourseModel, related_name='feeling_student_course', on_delete=models.CASCADE)
    descriptions = models.CharField(max_length=255)

    class Meta:
        db_table = 'tbl_feeling_student'
