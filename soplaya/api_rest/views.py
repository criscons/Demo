from django.shortcuts import render
from django.db.models import Sum
from api_rest.uploadfile import import_report
from api_rest.models import Report
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import connection
from django.http import JsonResponse




from rest_framework import viewsets
from . import serializers

#API
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = serializers.ReportSerializer


#LOAD DATA
def loadData(request):
    import_report()
    result = Report.objects.all()
    context = {
        "object_list" : result
        }
    return render(request, "index.html", context)

#RESET DATA
def resetData(request):
    result = Report.objects.all().delete()
    return HttpResponseRedirect(reverse('home'))

#DIFF planned_hours - actual_hours & budget - sells
def differences(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                date,
                restaurant,
                planned_hours,
                actual_hours,
                budget,
                sells,
                (planned_hours - actual_hours) AS difference_hours,
                (budget - sells) AS difference_budget
            FROM
                report
        """)
        results = cursor.fetchall()
    data = []
    for row in results:
        report = {
            'date' : row[0],
            'restaurant' : row[1],
            'planned_hours': row[2],
            'actual_hours': row[3],
            'budget': row[4],
            'sells': row[5],
            'difference_hours': row[6],
            'difference_budget': row[7],
        }
        data.append(report)
        context ={
            "data" : data
            }
    return render(request, "differences.html", context)


#JSON DIFF planned_hours - actual_hours & budget - sells
def calculate_differences(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                planned_hours,
                actual_hours,
                budget,
                sells,
                (planned_hours - actual_hours) AS difference_hours,
                (budget - sells) AS difference_budget
            FROM
                report
        """)
        results = cursor.fetchall()
    data = []
    for row in results:
        report = {
            'planned_hours': row[0],
            'actual_hours': row[1],
            'budget': row[2],
            'sells': row[3],
            'difference_hours': row[4],
            'difference_budget': row[5]
        }
        data.append(report)
    return JsonResponse(data, safe=False)

#JSON DATA
def JsonData(request):
    result = Report.objects.all()
    data = []
    for row in result:
        report = {
            'date' : row.date,
            'restaurant' : row.restaurant,
            'planned_hours': row.planned_hours,
            'actual_hours': row.actual_hours,
            'budget': row.budget,
            'sells': row.sells
        }
        data.append(report)
    return JsonResponse(data, safe=False)

#SEARCH REPORT
def filtered_report(request):
    restaurant = request.GET.get('restaurant')
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    queryset=None

    if (restaurant):
        queryset = Report.objects.filter(restaurant=restaurant).values('restaurant').annotate(
            total_planned_hours=Sum('planned_hours'),
            total_actual_hours=Sum('actual_hours'),
            total_budget=Sum('budget'),
            total_sells=Sum('sells'),
            difference_hours=Sum('planned_hours') - Sum('actual_hours'),
            difference_budget=Sum('budget') - Sum('sells')
            )

    if (start_date and end_date):
        queryset = Report.objects.filter(date__range=[start_date, end_date]).values('restaurant').annotate(
            total_planned_hours=Sum('planned_hours'),
            total_actual_hours=Sum('actual_hours'),
            total_budget=Sum('budget'),
            total_sells=Sum('sells'),
            difference_hours=Sum('planned_hours') - Sum('actual_hours'),
            difference_budget=Sum('budget') - Sum('sells')
            )

    if (restaurant and start_date and end_date):
        queryset = Report.objects.raw(
            "SELECT id, date, restaurant, SUM(planned_hours) AS total_planned_hours, "
            "SUM(actual_hours) AS total_actual_hours, SUM(budget) AS total_budget, "
            "SUM(sells) AS total_sells, (SUM(planned_hours) - SUM(actual_hours)) AS difference_hours, "
            "(SUM(budget) - SUM(sells)) AS difference_budget FROM report "
            "WHERE restaurant=%s AND date >= %s AND date <= %s",
            [restaurant, start_date, end_date]
            )

    context = {
        "results" : queryset,
        "query" : queryset
        }
    return render(request, 'filteredreport.html', context)















