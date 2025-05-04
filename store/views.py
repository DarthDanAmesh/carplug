from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.utils.html import escape
from django.contrib import messages
from django.utils import timezone

from .models import Car, Review, Manufacturer, Importer
from .utils import average_rating


def home(request):
    """Home page with featured cars and manufacturers"""
    featured_cars = Car.objects.filter(available=True).select_related('manufacturer')[:3]
    manufacturers = Manufacturer.objects.annotate(car_count=Count('car')).order_by('-car_count')[:5]
    
    context = {
        'featured_cars': featured_cars,
        'manufacturers': manufacturers,
    }
    return render(request, 'store_templates/home.html', context)


def car_list(request):
    """Optimized car listing with pagination and filtering"""
    manufacturer_id = request.GET.get('manufacturer')
    fuel_type = request.GET.get('fuel_type')
    sort_by = request.GET.get('sort', 'name')
    available = request.GET.get('available', 'true') == 'true'
    
    # Base queryset with optimized annotation
    cars = Car.objects.select_related('manufacturer').annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    )
    
    # Filter by availability
    cars = cars.filter(available=available)
    
    # Apply filters
    if manufacturer_id:
        cars = cars.filter(manufacturer_id=manufacturer_id)
    
    if fuel_type:
        cars = cars.filter(fuel_type__iexact=fuel_type)
    
    # Apply sorting
    if sort_by == 'price_low':
        cars = cars.order_by('price')
    elif sort_by == 'price_high':
        cars = cars.order_by('-price')
    elif sort_by == 'rating':
        cars = cars.order_by('-avg_rating')
    elif sort_by == 'date':
        cars = cars.order_by('-manufacture_date')
    else:  # Default to name
        cars = cars.order_by('name')
    
    # Pagination
    paginator = Paginator(cars, 9)  # Show 9 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique fuel types for filtering
    fuel_types = Car.objects.values_list('fuel_type', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'manufacturers': Manufacturer.objects.all(),
        'fuel_types': fuel_types,
        'current_manufacturer': manufacturer_id,
        'current_fuel_type': fuel_type,
        'current_sort': sort_by,
        'current_available': available,
    }
    return render(request, 'store_templates/car_list.html', context)


def car_detail(request, pk):
    """Detailed view of a car with reviews and related cars"""
    car = get_object_or_404(Car.objects.select_related('manufacturer'), pk=pk)
    
    # Get reviews with optimized query
    reviews = car.review_set.all().select_related('creator')
    
    # Get related cars by same manufacturer
    related_cars = Car.objects.filter(
        manufacturer=car.manufacturer, 
        available=True
    ).exclude(pk=car.pk).annotate(
        avg_rating=Avg('review__rating')
    )[:3]
    
    # Get importers for this car
    importers = car.carimporter_set.all().select_related('importer')
    
    # Calculate car rating
    car_rating = average_rating([review.rating for review in reviews]) if reviews else None
    
    # Review form for logged-in users
    review_form = None
    if request.user.is_authenticated:
        # You'll need to create a ReviewForm class in forms.py
        pass
    
    context = {
        'car': car,
        'car_rating': car_rating,
        'reviews': reviews,
        'related_cars': related_cars,
        'importers': importers,
        'review_form': review_form,
    }
    return render(request, 'store_templates/car_detail.html', context)


