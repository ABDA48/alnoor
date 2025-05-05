from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
BOURSIER_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
    ]
PRESENCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
SEMESTRE_CHOICES = [
        (1, 'Semestre 1'),
        (2, 'Semestre 2'),
        (3, 'Semestre 3'),
        (4, 'Semestre 4'),
        (5, 'Semestre 5'),
        (6, 'Semestre 6'),
        (0, 'Annuelle'),
    ]
TYPE_CHOICES = [
        ('mensuelle', 'Mensuelle'),
        ('annuelle', 'Annuelle'),
    ]
MONTH_CHOICES = [
        ('janvier', 'Janvier'), ('février', 'Février'), ('mars', 'Mars'), ('avril', 'Avril'),
        ('mai', 'Mai'), ('juin', 'Juin'), ('juillet', 'Juillet'), ('août', 'Août'),
        ('septembre', 'Septembre'), ('octobre', 'Octobre'), ('novembre', 'Novembre'), ('décembre', 'Décembre')
    ]
PAYE_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
    ]
Genre_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
CLASS_CHOICES = [
    ('MS', 'Moyenne Section'),
    ('GS', 'Grande Section'),
    ('CP1', 'Cours préparatoire 1'),
    ('CP2', 'Cours préparatoire 2'),
    ('CE', 'Cours élémentaire'),
  
    ('CM1', 'Cours moyen 1'),
    ('CM2', 'Cours moyen 2'),
    ('6', 'Sixième'),
    ('5', 'Cinquième'),
    ('4', 'Quatrième'),
    ('3', 'Troisième'),
    ('2nd', 'Seconde'),
    ('1er', 'Première'),
    ('Tle', 'Terminale'),
]    

DAY_CHOICES = [
    ('Monday', 'Lundi'),
    ('Tuesday', 'Mardi'),
    ('Wednesday', 'Mercredi'),
    ('Thursday', 'Jeudi'),
    ('Friday', 'Vendredi'),
    ('Saturday', 'Samedi'),
    ('Sunday', 'Dimanche'),
]
class ClassModel(models.Model):
    nom = models.CharField(max_length=100, choices=CLASS_CHOICES, verbose_name="Nom de la classe")
    
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name = "Classe"  # Singular form
        verbose_name_plural = "Classes"  # Plural form


class Boursier(models.Model):
    madressat = models.CharField(max_length=200, verbose_name="Nom de Madressat")
    cheick = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cheick Responsable")
    contact = models.CharField(max_length=100, blank=True, null=True, verbose_name="Contact de Madressat")
    
    def __str__(self):
        return f"{self.madressat}"
class Etudiant(models.Model):
    identifiant = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100,null=True,blank=True,verbose_name="Nom de l'Etudiants")
    photo = models.ImageField(upload_to='etudiants_photos/', default='default.png',blank=True, null=True,verbose_name="Photo de l'Etudiants")
    date_de_naissance = models.DateField(verbose_name="Date de Naissance")
    nom_pere = models.CharField(max_length=100,null=True,blank=True,verbose_name="Nom du Père")
    nom_mere = models.CharField(max_length=100,null=True,blank=True,verbose_name="Nom de la Mère")
    genre=models.CharField(max_length=10,choices=Genre_CHOICES,blank=True,null=True)
    parent_contact = models.CharField(max_length=100,null=True,blank=True,verbose_name="Contact des parents")
    address = models.TextField()
    boursier = models.CharField(max_length=3, choices=BOURSIER_CHOICES,default='non', verbose_name="Boursier")
    date_entree = models.DateField(null=True,blank=True,verbose_name="Date d'Entrée")
    idclass=models.ForeignKey(ClassModel, on_delete=models.SET_NULL,verbose_name="Classe Etudiants",null=True)
    idboursier=models.ForeignKey(Boursier, on_delete=models.SET_NULL,verbose_name="Boursier Etudiants",null=True)
    def __str__(self):
        return self.identifiant
    def Image(self):
        return mark_safe(f'<img src="{self.photo.url}" width="50" height="50" style="border-radius: 50%;" />')
    



