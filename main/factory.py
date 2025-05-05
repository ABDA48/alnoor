
from datetime import datetime, timedelta
import random
from main.models import ClassModel, Etudiant, Presence, Note, Ecolage, Avertissement, Boursier, EmploiduTemp
from main.models import CLASS_CHOICES, PRESENCE_CHOICES, MONTH_CHOICES, DAY_CHOICES
from django.utils import timezone
# Sample data lists
base_names  = ["Adam Smith", "Marie Curie", "Albert Einstein", "Isaac Newton", "Grace Hopper", 
        "Alan Turing", "Ada Lovelace", "Charles Darwin", "Jane Goodall", "Nikola Tesla"]

adresses = ["123 Rue Paris", "456 Avenue Lyon", "789 Boulevard Nice", "321 Rue Marseille",
           "654 Avenue Toulouse", "987 Boulevard Nantes", "147 Rue Bordeaux", "258 Avenue Lille",
           "369 Boulevard Strasbourg", "741 Rue Montpellier"]

matieres = ["Mathématiques", "Physique", "Chimie", "Biologie", "Histoire", 
           "Géographie", "Français", "Anglais", "Informatique", "Sport"]

professeurs = ["Prof. Martin", "Prof. Bernard", "Prof. Thomas", "Prof. Robert", "Prof. Richard",
              "Prof. Petit", "Prof. Durand", "Prof. Leroy", "Prof. Moreau", "Prof. Simon"]

madressats = ["Madressat Al-Azhar", "Madressat Al-Nur", "Madressat Al-Iman", "Madressat Al-Huda",
             "Madressat Al-Fajr", "Madressat Al-Salam", "Madressat Al-Rahma", "Madressat Al-Ihsan",
             "Madressat Al-Hidaya", "Madressat Al-Baraka"]

noms = [random.choice(base_names) for _ in range(100)]
# Create classes first
classes = []
for class_choice in CLASS_CHOICES:  # Take first 10 classes
    class_obj = ClassModel.objects.create(
        nom=class_choice[0]
    )
    classes.append(class_obj)

# Create students
students = []
for i in range(len(noms)):
    student = Etudiant.objects.create(
        identifiant=f"STU{2024}{i+1:03d}",
        nom=noms[i],
        date_de_naissance=datetime(2000 + i, 1, 1).date(),
        nom_pere=f"Mr. {noms[i].split()[-1]}",
        nom_mere=f"Mme. {noms[i].split()[-1]}",
        genre='M' if i % 2 == 0 else 'F',
        parent_contact=f"+33 6{i+1:08d}",
        address=random.choice(adresses),
        boursier='oui' if i < 3 else 'non',
        date_entree=datetime(2023, 9, 1).date(),
        idclass=classes[i % len(classes)]
    )
    students.append(student)

# Create presence records
students=Etudiant.objects.all()
for student in students:
    for _ in range(10):
        random_days = random.randint(0, (datetime(2026, 12, 31) - datetime.today()).days)
        Presence.objects.create(
            identifiant=student,
            date=timezone.now() + timedelta(days=random_days),
            idclass=student.idclass,
            presence=random.choice(['present', 'present','absent'])
        )

# Create notes
for student in students:
    for _ in range(10):
        Note.objects.create(
            identifiant=student,
            annees=2025,
            semestre=random.randint(1, 5),
            moyen=round(random.uniform(10.0, 20.0) * 2) / 2,
            rang=random.randint(1, 30),
            type=random.choice(['mensuelle', 'mensuelle','mensuelle','annuelle'])
        )

# Create ecolage
for student in students:
    for month in MONTH_CHOICES:
        Ecolage.objects.create(
            identifiant=student,
            date=month[0],
            payé=random.choice(['oui','oui' ,'oui','oui','non'])
        )

# Create avertissements
reasons = ["Absence non justifiée", "Comportement inapproprié", "Retard répété", 
          "Non-respect du règlement", "Devoir non rendu"]
decisions = ["Avertissement verbal", "Convocation des parents", "Exclusion temporaire", 
            "Travail supplémentaire", "Surveillance accrue"]

for student in students:
    for _ in range(5):
        Avertissement.objects.create(
            identifiant=student,
            date=timezone.now() - timedelta(days=random.randint(0, 365)),
            raison=random.choice(reasons),
            decision=random.choice(decisions)
        )

# Create boursiers
for i, student in enumerate(students):  # Create for first 10 students
    if student.boursier == 'oui':
        Boursier.objects.create(
            identifiant=student,
            madressat=madressats[i],
            cheick=f"Cheick {noms[i].split()[-1]}",
            contact=f"+33 7{i+1:08d}"
        )

# Create emploi du temps
classes=ClassModel.objects.all()
for class_obj in classes:
    for i in range(10):
        start_time = datetime.now().replace(hour=8 + i, minute=0)
        EmploiduTemp.objects.create(
            matiere=matieres[i],
            professeur=professeurs[i],
            commence=start_time,
            finish=start_time + timedelta(hours=1),
            jours=random.choice([day[0] for day in DAY_CHOICES]),
            idclass=class_obj
        )


