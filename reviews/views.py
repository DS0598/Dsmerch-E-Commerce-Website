from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import is_safe_url


# Create your views here.
from .models import Review
from base.models import Product

@login_required
def create_review_view(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    product_id_ = request.GET.get('product_id')
    product_id_post = request.POST.get('product_id')
    product_id = product_id_ or product_id_post or None
    print(request.POST)
    if request.method == 'POST':
        if product_id:
            user = request.user
            product = Product.objects.get(_id=product_id)
            try:

                if Review.objects.filter(product=product, user=user).count() == 1:
                    messages.warning(request, f"You have already submitted review for this product")
                    if is_safe_url(redirect_path, request.get_host()):
                        return redirect(redirect_path)
                else:
                    review_obj = Review.objects.create(product=product, user=user)
                    review_obj.comments = request.POST.get("comments")
                    review_obj.save()
                    if is_safe_url(redirect_path, request.get_host()):
                        return redirect(redirect_path)
            except:
                messages.error(request, f"Internal server issue")
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)                

    return redirect('/')
            
