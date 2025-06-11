from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductForm, CategoryForm


@login_required
def product_list(request):
    products = Product.objects.all().order_by('name')

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }

    return render(request, 'products/product_list.html', context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Product created successfully.'))
            return redirect('product_list')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': _('Create Product'),
    }

    return render(request, 'products/product_form.html', context)


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, _('Product updated successfully.'))
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'title': _('Update Product'),
    }

    return render(request, 'products/product_form.html', context)


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, _('Product deleted successfully.'))
        return redirect('product_list')

    context = {
        'product': product,
    }

    return render(request, 'products/product_confirm_delete.html', context)


@login_required
def category_list(request):
    categories = Category.objects.all().order_by('name')

    context = {
        'categories': categories,
    }

    return render(request, 'products/category_list.html', context)


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Category created successfully.'))
            return redirect('category_list')
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'title': _('Create Category'),
    }

    return render(request, 'products/category_form.html', context)


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _('Category updated successfully.'))
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
        'title': _('Update Category'),
    }

    return render(request, 'products/category_form.html', context)


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, _('Category deleted successfully.'))
        return redirect('category_list')

    context = {
        'category': category,
    }

    return render(request, 'products/category_confirm_delete.html', context)