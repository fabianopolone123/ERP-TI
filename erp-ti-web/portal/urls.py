from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("modulo/<str:module_key>/", views.module_page, name="module-page"),
]
