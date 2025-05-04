from .models import *
def cart_and_wishlist_count(request):
    if request.user.is_authenticated:
        return {
            'cart_count': Cart.objects.filter(user=request.user).count(),
            'wishlist_count': Wishlist.objects.filter(user=request.user).count()
        }
    return {'cart_count': 0, 'wishlist_count': 0}