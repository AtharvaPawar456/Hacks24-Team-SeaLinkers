from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),


    # path("upload_file/", views.upload_file, name="upload_file"),


    # path("showresult/<int:myid>", views.showresult, name="showresult"),


    path('user_login/',      views.user_login,     name='user_login'),
    path('user_logout/',     views.user_logout,    name='user_logout'),
    path('user_register/',   views.user_register,  name='user_register'),

    # path('apikeyGen/', views.your_view_function, name='your_view_function'),








    # path("business", views.business, name="Business"),
    # path("about/", views.about, name="AboutUs"),
    # path("contact/", views.contact, name="ContactUs"),
    # # path("products/<int:myid>", views.productView, name="ProductView"),
    # path("products/<str:myslug>", views.productView, name="ProductView"),

]
