from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexPage, name='index'),
    path('dashboard/', views.dashboardPage, name='dashboard'),
    path('reviews/', views.reviewsPage, name='reviews'),
    path('suggestions/<str:sentiment>/<str:review>', views.suggestionPage, name='suggestion'),
]
