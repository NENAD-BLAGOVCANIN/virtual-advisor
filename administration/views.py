from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from main.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, F, Sum
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Avg
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils.dateformat import DateFormat
from django.core.exceptions import PermissionDenied

def dashboard(request):

    if request.user.is_admin:
        registered_users = User.objects.all().count()
        application_allowed_users = User.objects.filter(is_deleted = 0, application_access = User.APPLICATION_ACCESS_STATUS_ALLOWED).count()
        application_declined_users = User.objects.filter(is_deleted = 0, application_access = User.APPLICATION_ACCESS_STATUS_DECLINED).count()
        users_deleted = User.objects.filter(is_deleted=1).count()

        active_users = User.objects.all().count()

        admin_count = User.objects.filter(is_deleted = 0, is_admin = True).count()
        customer_count = User.objects.filter(is_deleted = 0, is_admin = False).count()

        current_date = datetime.now()

        userGrowthData = getUsersGrowthData()


        return render(request, 'dashboard.html', context={'registered_users':registered_users, 'users_deleted':users_deleted, 
            'current_date':current_date, 'userGrowthData':userGrowthData, 'application_allowed_users':application_allowed_users, 
            'application_declined_users':application_declined_users, 'admin_count':admin_count, 'customer_count':customer_count, 'active_users':active_users})
    else:
        raise PermissionDenied("You do not have permission to access this page")

def getUsersGrowthData():
    today = datetime.now().date()
    start_date = today - timedelta(days=365)

    data = (
        User.objects
        .annotate(month=TruncMonth('date_joined'))
        .filter(date_joined__gte=start_date)
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    labels = []
    values = []
    cumulative_count = 0

    for d in data:
        month_name = DateFormat(d['month']).format('F')
        labels.append(month_name)
        cumulative_count += d['count']
        values.append(cumulative_count)

    return {'labels': labels, 'values': values}


def usersView(request):

    if request.user.is_admin:

        new_users = User.objects.filter(application_access=User.APPLICATION_ACCESS_STATUS_PENDING, is_deleted=0)
        asigned_access_users = User.objects.exclude(application_access=User.APPLICATION_ACCESS_STATUS_PENDING, is_deleted=0)

        return render(request, 'users.html', context={'new_users': new_users, 'asigned_access_users':asigned_access_users})
    else:
        raise PermissionDenied("You do not have permission to access this page")

def allowUserApplicationAccess(request):

    if request.user.is_admin:
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        user.application_access = User.APPLICATION_ACCESS_STATUS_ALLOWED
        user.save()

        return redirect('/administration/users')
    else:
        raise PermissionDenied("You do not have permission to access this page")

def declineUserApplicationAccess(request):

    if request.user.is_admin:

        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        user.application_access = User.APPLICATION_ACCESS_STATUS_DECLINED
        user.save()

        return redirect('/administration/users')
    else:
        raise PermissionDenied("You do not have permission to access this page")