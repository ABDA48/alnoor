from django.shortcuts import render, redirect
from main.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
import json
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.db.models import Count
import datetime
from django.views.decorators.csrf import csrf_exempt
from main.models import MONTH_CHOICES,CLASS_CHOICES
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from datetime import date
from django.db.models import Avg

from django.http import HttpResponse
 
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import DetailView
from io import BytesIO
import os
import requests
 
from django.conf import settings

def calculate_age(birth_date):
    """ Helper function to calculate age """
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# Create your views here.
def loginSingup(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie !")  # Success message
            return redirect('home')  # Redirect to a home/dashboard page
        else:
            messages.error(request, "Email ou mot de passe incorrect.")  # Error message

    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})

@login_required(login_url='/login/') 
@group_required('admins')
def dashboard(request):
    classes=dict(CLASS_CHOICES)
    selected_class=request.POST.get('class', '')

    etudiants=Etudiant.objects.all() 
    professeurs=Professeur.objects.all()
    personelles=Personnel.objects.all()
    if selected_class:
        etudiants=etudiants.filter(idclass__nom=selected_class)
     # Gender Distribution
       # Gender Distribution
    gender_data = Etudiant.objects.values('genre').annotate(count=Count('genre'))
    if selected_class:
        gender_data = Etudiant.objects.filter(idclass__nom=selected_class).values('genre').annotate(count=Count('genre'))
    gender_labels = [item['genre'] for item in gender_data]
    gender_counts = [item['count'] for item in gender_data]

   
    # Boursier Status Distribution
    boursier_data = Etudiant.objects.values('boursier').annotate(count=Count('boursier'))
    boursier_labels = [item['boursier'] for item in boursier_data]
    boursier_counts = [item['count'] for item in boursier_data]

    # Presence Distribution
    presence_data = Presence.objects.values('presence').annotate(count=Count('presence'))
    if selected_class:
        presence_data = Presence.objects.filter(idclass__nom=selected_class).values('presence').annotate(count=Count('presence'))
    presence_labels = [item['presence'] for item in presence_data]
    presence_counts = [item['count'] for item in presence_data]

    # classes



    # Age Distribution
    students = Etudiant.objects.all()
    if selected_class:
        students=Etudiant.objects.filter(idclass__nom=selected_class)
    age_groups = {"3-10": 0, "11-14": 0, "15-18": 0, "19-21": 0, "22-25": 0, "26+": 0}
    for student in students:
        age = calculate_age(student.date_de_naissance)
        if 3 <= age <= 10:
            age_groups["3-10"] += 1
        elif 11 <= age <= 14:
            age_groups["11-14"] += 1
        elif 15 <= age <= 18:
            age_groups["15-18"] += 1
        elif 19 <= age <= 21:
            age_groups["19-21"] += 1
        elif 22 <= age <= 25:
            age_groups["22-25"] += 1
        else:
            age_groups["26+"] += 1

    context = {
        "etudiants":etudiants,"professeurs":professeurs,"personelles":personelles,
        'classes':classes,"selected_class":selected_class,
        "gender_labels": gender_labels, "gender_counts": gender_counts,
       
        "boursier_labels": boursier_labels, "boursier_counts": boursier_counts,
        "presence_labels": presence_labels, "presence_counts": presence_counts,
        "age_labels": list(age_groups.keys()), "age_counts": list(age_groups.values()),
    }
    return render(request,'main/home.html',context)


 





















@login_required(login_url='/login/')
def etudiants(request):
    etudiants = Etudiant.objects.all()
    all_classes = ClassModel.objects.values_list('nom', flat=True).distinct()
    query = request.POST.get('q', '')
    selected_class = request.GET.get('class', '')
    selected_boursier = request.GET.get('boursier', '')
    selected_genre=request.GET.get('genre', '')
    if query:
        etudiants = Etudiant.objects.filter(nom__icontains=query)
    if selected_class:
        etudiants = etudiants.filter(idclass__nom=selected_class)
    if selected_boursier:
        etudiants = etudiants.filter(boursier=selected_boursier)
    if selected_genre:
        etudiants=etudiants.filter(genre=selected_genre)
        print(selected_genre)
    students_count=etudiants.count()    
    paginator = Paginator(etudiants, 10)  # Show 10 students per page
    
    page_number = request.GET.get('page')  # Get the current page number from the request
    obj = paginator.get_page(page_number)  # Get the students for the current page
    
    return render(request,'main/etudiants.html',{'etudiants': obj,
                                                 'all_classes':all_classes,
                                                 "selected_class": selected_class,
                                                 'selected_boursier':selected_boursier,
                                                 'selected_genre':selected_genre,
                                                 'students_count':students_count
                                                 })

