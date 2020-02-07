from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def index(request):
      category_list = Category.objects.order_by('-likes')[:5]
      page_list = Page.objects.order_by('-views')[:5]

      context_dict = {}
      context_dict ['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
      context_dict ['categories'] = category_list
      context_dict ['pages'] = page_list
      return render(request, 'rango/index.html', context=context_dict)
   
def about(request):
       return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
      #create a context dictionary
      context_dict = {}

      try:
          category = Category.objects.get(slug=category_name_slug)
          #The filter() will return a list of page objects or an empty list
          pages = Page.objects.filter(category=category)
          
          #Add results list to the template context under name pages
          context_dict['pages'] = pages
          context_dict['category'] = category
      except Category.DoesNotExist:
          context_dict['pages'] = None
          context_dict['category'] = None
     
      return render(request, 'rango/category.html', context=context_dict)

def show_page(request, page_url):
      context_dict = {}

      