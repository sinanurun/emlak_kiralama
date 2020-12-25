from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from emlak.models import Rentalad, Category, Images, Comment
from home.forms import SignUpForm
from home.models import Setting, ContactForm, ContactMessage, UserProfile, FAQ
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request


def index(request):
    setting = Setting.objects.get(pk=1)
    rentalad_slider = Rentalad.objects.filter(status=True).order_by('-id')[:4]  # last 4 products
    category = Category.objects.filter(status=True).all()

    # products_slider = Product.objects.all().order_by('id')[:4]  #first 4 products

    rentalads_picked = Rentalad.objects.all().order_by('?')[:6]  # Random selected 4 products

    context = {'setting': setting,
               'sliderdata': rentalad_slider,
               'rentalads_picked': rentalads_picked,
               'category': category}
    return render(request, "index.html", context)
    """aşağıdaki kısım direk bir içerik döndürmek için yukarıdaki kısım ise
     bir html view döndürmek için """
    # return HttpResponse("Karşılama Sayfası %s." % text)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category}
    return render(request, "aboutus.html", context)


def contact(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    form = ContactForm
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               'form': form}
    return render(request, 'contact.html', context)


def referances(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category}
    return render(request, "referances.html", context)


def category_rentalads(request, id, slug):
    catdata = Category.objects.get(pk=id)
    rentalads = Rentalad.objects.filter(category_id=id,status=True)  # default language
    category = Category.objects.all()
    context = {'rentalads': rentalads,
               'category': category,
               'catdata': catdata}
    return render(request, 'category_rentalads.html', context)


def rentalad_details(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.filter(status=True).all()
    rentalad = Rentalad.objects.get(pk=id)  # default language
    images = Images.objects.filter(rentalad=id).all()
    comments = Comment.objects.filter(rentalad=id, status=True).all()

    context = {'setting': setting,
               'rentalad': rentalad,
               'comments': comments,
               'images': images,
               'category': category}
    return render(request, 'properties-detail.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category}
    return render(request, 'signin.html', context)


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               'form': form}

    return render(request, 'signup.html', context)

def faq(request):

    faq = FAQ.objects.filter(status="True")
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
        'faq': faq,
    }
    return render(request, 'fag.html', context)

