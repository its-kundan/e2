from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Department, Employee
from .forms import EmployeeForm

def home(request):
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    return render(request, 'employees/home.html', {
        'total_employees': total_employees,
        'total_departments': total_departments
    })

def about(request):
    return render(request, 'employees/about.html')

def employee_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        employees = Employee.objects.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query)
        ).select_related('department')
    else:
        employees = Employee.objects.all().select_related('department')
    
    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'employees/employee_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee'
    })

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Edit Employee'
    })

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list')
    
    return render(request, 'employees/employee_confirm_delete.html', {
        'employee': employee
    })