def etudiantPage(request,id):
    etudiant=Etudiant.objects.get(pk=id)
    return render(request,'main/etudiantpage.html',{"etudiant":etudiant})

@login_required(login_url='/login/')
def avertissements(request):
    # Handle the filters (date, reason, decision)
    q = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    raison_filter = request.GET.get('raison', '')
    decision_filter = request.GET.get('decision', '')

    avertissements = Avertissement.objects.all()

    if q:
        avertissements = avertissements.filter(
            identifiant__nom__icontains=q
        )
    if date_filter:
        avertissements = avertissements.filter(date=date_filter)
    if raison_filter:
        avertissements = avertissements.filter(raison__icontains=raison_filter)
    if decision_filter:
        avertissements = avertissements.filter(decision__icontains=decision_filter)
    paginator = Paginator(avertissements, 10)  # Show 10 students per page
    
    page_number = request.GET.get('page')  # Get the current page number from the request
    obj = paginator.get_page(page_number)  # Get the students for the current page

    return render(request,'main/avertissements.html',{'avertissements': obj,
        'q': q,
        'date_filter': date_filter,
        'raison_filter': raison_filter,
        'decision_filter': decision_filter,})

@login_required(login_url='/login/')
def classes(request):
    class_etudiants={}
    dict_class=dict(CLASS_CHOICES)
    for key,value in dict_class.items():
        etudiant_number=Etudiant.objects.filter(idclass__nom=key).count()
        class_etudiants[dict_class[key] ]=etudiant_number
    
    class_data = Etudiant.objects.values('idclass__nom').annotate(count=Count('idclass')).order_by("-count")
     

    class_labels = [item['idclass__nom'] for item in class_data]
    class_counts = [item['count'] for item in class_data]

    return render(request,'main/classes.html',{
        "class_etudiants":class_etudiants,
          "class_labels": class_labels, "class_counts": class_counts,
        })

@login_required(login_url='/login/')
def professeurs(request):
    query = request.GET.get('q', '')
    professeurs = Professeur.objects.all()
    if query:
        professeurs = professeurs.filter(nom__icontains=query)
    paginator = Paginator(professeurs, 10)  # Show 10 students per page
    
    page_number = request.GET.get('page')  # Get the current page number from the request
    obj = paginator.get_page(page_number)  # Get the students for the current page

    
    return render(request,'main/professeures.html',{"professeurs":obj})
@login_required(login_url='/login/')
def matieres(request):
    matieres= matieres = Matiere.objects.select_related('professeur', 'classe').all()
    professeurs=Professeur.objects.all()
    classes=ClassModel.objects.all()
    query=request.GET.get('q', '')
    if query:
        matieres=matieres.filter(nom__icontains=query)
    paginator=Paginator(matieres, 10)
    page_number=request.GET.get('page')
    obj=paginator.get_page(page_number)

    return render(request,'main/matieres.html',{'matieres':obj,'professeurs':professeurs,'classes':classes})




@login_required(login_url='/login/')
def ecolages(request):
    ecolages = Ecolage.objects.all()
    
    # Apply search filters
    search_query = request.GET.get('q')
    if search_query:
        ecolages = ecolages.filter(identifiant__nom__icontains=search_query)

    # Apply date filter
    selected_date = request.GET.get('date')
    if selected_date:
        ecolages = ecolages.filter(date=selected_date)

    # Apply payé filter
    selected_payé = request.GET.get('payé')
    if selected_payé:
        ecolages = ecolages.filter(payé=selected_payé)

    # Apply boursier filter
    selected_boursier = request.GET.get('boursier')
    if selected_boursier:
        ecolages = ecolages.filter(identifiant__boursier=selected_boursier)

    # Apply class filter
    selected_class = request.GET.get('class')
    if selected_class:
        ecolages = ecolages.filter(identifiant__idclass__nom=selected_class)

    # Pagination setup
    paginator = Paginator(ecolages, 10)  # Show 10 ecolages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'main/ecolages.html',{'ecolages':page_obj,
                                                'MONTH_CHOICES':MONTH_CHOICES,
                                                'selected_date':selected_date,
                                                'selected_payé':selected_payé,
                                                'selected_boursier':selected_boursier,
                                                'selected_class':selected_class,
                                                'CLASS_CHOICES':CLASS_CHOICES
                                                })

