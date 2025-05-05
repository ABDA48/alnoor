from django.contrib import admin
from .models import Etudiant, ClassModel, Presence, Note, Ecolage, Avertissement, Boursier,EmploiduTemp,Professeur,Matiere,Personnel
 
from django.contrib.auth.models import User
 
class BoursierAdmin(admin.ModelAdmin):
    list_display = ( 'madressat', 'cheick', 'contact')
    list_filter = ('madressat',)  # Filter by madressat name
    search_fields = ( 'madressat', 'cheick')
    ordering = ('madressat',)
    
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('identifiant','nom', 'photo','date_de_naissance', 'nom_pere', 'nom_mere','parent_contact','address', 'boursier', 'date_entree', 'idclass')
    search_fields = ('identifiant','nom', 'nom_pere', 'nom_mere')
    list_filter = ('boursier', 'date_entree', 'idclass')  # Filter by scholarship, entry date, and class
    ordering = ('identifiant',)  # Default ordering by identifiant

class ClassModelAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    ordering = ('nom',)

class PresenceAdmin(admin.ModelAdmin):
    list_display = ('identifiant', 'date', 'idclass', 'presence')
    list_filter = ('presence', 'idclass', 'date')  # Filter by presence status, class, and date
    search_fields = ('identifiant__identifiant',)
    ordering = ('date',)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('identifiant','identifiant__nom','identifiant__photo','identifiant__boursier', 'annees', 'semestre', 'moyen', 'rang', 'type')
    list_filter = ('identifiant__nom','identifiant__boursier','semestre', 'annees', 'type', 'rang')  # Filter by semester, year, and type of note
    search_fields = ('identifiant__identifiant',)
    ordering = ('annees', 'semestre')

class EcolageAdmin(admin.ModelAdmin):
    list_display = ('identifiant__nom','identifiant__photo','identifiant__boursier','identifiant__idclass__nom' ,'date', 'payé')
    list_filter = ('payé', 'date','identifiant__boursier','identifiant__idclass__nom')  # Filter by paid status and date
    search_fields = ('identifiant__nom',)
    ordering = ('date',)

class AvertissementAdmin(admin.ModelAdmin):
    list_display = ('identifiant', 'date', 'raison', 'decision')
    list_filter = ('date',)  # Filter by date
    search_fields = ('identifiant__identifiant', 'raison')
    ordering = ('date',)



@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'email', 'telephone', 'date_embauche')
    list_filter = ('date_embauche',)  # Filter by date of hiring
    search_fields = ('nom', 'prenom', 'email')
    ordering = ('nom',)

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'professeur')
    list_filter = ('professeur',)  # Filter by professor
    search_fields = ('nom', 'professeur__nom', 'professeur__prenom')  # Search by subject name and professor name
    ordering = ('nom',)
@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'fonction', 'contact', 'date_d_embauche')
    list_filter = ('date_d_embauche',)  # Filter by date of hiring
    search_fields = ('nom', 'prenom')  # Search by name and email
    ordering = ('nom',)  # Ordering by last name

# Register the Personnel model with the custom admin interface


# Registering the models with the custom admin classes
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(ClassModel, ClassModelAdmin)
admin.site.register(Presence, PresenceAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Ecolage, EcolageAdmin)
admin.site.register(Avertissement, AvertissementAdmin)
admin.site.register(Boursier, BoursierAdmin)
admin.site.register(EmploiduTemp)

 
 
 
