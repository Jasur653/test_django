from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from django.db.models import Sum, F
from .models import Order, OrderItem, Customer
from .forms import OrderForm, OrderItemFormSet, CustomerForm


@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')

    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)

    # Filter by customer
    customer_id = request.GET.get('customer')
    if customer_id:
        orders = orders.filter(customer_id=customer_id)

    # Search by order number
    search_query = request.GET.get('search')
    if search_query:
        orders = orders.filter(order_number__icontains=search_query)

    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    customers = Customer.objects.all()

    context = {
        'page_obj': page_obj,
        'customers': customers,
        'status': status,
        'customer_id': customer_id,
        'search_query': search_query,
        'status_choices': Order.STATUS_CHOICES,
    }

    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    context = {
        'order': order,
    }

    return render(request, 'orders/order_detail.html', context)


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = 0  # Will be calculated from items
            order.save()

            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                formset.save()

                # Calculate total amount
                total = order.items.aggregate(
                    total=Sum(F('price') * F('quantity'))
                )['total'] or 0
                order.total_amount = total
                order.save()

                messages.success(request, _('Order created successfully.'))
                return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    context = {
        'form': form,
        'formset': formset,
        'title': _('Create Order'),
    }

    return render(request, 'orders/order_form.html', context)


@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()

            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                formset.save()

                # Recalculate total amount
                total = order.items.aggregate(
                    total=Sum(F('price') * F('quantity'))
                )['total'] or 0
                order.total_amount = total
                order.save()

                messages.success(request, _('Order updated successfully.'))
                return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    context = {
        'form': form,
        'formset': formset,
        'order': order,
        'title': _('Update Order'),
    }

    return render(request, 'orders/order_form.html', context)


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.delete()
        messages.success(request, _('Order deleted successfully.'))
        return redirect('order_list')

    context = {
        'order': order,
    }

    return render(request, 'orders/order_confirm_delete.html', context)


@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('name')

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(customers, 10)  # Show 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'orders/customer_list.html', context)


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Customer created successfully.'))
            return redirect('customer_list')
    else:
        form = CustomerForm()

    context = {
        'form': form,
        'title': _('Create Customer'),
    }

    return render(request, 'orders/customer_form.html', context)


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, _('Customer updated successfully.'))
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'customer': customer,
        'title': _('Update Customer'),
    }

    return render(request, 'orders/customer_form.html', context)


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, _('Customer deleted successfully.'))
        return redirect('customer_list')

    context = {
        'customer': customer,
    }

    return render(request, 'orders/customer_confirm_delete.html', context)