def personelles(request):
    # Get the search query from the GET parameters
    query = request.GET.get('q', '')  # If there's no query, default is an empty string
    
    # Start with all personnel
    personnels = Personnel.objects.all()
    all_fonctions=Personnel.objects.values_list("fonction",flat=True).distinct()
    # Apply search filter if query is provided
    if query:
        personnels = personnels.filter(nom__icontains=query)  # Filter by name
    selected_fonction = request.GET.get('fonction')
    if selected_fonction:
        personnels=personnels.filter(fonction=selected_fonction) 
    
    personnel_count=personnels.count()
    # Set up pagination (show 10 personnels per page)
    paginator = Paginator(personnels, 10)  # Show 10 personnels per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    obj = paginator.get_page(page_number)  # Get the personnels for the current page
    
    return render(request,'main/personnels.html', {"personnels": obj,"selected_fonction":selected_fonction,"all_fonctions":all_fonctions,'personnel_count':personnel_count})

@login_required(login_url='/login/')
def notes(request):
    # Get the filter parameters from the request
    semester = request.GET.get('semestre')
    select_classes = request.GET.get('classes')
    year = request.GET.get('annees')
    note_type = request.GET.get('type')
    rank = request.GET.get('rang')
    query = request.GET.get('q', '')
    classes=dict(CLASS_CHOICES)
    # Filter the notes based on the provided parameters
    notes = Note.objects.all()
    
    if query:
        notes = notes.filter(identifiant__nom__icontains=query)
    if semester:
        notes = notes.filter(semestre=semester)
    if year:
        notes = notes.filter(annees=year)
    if note_type:
        notes = notes.filter(type=note_type)
    if rank:
        notes = notes.filter(rang=rank)
    if select_classes:
        notes=notes.filter(identifiant__idclass__nom=select_classes)
    
    # Set up pagination
    paginator = Paginator(notes, 10)  # Show 10 notes per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the page object

        # Get filter parameters
    classe_filter = request.GET.get('classe', 'CE')
    annee_filter = request.GET.get('annee', 2025)
    semestre_filter = request.GET.get('semestre', 1)
    type_filter = request.GET.get('type', 'mensuelle')
    
    # Filter notes based on the provided filters
    notes_queryset = Note.objects.filter(annees=annee_filter, semestre=semestre_filter, type=type_filter)
    
    if classe_filter != 'tous':
        notes_queryset = notes_queryset.filter(identifiant__idclass__nom=classe_filter)
    
    # Aggregate average grade (moyenne) for each student in the filtered dataset
    notes_data = notes_queryset.values('identifiant__nom', 'identifiant__idclass__nom').annotate(avg_moyenne=Avg('moyen'))
     
    # Prepare data for Chart.js
    labels = []
    data = []
    
    for note in notes_data:
        labels.append(f"{note['identifiant__nom']} ({note['identifiant__idclass__nom']})")
        data.append(note['avg_moyenne'])

    
    # Pass the page object to the template
    return render(request, 'main/notes.html', {'notes': page_obj,  'labels': labels,"classes":classes,"select_classes":select_classes,
        'data': data,})
    

@login_required(login_url='/login/')
def presences(request):
    # Get all presences
    presences = Presence.objects.all().order_by('-date')
    
    # Get all classes for the filter dropdown
    all_classes = ClassModel.objects.all()
    
    # Handle search
    query = request.POST.get('q')
    if query:
        presences = presences.filster(
            Q(identifiant__nom__icontains=query) |
            Q(idclass__nom__icontains=query)
        )
    
    # Handle filters
    selected_class = request.POST.get('class')
    if selected_class:
        presences = presences.filter(idclass__nom=selected_class)
        
    selected_presence = request.POST.get('presence')
    if selected_presence:
        presences = presences.filter(presence=selected_presence)
        
    selected_date = request.POST.get('date')

    if selected_date:
        presences = presences.filter(date__date=selected_date)
    
    # Pagination
    paginator = Paginator(presences, 10)  # Show 10 presences per page
    page_number = request.GET.get('page')
    presences = paginator.get_page(page_number)
    
    context = {
        'presences': presences,
        'all_classes': all_classes,
        'selected_class': selected_class,
        'selected_presence': selected_presence,
        'selected_date': selected_date,
    }
    
    return render(request,'main/presences.html',context)
 
