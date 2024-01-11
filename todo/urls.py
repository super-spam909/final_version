from django.urls import path
from .views import TaskList, TaskDetail ,TaskCreate ,TaskUpdate , TaskDelete,custom_login, custom_signup
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('',TaskList.as_view(),name='task'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',custom_signup,name='register'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task-detail'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name='task-delete'),
    path('login/',custom_login,name='login'),




]