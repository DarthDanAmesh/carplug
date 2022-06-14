from django.shortcuts import get_object_or_404, render

from .models import Car
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
            car_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            car_rating = None
            number_of_reviews = 0
        all_cars.append({'car': car, 'car_rating': car_rating, 'number_of_reviews': number_of_reviews})
    '''Returns the context, eg. empty or full list of cars regardless of else statement being triggered'''
    context = {
        'car_list': all_cars}
    return render(request, 'store_templates/car_lisy.html', context)


'''book detail endpoint'''


def car_detail(request, pk):
    car_det = get_object_or_404(Car, pk=pk)
    # get total reviews
    reviews = car_det.review_set.all()
    # declare the object's values in context
    if reviews:
        car_rating = average_rating([review.rating for review in reviews])
        context = {
            'car': car_det,
            'car_rating': car_rating,
            # map to list of reviews
            'car_rev': reviews
        }
    else:
        context = {
            'car': car_det,
            'car_rating': None,
            'car_rev': None
        }
        # if no reviews are present
    '''Returns the context, eg. empty or full list of cars regardless of else statement being triggered'''

    cont = context
    return render(request, 'store_templates/car_detail.html', cont)


'''
def carousel_list(request):
    for item in reviews:
        if item.available==True:
        
        pos1 = Car.objects.all()[:1]
    pos2 = Car.objects.all()[:2]
    pos3 = Car.objects.all()[:3]
    context = {'slider1': pos1, 'slider2': pos2, 'slider3': pos3}
    return render(request, 'store_templates/car_lis.html', context)
'''
