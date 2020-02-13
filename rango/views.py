from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

def add_category(request):
      form = CategoryForm()
      
      if request.method == 'POST':
           form = CategoryForm(request.POST)

           if form.is_valid():
                    cat = form.save(commit=True)
                    print(cat, cat.slug)
                    return redirect('/rango/')
           else:
                    print(form.errors)
       
      return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
     try:
            category = Category.objects.get(slug=category_name_slug)
     except Category.DoesNotExist:
            category = None
  
     if category is None:
            return redirect('/rango/')

     form = PageForm()

     if request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                    if category:
                           page = form.save(commit=False)
                           page.category = category
                           page.view = 0
                           page.save()
                           return redirect(reverse('rango:show_category', 
                                                                   kwargs={'category_name_slug':category_name_slug}))
      
            else:
                    print(form.errors)
                 

     context_dict = {'form' : form, 'category': category}
     return render(request, 'rango/add_page.html', context=context_dict) 

def register(request):
     #if the registeration was secessful
     registered = False

     if request.method == 'POST':
            user_form = UserForm(request.POST)
            profile_form = UserProfileForm(request.POST)

            if user_form .is_valid() and profile_form.is_valid():
                    #save the user's form data to the database
                    user = user_form.save()
        
                    user.set_password(user.password)
                    user.save()
 
                    #Now sort the UserProfile instance
                    #set commit=False. This delays saving the model
                    profile = profile_form.save(commit=False)
                    profile.user = user
 
                    if 'picture' in request.FILES:
                           profile.picture = request.FILES['picture']
                    profile.save()
                    registered = True
            else:
                     print(user_form.errors, profile_form.errors)

     else:
            #Not a HTTP POST, so we render our form using two ModelForm instance
            #These forms will be blank, reandy for user input
            user_form = UserForm()
            profile_form = UserProfileForm()

     return render(request,
                             'rango/register.html',
                             context = {'user_form' : user_form, 
                                                'profile_form' : profile_form,
                                                'registered': registered})

def user_login(request):
       if request.method == 'POST':
            username = request.POST.get('username')             
            password= request.POST.get('password') 

            #Use Dajngo's machinery to attempt to see if the username/password
            user = authenticate(username=username, password=password)

            # If we have a User Object, the details are correct
            # If none, no user
            if user:
                     # Is the account active. It could have been disabled.
                     if user.is_active:
                           login(request, user)
                           return redirect(reverse('rango:index'))
                     else:      
                           # An inactive accounted was used - no logging in!
                           return HttpResponse("Your Rango account is disabled.")   
            else:
                     # Bad login details were provided. So we cannot log the user in.
                     print(f"Invalid login details: {username}, {password}")
                     return HttpResponse("Invalid login details supplied.")
       # The request is not a HTTP POST, so display the login from
       # This scenario would most likely be a HTTP GET.
       else:
            # No context varible to pass to the template system, hence the blank dictionary object...
            return render(request, 'rango/login.html')

@login_required
def restricted(request):
       return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
       logout(request)
       return redirect(reverse('rango:index'))

      