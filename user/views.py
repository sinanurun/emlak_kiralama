from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from emlak.models import Category, Comment, Rentalad, RentaladForm
from home.models import Setting, UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')  # Check login
def index(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {'category': category,
               'profile': profile}
    return render(request, 'user_profile.html', context)


@login_required(login_url='/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form, 'category': category})


@login_required(login_url='/login')  # Check login
def user_rentalads(request):
    category = Category.objects.all()
    current_user = request.user
    rentalads = Rentalad.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'rentalads': rentalads, }
    return render(request, 'user_rentalads.html', context)


@login_required(login_url='/login')  # Check login
def user_rentalads_add(request):
    if request.method == 'POST':
        form = RentaladForm(request.POST, request.FILES)

        if form.is_valid():
            current_user = request.user
            data = Rentalad()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.detail = form.cleaned_data['detail']
            data.ROOMCOUNT = form.cleaned_data['roomcount']
            data.category = form.cleaned_data['category']
            data.furnished = form.cleaned_data['furnished']
            data.STATUS = 'False'
            data.balcony = form.cleaned_data['balcony']
            data.area = form.cleaned_data['area']
            data.location = form.cleaned_data['location']
            data.price = form.cleaned_data['price']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.slug = form.cleaned_data['slug']
            data.save()
            messages.success(request,"Your Rental Ad ise Added")
            return HttpResponseRedirect('/user/user_rentalads')
        else:
            messages.success(request, "Rental Ad Form Error : " + str(form.errors))
            return HttpResponseRedirect('/user/user_rentalads')


    form = RentaladForm
    category = Category.objects.all()
    current_user = request.user
    rentalads = Rentalad.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'rentalads': rentalads,
               'form': form,
               }
    return render(request, 'user_rentalad_add.html', context)


# @login_required(login_url='/login') # Check login
# def user_orderdetail(request,id):
#     #category = Category.objects.all()
#     current_user = request.user
#     order = Order.objects.get(user_id=current_user.id, id=id)
#     orderitems = OrderProduct.objects.filter(order_id=id)
#     context = {
#         #'category': category,
#         'order': order,
#         'orderitems': orderitems,
#     }
#     return render(request, 'user_order_detail.html', context)
#
# @login_required(login_url='/login') # Check login
# def user_order_product(request):
#     #category = Category.objects.all()
#     current_user = request.user
#     order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
#     context = {#'category': category,
#                'order_product': order_product,
#                }
#     return render(request, 'user_order_products.html', context)

# @login_required(login_url='/login') # Check login
# def user_order_product_detail(request,id,oid):
#     #category = Category.objects.all()
#     current_user = request.user
#     order = Order.objects.get(user_id=current_user.id, id=oid)
#     orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
#     context = {
#         #'category': category,
#         'order': order,
#         'orderitems': orderitems,
#     }
#     return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login')  # Check login
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')  # Check login
def user_delete_rentalad(request, id):
    current_user = request.user
    Rentalad.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Rentalad deleted..')
    return HttpResponseRedirect('/user/user_rentalads')


@login_required(login_url='/login')  # Check login
def user_update_rentalad(request, id):
    rentalad = Rentalad.objects.get(id=id)
    if request.method == 'POST':
        form = RentaladForm(request.POST, request.FILES, instance=rentalad)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Rental Ad ise Updateded")
            return HttpResponseRedirect('/user/user_rentalads')
        else:
            messages.success(request, "Rental Ad Form Error : " + str(form.errors))
            return HttpResponseRedirect('/user/user_rentalads')

    form = RentaladForm(instance=rentalad)
    category = Category.objects.all()
    current_user = request.user
    rentalads = Rentalad.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'rentalads': rentalads,
               'form': form,
               }
    return render(request, 'user_rentalad_update.html', context)