class Presence(models.Model):
    identifiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Date",auto_now_add=True)
    idclass = models.ForeignKey(ClassModel, on_delete=models.CASCADE, verbose_name="Classe")
    presence = models.CharField(max_length=7, choices=PRESENCE_CHOICES,default="present", verbose_name="Présence")
     
    
    def __str__(self):
        return f"{self.identifiant} - {self.date} - {self.presence}"

class Note(models.Model):
    identifiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    annees = models.IntegerField(default='2025', verbose_name="Année")
    semestre = models.IntegerField(choices=SEMESTRE_CHOICES,default='semester 1', verbose_name="Semestre")
    moyen = models.FloatField(verbose_name="Moyenne")
    rang = models.IntegerField(blank=True,null=True,verbose_name="Rang")
    fichier = models.FileField(upload_to='notes/', blank=True, null=True, verbose_name="Fichier")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,default='mensuelle', verbose_name="Type")
    def Image(self):
        return mark_safe(f'<img src="{self.identifiant.photo.url}" width="50" height="50" style="border-radius: 50%;" />')
    
    def __str__(self):
        return f"{self.identifiant} - {self.annees} - {self.semestre}"

class Ecolage(models.Model):
    identifiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date = models.CharField(max_length=10, choices=MONTH_CHOICES, verbose_name="Mois")
    payé = models.CharField(max_length=3, choices=PAYE_CHOICES, verbose_name="Payé")
    def Image(self):
        return mark_safe(f'<img src="{self.identifiant.photo.url}" width="50" height="50" style="border-radius: 50%;" />')
    def __str__(self):
        return f"{self.identifiant} - {self.date} - {self.payé}"

class Avertissement(models.Model):
    identifiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date = models.DateField(blank=True,null=True,verbose_name="Date")
    raison = models.TextField(blank=True,null=True,verbose_name="Raison")
    decision = models.TextField(blank=True,null=True,verbose_name="Décision")
    def Image(self):
        return mark_safe(f'<img src="{self.identifiant.photo.url}" width="50" height="50" style="border-radius: 50%;" />')

    def __str__(self):
        return f"{self.identifiant} - {self.date}"
    

    
class EmploiduTemp(models.Model):
    matiere = models.CharField(max_length=100)  # Class name
    professeur = models.CharField(max_length=100, blank=True, null=True)  # Instructor
    commence = models.DateTimeField()  # Start time
    finish = models.DateTimeField()  # End time
    jours = models.CharField(max_length=10,choices=DAY_CHOICES)  # E.g., Monday, Tuesday, etc.
    idclass=models.ForeignKey(ClassModel, on_delete=models.SET_NULL,verbose_name="Classe Etudiants",null=True)




class Professeur(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    date_naissance = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    photo = models.ImageField(upload_to='professeures_photos/', default='default.png',blank=True, null=True,verbose_name="Photo du Professeur")
    def Image(self):
        return mark_safe(f'<img src="{self.photo.url}" width="50" height="50" style="border-radius: 50%;" />')
    class Meta:
        verbose_name = "Professeur"
        verbose_name_plural = "Professeurs"

    def __str__(self):
        return f"{self.prenom} {self.nom}"

 

class Personnel(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")  # Last name
    prenom = models.CharField(max_length=100, verbose_name="Prénom")  # First name
    fonction = models.CharField(max_length=100, verbose_name="Fonction")  # Job position
    contact = models.CharField(max_length=15, verbose_name="Contact")  # Contact number
    date_d_embauche = models.DateField(verbose_name="Date d'embauche")  # Hiring date
    photo = models.ImageField(upload_to='personnel_photos/', default='default.png',blank=True, null=True,verbose_name="Photo de Personnel")
    def Image(self):
        return mark_safe(f'<img src="{self.photo.url}" width="50" height="50" style="border-radius: 50%;" />')
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.fonction}"

    class Meta:
        verbose_name = "Personnel"
        verbose_name_plural = "Personnel"


class Matiere(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la matière")
    professeur = models.ForeignKey(
        Professeur, on_delete=models.SET_NULL, null=True, related_name="matieres", verbose_name="Professeur"
    )
    classe=models.ForeignKey(ClassModel, on_delete=models.SET_NULL,verbose_name="Classe Etudiants",null=True)
    def Image(self):
        return mark_safe(f'<img src="{self.professeur.photo.url}" width="50" height="50" style="border-radius: 50%;" />')


    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"

    def __str__(self):
        return self.nom

