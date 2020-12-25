"""emlak_kiralama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    #path('em', include('emlak.urls')),
    path('', include('home.urls')),
    # path('home', include('home.urls')), # yukarıda ki satır gibi
    path('admin/', admin.site.urls),
    path('rentalad/',include('emlak.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/',include('user.urls')),

    

    path('category/<int:id>/<slug:slug>', views.category_rentalads, name='category_rentalads'),
    path('rentalad/<int:id>/<slug:slug>', views.rentalad_details, name='rentalad_details'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup_form, name='signup'),
    path('faq/', views.faq, name='faq'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)