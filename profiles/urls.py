from django.urls import path
from . import views
from django.urls import path
from .views import admin_page, delete_user, delete_post
from .views import admin_login, admin_logout


urlpatterns = [
    path('upload/', views.upload, name='upload'), 
    path('result/', views.result, name='result'), 
    path('findhotel/', views.findhotel, name='findhotel'), 
    path('', views.homePage, name='home'),
    path('about_us/', views.aboutUs, name='aboutUs'),
    path('recipe_suggestion/', views.recipeSuggestion, name='recipeSuggestion'),
    path('news_section/', views.newsSection, name='newsSection'),
    path('scan_barcode/', views.scan_barcode, name='scan_barcode'),
    path('steps_start/', views.stepsStart, name='stepsStart'),
    path('chatbot/', views.chatbot, name='chatbot'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
     path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_post, name='create_post'),
    path('update/<str:post_id>/', views.update_post, name='update_post'),
    path('delete/<str:post_id>/', views.delete_post, name='delete_post'),
    path('community_forum/', views.community_forum, name='community_forum'),
    path('input-user-details/', views.input_user_details, name='input_user_details'),
    
    path('admin_page/', views.admin_page, name='admin_page'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('admin_login/', views.admin_login, name='admin_login'), 
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path("delete_user/<str:user_id>/", delete_user, name="delete_user"),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

]

