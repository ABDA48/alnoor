
from django.urls import path
from main import views

urlpatterns = [
     path('dashboard/',views.dashboard,name="home"),
     path('',views.loginSingup,name="acceuil"),
     path('login/',views.loginSingup,name="loginSingup"),

     path('dashboard/',views.dashboard,name="dashboard"),
     path('etudiants/',views.etudiants,name="etudiants"),

      path('avertissements/',views.avertissements,name="avertissements"),
       path('classes/',views.classes,name="classes"),
        path('ecolages/',views.ecolages,name="ecolages"),
 path('professeurs/',views.professeurs,name="professeurs"),
  path('personelles/',views.personelles,name="personelles"),
  path('matieres/',views.matieres,name="matieres"),
         path('presences/',views.presences,name="presences"),
          path('notes/',views.notes,name="notes"),
     path("api/classes/", views.get_classes, name="get_classes"),
    path("api/students/", views.get_students, name="get_students"),
    path("api/presences/", views.submit_presences, name="submit_presences"),

      path("api/date/", views.datepicker, name="datepicker"),
   path('logout/',views.logoutView,name="logout"),


  # index
   path('etudiants/<int:id>',views.etudiantPage,name="etudiantPage"),
 
]