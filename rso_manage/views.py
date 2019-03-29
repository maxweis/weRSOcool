from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RSOCreationForm
from .models import RSO

def AddRSO(request):
    if request.method == 'POST':
        form = RSOCreationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            date_established = form.cleaned_data.get('date_established')
            college_association = form.cleaned_data.get('college_association')
            icon = form.cleaned_data.get('icon')
            form_save = form.save(commit=False)
            form_save.creator = request.user.username
            form.save()
            return redirect('home')
    else:
        form = RSOCreationForm()

    return render(request, 'rso_registration.html', {'form' : form})

def rso_list(request):
    all_rsos = RSO.objects.raw('SELECT * FROM "rso_manage_rso"')
    return render(request, 'rso_list.html', {'all_rsos' : all_rsos})

def rso_profile(request, rso_name):
    rso = get_object_or_404(RSO, name=rso_name)
    return render(request, 'rso_profile.html', {'rso' : rso})

def register(request, rso_name):
    username = request.user.username
    member = Member.objects.get(username=username)
    rso = RSO.objects.get(name=rso_name)

    reg = Registrations(member=member, rso=rso)
    reg.save()
    return render(request, 'register_success.html', {'name' : username, 'rso' : rso_name})

def rso_members(request, rso_name):
    rso_id = RSO.objects.get(name=rso_name).id
    member_registrations = Registrations.objects.raw("SELECT * FROM users_registrations WHERE rso_id = {}".format(rso_id))
    return render(request, 'rso_members.html', {"member_registrations" : member_registrations})

def rso_delete(request, rso_name):
    if request.user.is_authenticated:
        try:
            cursor = connection.cursor()
            query = 'DELETE FROM "rso_manage_rso" WHERE rso_manage_rso.name = "{}" AND rso_manage_rso.creator = "{}"'.format(rso_name, request.user.username)
            cursor.execute(query)
            connection.commit()
            messages.success(request, "RSO deleted")
        except:
            messages.error(request, "RSO not found or you must be the creator of the RSO")
    else:
        messages.error(request, "You must be logged in to delete an RSO.")
    return redirect('/rso/')
