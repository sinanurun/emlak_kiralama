from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Create your models here.


# emlak kategorileri için
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Location(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


# Emlak kiralık ilanlaır için

class Rentalad(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    ROOMCOUNT = (
        ('Stüdyo (1+0)', 'Stüdyo (1+0)'),
        ('1+1', '1+1'),
        ('1,5+1', '1,5+1'),
        ('2+1', '2+1'),
        ('3+1', '3+1'),
        ('3+2', '3+2'),
        ('4+1', '4+1'),
        ('5+1', '5+1'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='None')  # many to one relation with Category
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default='None')  # many to one relation with Category
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    age = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    balcony = models.CharField(max_length=10, choices=STATUS, default='None')
    furnished = models.CharField(max_length=10, choices=STATUS, default='None')
    roomcount = models.CharField(max_length=20, choices=ROOMCOUNT, default='None')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS, default='False')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    ## method to create a fake table field in read only mode
    def image_tag2(self):
        if self.image.url is not None:
            return mark_safe('{}'.format(self.image.url))
        else:
            return ""


class Images(models.Model):
    rentalad = models.ForeignKey(Rentalad, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    ## method to create a fake table field in read only mode
    def image_tag2(self):
        if self.image.url is not None:
            return mark_safe('{}'.format(self.image.url))
        else:
            return ""

    def __str__(self):
        return self.title


class RentaladForm(ModelForm):
    class Meta:
        model = Rentalad

        fields = ['category', 'location', 'title', 'keywords', 'description', 'image', 'price', 'age', 'area',
                  'balcony', 'furnished',
                  'roomcount', 'detail', 'slug']
        widgets = {
            'category': Select(attrs={'class': 'input', 'placeholder': 'Category'}, choices=Category.objects.all()),
            'location': Select(attrs={'class': 'input', 'placeholder': 'Location'}, choices=Location.objects.all()),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'Keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'Image', }),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'Price'}),
            'age': TextInput(attrs={'class': 'input', 'placeholder': 'Age'}),
            'area': TextInput(attrs={'class': 'input', 'placeholder': 'Area'}),
            'balcony': Select(attrs={'class': 'input', 'placeholder': 'Balcony'}, choices=model.STATUS),
            'furnished': Select(attrs={'class': 'input', 'placeholder': 'Furnished'}, choices=model.STATUS),
            'roomcount': Select(attrs={'class': 'input', 'placeholder': 'Roomcount'}, choices=model.ROOMCOUNT),
            'detail': CKEditorUploadingWidget(),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'Price'}),
        }


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    rentalad = models.ForeignKey(Rentalad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']
