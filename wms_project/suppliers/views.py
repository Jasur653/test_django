from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .models import Supplier, Restock
from .forms import SupplierForm, RestockForm


@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        suppliers = suppliers.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(suppliers, 10)  # Show 10 suppliers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'suppliers/supplier_list.html', context)


@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    restocks = Restock.objects.filter(supplier=supplier).order_by('-created_at')

    context = {
        'supplier': supplier,
        'restocks': restocks,
    }

    return render(request, 'suppliers/supplier_detail.html', context)


@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Supplier created successfully.'))
            return redirect('supplier_list')
    else:
        form = SupplierForm()

    context = {
        'form': form,
        'title': _('Create Supplier'),
    }

    return render(request, 'suppliers/supplier_form.html', context)


@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, _('Supplier updated successfully.'))
            return redirect('supplier_detail', pk=supplier.pk)
    else:
        form = SupplierForm(instance=supplier)

    context = {
        'form': form,
        'supplier': supplier,
        'title': _('Update Supplier'),
    }

    return render(request, 'suppliers/supplier_form.html', context)


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier.delete()
        messages.success(request, _('Supplier deleted successfully.'))
        return redirect('supplier_list')

    context = {
        'supplier': supplier,
    }

    return render(request, 'suppliers/supplier_confirm_delete.html', context)


@login_required
def restock_list(request):
    restocks = Restock.objects.all().order_by('-created_at')

    # Filter by status
    status = request.GET.get('status')
    if status:
        restocks = restocks.filter(status=status)

    # Filter by supplier
    supplier_id = request.GET.get('supplier')
    if supplier_id:
        restocks = restocks.filter(supplier_id=supplier_id)

    # Pagination
    paginator = Paginator(restocks, 10)  # Show 10 restocks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    suppliers = Supplier.objects.all()

    context = {
        'page_obj': page_obj,
        'suppliers': suppliers,
        'status': status,
        'supplier_id': supplier_id,
        'status_choices': Restock.STATUS_CHOICES,
    }

    return render(request, 'suppliers/restock_list.html', context)


@login_required
def restock_create(request):
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Restock order created successfully.'))
            return redirect('restock_list')
    else:
        form = RestockForm()

    context = {
        'form': form,
        'title': _('Create Restock Order'),
    }

    return render(request, 'suppliers/restock_form.html', context)


@login_required
def restock_update(request, pk):
    restock = get_object_or_404(Restock, pk=pk)

    if request.method == 'POST':
        form = RestockForm(request.POST, instance=restock)
        if form.is_valid():
            form.save()
            messages.success(request, _('Restock order updated successfully.'))
            return redirect('restock_list')
    else:
        form = RestockForm(instance=restock)

    context = {
        'form': form,
        'restock': restock,
        'title': _('Update Restock Order'),
    }

    return render(request, 'suppliers/restock_form.html', context)


@login_required
def restock_delete(request, pk):
    restock = get_object_or_404(Restock, pk=pk)

    if request.method == 'POST':
        restock.delete()
        messages.success(request, _('Restock order deleted successfully.'))
        return redirect('restock_list')

    context = {
        'restock': restock,
    }

    return render(request, 'suppliers/restock_confirm_delete.html', context)