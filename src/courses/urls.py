from django.urls import path
from . import views

urlpatterns = [
    path('<slug:course_id>/lesson/<slug:lesson_id>/', views.lesson_detail_view),
    path('<slug:course_id>/', views.cource_detail_view),
    path('', views.cource_list_view),

]

