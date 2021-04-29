from django.urls import path, include
from django.conf.urls import url
from .views import GetAllUserView, CreateUserView, ChangePasswordView
from .views import MyTokenObtainPairView, CustomTokenRefreshView, ResetPasswordView, LoginWithNoPasswordView, UpdateUserView, DeleteUserView, UploadPhotoView, GetAllPhotoView

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('upload-images', UploadPhotoView.as_view()),
    path('login-no-pass', LoginWithNoPasswordView.as_view()),
    path('login', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('list', GetAllUserView.as_view(), name='list-user'),
    path('create', CreateUserView.as_view(), name='create-user'),
    # url(r'^list/(?P<id>\d+)$',
    #     DetailCourseView.as_view(), name='detail-user'),
    path('update', UpdateUserView.as_view(), name='update-user'),
    path('photo', GetAllPhotoView.as_view(), name='get-photo'),
    url(r'^delete/(?P<pk>\d+)$', DeleteUserView.as_view(), name='delete-user'),
]
