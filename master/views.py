from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from . forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.http import JsonResponse
from django.core.paginator import Paginator
from . serializers import *

from datetime import timedelta
from django.utils import timezone

def SignIn(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(username=email, password=password)
                login(request, user)
                # messages.success(request, "Login succesfully!")
                return redirect('dashboard')
            else:
                print(f"{form.errors = }")
                messages.error(request, "Invalid credentials!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = LoginForm()
            context = {}
            context['form'] = form
            return render(request, "login.html", context)
    else:
        return redirect('dashboard')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'dashboard.html')

def dashboardAPI(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        appointment = ClientAppointment.objects.filter(account_holder__id=request.user.id)
        paginator = Paginator(appointment, 1)  # 5 clients per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = ClientAppointmentsSerializers(page_obj.object_list, many=True)

        # Get current time and 2 months ago
        now = timezone.now()
        two_months_ago = now - timedelta(days=60)

        # New clients added in last 2 months
        new_clients_count = ClientAppointment.objects.filter(account_holder=request.user,
                                                             appointment_datetime__gte=two_months_ago,
                                                             client__role='client').values('client').distinct().count()

        # New appointments in last 2 months
        new_appointments_count = ClientAppointment.objects.filter(
            appointment_datetime__gte=two_months_ago,
            account_holder__id=request.user.id
        ).count()

        context = {}
        context['clients_data'] = serializer.data
        context['page'] = page_obj.number
        context['total_pages'] = paginator.num_pages
        context['new_clients'] = new_clients_count,
        context['new_appointments'] = new_appointments_count
        return JsonResponse(context)

def ClientAddAPI(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        user = User()
        user.username = request.POST.get('username')
        user.name = request.POST.get('name')
        user.role = 'client'
        user.save()
        return JsonResponse({'success': True, 'message': 'Your Client Created Successfuly', 'color_class' : 'success-toast'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error : {e}', 'color_class' : 'error-toast'})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    logout(request)
    return redirect('signin')


# abc