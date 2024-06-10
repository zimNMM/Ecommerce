from django.shortcuts import render

# Create your views here.




#index view
def index(request):
    return render(request, 'shop/index.html')