print(f"Classes: {ClassModel.objects.count()}")
print(f"Students: {Etudiant.objects.count()}")
print(f"Presence records: {Presence.objects.count()}")
print(f"Notes: {Note.objects.count()}")
print(f"Ecolage records: {Ecolage.objects.count()}")
print(f"Avertissements: {Avertissement.objects.count()}")
print(f"Boursiers: {Boursier.objects.count()}")
print(f"Emploi du temps entries: {EmploiduTemp.objects.count()}")

import random
from datetime import datetime, timedelta
from main.models import Professeur, Matiere, ClassModel  # Update with your actual app name

# Sample names for professors
professeur_noms = [
    "Smith", "Johnson", "Brown", "Williams", "Jones", 
    "Miller", "Davis", "Garcia", "Rodriguez", "Martinez"
]
professeur_prenoms = [
    "Alice", "Bob", "Charlie", "David", "Eva", 
    "Frank", "Grace", "Helen", "Isaac", "Julia"
]

# Sample subjects
matieres_noms = [
    "Mathématiques", "Physique", "Chimie", "Biologie", "Informatique",
    "Histoire", "Géographie", "Philosophie", "Anglais", "Français"
]

# Get all available classes
classes = list(ClassModel.objects.all())

# Function to generate a random date
def random_date(start_year=1990, end_year=2022):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Create 20 professors
professeurs = []
for i in range(20):
    nom = random.choice(professeur_noms)
    prenom = random.choice(professeur_prenoms)
    email = f"{prenom.lower()}.{nom.lower()+str(i)}@example.com"
    telephone = f"+261 {random.randint(320000000, 329999999)}"
    adresse = f"Rue {random.randint(1, 100)}, Ville {random.randint(1, 10)}"
    date_naissance = random_date(1960, 1995)
    date_embauche = random_date(2010, 2024)
    idclass = random.choice(classes) if classes else None
    professeur = Professeur.objects.create(
        nom=nom,
        prenom=prenom,
        email=email,
        telephone=telephone,
        adresse=adresse,
        date_naissance=date_naissance,
        date_embauche=date_embauche,
        idclass=idclass
    )
    professeurs.append(professeur)

# Create 20 subjects and assign random professors
professeurs=list(Professeur.objects.all())
for _ in range(20):
    nom = random.choice(matieres_noms)
    professeur = random.choice(professeurs)
    
    Matiere.objects.create(
        nom=nom,
        professeur=professeur
    )

print("20 Professeurs and 20 Matières have been successfully created!")

from main.models import Personnel  # Replace 'myapp' with the name of your app

# Create 20 example Personnel
personnel_data = [
    ('John', 'Doe', 'Manager', '0701234567', '2015-03-10'),
    ('Jane', 'Smith', 'Secretary', '0702345678', '2016-07-21'),
    ('Albert', 'Johnson', 'Developer', '0703456789', '2017-09-30'),
    ('Emily', 'Davis', 'Designer', '0704567890', '2018-06-15'),
    ('Michael', 'Wilson', 'Accountant', '0705678901', '2019-04-02'),
    ('Sarah', 'Moore', 'HR Specialist', '0706789012', '2020-01-18'),
    ('David', 'Taylor', 'Team Leader', '0707890123', '2021-11-05'),
    ('Laura', 'Anderson', 'Marketing Specialist', '0708901234', '2020-03-19'),
    ('James', 'Thomas', 'Sales Representative', '0709012345', '2022-02-25'),
    ('Maria', 'Jackson', 'Customer Support', '0700123456', '2021-08-30'),
    ('Robert', 'White', 'IT Support', '0701239876', '2019-05-12'),
    ('Sophia', 'Harris', 'Project Manager', '0702348765', '2018-10-20'),
    ('Daniel', 'Martin', 'Software Engineer', '0703457654', '2017-02-14'),
    ('Olivia', 'Garcia', 'Content Writer', '0704566543', '2020-07-10'),
    ('William', 'Clark', 'Sales Manager', '0705675432', '2021-12-01'),
    ('Lily', 'Rodriguez', 'Customer Success', '0706784321', '2019-08-24'),
    ('Daniel', 'Lewis', 'Product Designer', '0707893210', '2018-01-23'),
    ('Mason', 'Lee', 'Operations Manager', '0708902109', '2022-06-11'),
    ('Chloe', 'Walker', 'Public Relations', '0709011098', '2021-09-17'),
    ('Lucas', 'Allen', 'Legal Advisor', '0700120987', '2020-12-05')
]

# Create personnel records using the data
for nom, prenom, fonction, contact, date_d_embauche in personnel_data:
    Personnel.objects.create(
        nom=nom,
        prenom=prenom,
        fonction=fonction,
        contact=contact,
        date_d_embauche=date_d_embauche
    )

# Verify that the Personnel objects were created
Personnel.objects.all()
