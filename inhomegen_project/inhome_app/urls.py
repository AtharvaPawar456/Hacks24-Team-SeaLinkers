from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    
    path("dashboard/", views.dashboard, name="dashboard"),
    path("viewprojects/", views.viewprojects, name="viewprojects"),
    path('dashboard_v2/<str:proj_name>/', views.dashboard_v2, name='dashboard_v2'),


    path('Budget/<str:genimgid>/', views.Budget, name='Budget'),

    path('revision/', views.revision, name='revision'),

    # path("upload_file/", views.upload_file, name="upload_file"),

    path("addproject/", views.addproject, name="addproject"),
    path("addroom/", views.addroom, name="addroom"),

    path("generate/", views.generate, name="generate"),

    path("view_data/", views.view_data, name="view_data"),

    # path("showresult/<int:myid>", views.showresult, name="showresult"),

    path('convert_image_to_svg/<int:myid>/', views.convert_image_to_svg, name='convert_image_to_svg'),

    path('user_login/',      views.user_login,     name='user_login'),
    path('user_logout/',     views.user_logout,    name='user_logout'),
    path('user_register/',   views.user_register,  name='user_register'),

    # path('apikeyGen/', views.your_view_function, name='your_view_function'),



    path('convert_image_to_svg/<int:myid>/', views.convert_image_to_svg, name='convert_image_to_svg'),






    # path("business", views.business, name="Business"),
    # path("about/", views.about, name="AboutUs"),
    # path("contact/", views.contact, name="ContactUs"),
    # # path("products/<int:myid>", views.productView, name="ProductView"),
    # path("products/<str:myslug>", views.productView, name="ProductView"),

]
