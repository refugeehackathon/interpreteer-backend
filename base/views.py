""" Views for the base application """

from django.shortcuts import render


def home(request):
    """ Default view for the root """
    return render(request, 'index.html')


def offers(request):
    return render(request, 'offers.html')


def requests(request):
    return render(request, 'requests.html')

def matchingOffers(request):
    return render(request, 'matching_offers.html')