def get_classes(request):
    classes = ClassModel.objects.all().values("id", "nom")
    return JsonResponse(list(classes), safe=False)

def get_students(request):
    class_id = request.GET.get("class_id")
    students = Etudiant.objects.filter(idclass_id=class_id).values("id", "nom")
    return JsonResponse(list(students), safe=False)

@csrf_exempt  # TODO: Replace with proper CSRF handling in production
def submit_presences(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            class_id = data.get("class_id")
            absent_students = data.get("absents", [])
            
            all_students = Etudiant.objects.filter(idclass_id=class_id)
            
            if not class_id or not absent_students:
                return JsonResponse({"error": "Class ID and absent students are required"}, status=400)

             
            if absent_students:
                present_students_list = all_students.exclude(id__in=absent_students)
                absent_students_list = all_students.filter(id__in=absent_students)
            else:
                # If no absents, all are present
                present_students_list = all_students
                absent_students_list = []
             

            if not all_students.exists():
                return JsonResponse({"error": "No valid students found"}, status=400)
            for student in absent_students_list:
                Presence.objects.create(identifiant=student,date=datetime.datetime.now(),idclass=student.idclass,presence='absent')
            for student in present_students_list:
                Presence.objects.create(identifiant=student,date=datetime.datetime.now(),idclass=student.idclass,presence='present')
          
               # Efficient bulk insert

            return JsonResponse({"message": "Présences enregistrées!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def datepicker(request):
     if request.method == "POST":
        selected_date = request.POST.get("selected_date")
        if selected_date:
            # Process the date (e.g., save it to the database or return it back)
            # Example: returning the selected date as a JSON response
            return JsonResponse({"status": "success", "selected_date": selected_date})
        else:
            return JsonResponse({"status": "error", "message": "Date not provided"})
    



















def logoutView(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('loginSingup') 



 

 
    model = Etudiant

    def get(self, request, *args, **kwargs):
        identifiant = self.kwargs.get('identifiant')
        print("identifiant", identifiant)
        
        # Fetch the Etudiant instance
        etudiant = get_object_or_404(Etudiant, identifiant=identifiant)
        
        # Generate the main PDF
        main_pdf = self.generate_main_pdf(request, etudiant)
        
        # Return the PDF response
        response = HttpResponse(main_pdf.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="etudiant_{identifiant}.pdf"'
        return response

    def generate_main_pdf(self, request, etudiant):
        """Generate the main PDF with Etudiant details"""
        html_string = render_to_string('main/etudiantpage.html', {
            'etudiant': etudiant,
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL,
        })

        css = CSS(string=''' 
            @page { size: A4; margin: 2.5cm; @top-right { content: "Page " counter(page); }}
            body { font-family: Arial, sans-serif; line-height: 1.5; }
            .header { text-align: center; margin-bottom: 30px; }
            .profile-image { width: 150px; height: 150px; object-fit: cover; border-radius: 50%; margin: 0 auto; display: block; }
            .info-section { margin: 20px 0; border: 1px solid #ddd; padding: 20px; border-radius: 5px; }
            .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
            .info-item { margin-bottom: 10px; }
            .label { font-weight: bold; color: #444; }
            .value { color: #666; }
            .document-title { color: #2c3e50; font-size: 24px; margin-bottom: 20px; }
        ''')

        # Create a BytesIO object to store the PDF
        pdf_buffer = BytesIO()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer

    def combine_pdfs(self, main_pdf_buffer, acte_pdf):
        """Combine the main PDF with additional PDFs like acte_de_décé"""
        output = BytesIO()
        merger = PdfMerger()

        # Add the main PDF
        merger.append(main_pdf_buffer)

        try:
            # If acte_pdf is a FileField or path, append it
            if hasattr(acte_pdf, 'path'):
                merger.append(acte_pdf.path)
            else:
                acte_pdf_path = os.path.join(settings.MEDIA_ROOT, str(acte_pdf))
                if os.path.exists(acte_pdf_path):
                    merger.append(acte_pdf_path)
                else:
                    acte_pdf_url = request.build_absolute_uri(settings.MEDIA_URL + str(acte_pdf))
                    response = requests.get(acte_pdf_url)
                    if response.status_code == 200:
                        acte_pdf_buffer = BytesIO(response.content)
                        merger.append(acte_pdf_buffer)
        except Exception as e:
            print(f"Error combining PDFs: {e}")
            return main_pdf_buffer

        # Write the combined PDF to the output buffer
        merger.write(output)
        merger.close()
        output.seek(0)
        return output