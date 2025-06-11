from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from .models import StockMovement
from .forms import StockMovementForm


@login_required
def stock_movement_list(request):
    movements = StockMovement.objects.all().order_by('-created_at')

    # Filter by movement type
    movement_type = request.GET.get('type')
    if movement_type:
        movements = movements.filter(movement_type=movement_type)

    # Filter by product
    product_id = request.GET.get('product')
    if product_id:
        movements = movements.filter(product_id=product_id)

    # Pagination
    paginator = Paginator(movements, 10)  # Show 10 movements per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'movement_type': movement_type,
        'product_id': product_id,
    }

    return render(request, 'inventory/stock_movement_list.html', context)


@login_required
def stock_movement_create(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.staff = request.user
            movement.save()
            messages.success(request, _('Stock movement recorded successfully.'))
            return redirect('stock_movement_list')
    else:
        form = StockMovementForm()

    context = {
        'form': form,
        'title': _('Record Stock Movement'),
    }

    return render(request, 'inventory/stock_movement_form.html', context)


@login_required
def stock_movement_detail(request, pk):
    movement = get_object_or_404(StockMovement, pk=pk)

    context = {
        'movement': movement,
    }

    return render(request, 'inventory/stock_movement_detail.html', context)