@login_required
def add_review(request, car_id):
    """Add a review to a car"""
    car = get_object_or_404(Car, pk=car_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        
        if content and rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:  # Assuming 5-star rating system
                    # Create review
                    review = Review(
                        content=content,
                        rating=rating,
                        creator=request.user,
                        car=car,
                        date_created=timezone.now()
                    )
                    review.save()
                    messages.success(request, "Your review has been added!")
                else:
                    messages.error(request, "Rating must be between 1 and 5.")
            except ValueError:
                messages.error(request, "Invalid rating value.")
        else:
            messages.error(request, "Both content and rating are required.")
    
    return redirect('car_detail', pk=car_id)


@login_required
def edit_review(request, review_id):
    """Edit an existing review"""
    review = get_object_or_404(Review, pk=review_id)
    
    # Check if user is the creator of the review
    if review.creator != request.user:
        messages.error(request, "You don't have permission to edit this review.")
        return redirect('car_detail', pk=review.car.pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        
        if content and rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    review.content = content
                    review.rating = rating
                    review.date_edited = timezone.now()
                    review.save()
                    messages.success(request, "Your review has been updated!")
                else:
                    messages.error(request, "Rating must be between 1 and 5.")
            except ValueError:
                messages.error(request, "Invalid rating value.")
        else:
            messages.error(request, "Both content and rating are required.")
    
    return redirect('car_detail', pk=review.car.pk)


def search_view(request):
    """Search for cars with pagination and filtering"""
    query = request.GET.get('q', '').strip()
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    manufacturer = request.GET.get('manufacturer')
    fuel_type = request.GET.get('fuel_type')
    available = request.GET.get('available', 'true') == 'true'
    
    # Base query with annotations
    results = Car.objects.filter(available=available).select_related('manufacturer').annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    )
    
    # Apply filters
    if query:
        # Sanitize the input
        sanitized_query = escape(query)
        results = results.filter(
            Q(name__icontains=sanitized_query) | 
            Q(manufacturer__name__icontains=sanitized_query) |
            Q(fuel_type__icontains=sanitized_query)
        )
    
    if price_min:
        try:
            price_min = float(price_min)
            results = results.filter(price__gte=price_min)
        except ValueError:
            pass
    
    if price_max:
        try:
            price_max = float(price_max)
            results = results.filter(price__lte=price_max)
        except ValueError:
            pass
    
    if manufacturer:
        results = results.filter(manufacturer_id=manufacturer)
    
    if fuel_type:
        results = results.filter(fuel_type__iexact=fuel_type)
    
    # Pagination
    paginator = Paginator(results, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique fuel types for filtering
    fuel_types = Car.objects.values_list('fuel_type', flat=True).distinct()
    
    context = {
        'results': page_obj,
        'query': query,
        'manufacturers': Manufacturer.objects.all(),
        'fuel_types': fuel_types,
        'current_manufacturer': manufacturer,
        'current_fuel_type': fuel_type,
        'price_min': price_min,
        'price_max': price_max,
        'current_available': available,
    }
    return render(request, 'store_templates/search_results.html', context)


def manufacturer_view(request, manufacturer_id):
    """View cars by manufacturer"""
    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
    cars = Car.objects.filter(manufacturer=manufacturer).annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    )
    
    # Pagination
    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'manufacturer': manufacturer,
        'page_obj': page_obj,
    }
    return render(request, 'store_templates/manufacturer.html', context)


def carousel_list(request):
    """Featured cars for carousel display"""
    featured_cars = Car.objects.filter(available=True).annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    ).order_by('-manufacture_date')[:3]
    
    context = {
        'carousel_items': featured_cars
    }
    return render(request, 'store_templates/carousel.html', context)


# User account views
@login_required
def user_profile(request):
    """User profile page showing reviews"""
    user_reviews = Review.objects.filter(creator=request.user).select_related('car')
    
    context = {
        'user_reviews': user_reviews,
    }
    return render(request, 'store_templates/profile.html', context)


# Admin views (these would typically be in admin.py but included here for completeness)
@login_required
def admin_car_list(request):
    """Admin view for listing all cars"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
    cars = Car.objects.all().select_related('manufacturer')
    context = {'cars': cars}
    return render(request, 'admin/car_list.html', context)


def shop_view(request):
    """Shop page view"""
    # Similar to car_list but with different template/filtering
    return render(request, 'store_templates/shop.html', context)

def deals_view(request):
    """Special deals page"""
    deals = Car.objects.filter(
        discount_price__isnull=False,
        available=True
    ).select_related('manufacturer').annotate(
        avg_rating=Avg('review__rating')
    )
    return render(request, 'store_templates/deals.html', {'deals': deals})

def about_view(request):
    """About us page"""
    return render(request, 'store_templates/about.html')

def contact_view(request):
    """Contact page"""
    if request.method == 'POST':
        # Process contact form
        pass
    return render(request, 'store_templates/contact.html')

@login_required
def wishlist_view(request):
    """User wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('car')
    return render(request, 'store_templates/wishlist.html', {'wishlist': wishlist_items})

@login_required
def cart_view(request):
    """Shopping cart"""
    cart_items = Cart.objects.filter(user=request.user).select_related('car')
    return render(request, 'store_templates/cart.html', {'cart': cart_items})

@login_required
def user_orders(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store_templates/orders.html', {'orders': orders})

# Policy pages (can be simple TemplateViews if no logic needed)
def faq_view(request):
    return render(request, 'store_templates/faq.html')

def shipping_policy(request):
    return render(request, 'store_templates/shipping_policy.html')

def return_policy(request):
    return render(request, 'store_templates/return_policy.html')

def privacy_policy(request):
    return render(request, 'store_templates/privacy_policy.html')