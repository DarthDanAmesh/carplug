from django.shortcuts import get_object_or_404, render

from .models import Car, Review
from .utils import average_rating


def home(request):
    return render(request, 'base.html')


def car_list(request):
    cars = Car.objects.all()
    all_cars = []
    for car in cars:
        # get total reviews
        reviews = car.review_set.all()
        if reviews:
            car_rating = average_rating([review.rating for \
                                         review in reviews])
            number_of_reviews = len(reviews)
        else:
            car_rating = None
            number_of_reviews = 0
        all_cars.append({'car': car, \
                         'car_rating': car_rating, \
                         'number_of_reviews': number_of_reviews})
        context = {
            'car_list': all_cars}
    return render(request, 'store_templates/car_list.html', context)


'''book detail endpoint'''


def car_detail(request, pk):
    car_det = get_object_or_404(Car, pk=pk)
    car_reviews = []
    # get total reviews
    reviews = car_det.review_set.all()
    # declare the object's values in context
    if reviews:
        car_rating = average_rating([review.rating for \
                                     review in reviews])
        context = {
            'car': car_det,
            'car_rating': car_rating,
            # map to list of reviews
            'car_rev': reviews
        }

    else:
        # if no reviews are present
        context = {
            'car': car_det,
            'car_rating': None,
            'car_rev': None
        }
    return render(request, 'store_templates/car_detail.html', context)
