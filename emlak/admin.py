# -*- coding: utf-8 -*-

import io

from django.contrib import admin

# Register your models here.
from django.http import FileResponse
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table, SimpleDocTemplate, TableStyle
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

from emlak.models import Category, Rentalad, Images, Location, Comment

def make_published(modeladmin, request, queryset):
    queryset.update(status='True')
make_published.short_description = "Mark selected stories as published"


def some_view(modeladmin,request, queryset):
    data = [
        ['Dedicated Hosting', 'VPS Hosting', 'Sharing Hosting', 'Reseller Hosting'],
        ['€200/Month', '€100/Month', '€20/şğüMonth', '€50/Month'],
        ['Free Domain', 'Free Domain', 'Free Domain', 'Free Domain'],
        ['2GB DDR2', '20GB Disc Space', 'Unlimited Email', 'Unlimited Email']
    ]

    fileName = 'pdfTable.pdf'

    pdf = SimpleDocTemplate(
        fileName,
        pagesize=letter,
    )

    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(style)

    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 2, colors.black),

            ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),

            ('GRID', (0, 1), (-1, -1), 2, colors.black),
        ]
    )
    table.setStyle(ts)

    elems = []
    elems.append(table)

    pdf.build(elems)

    # # Create a file-like buffer to receive PDF data.
    # buffer = io.BytesIO()
    #
    # # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buffer)
    # pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
    # p.setFont("Verdana", 8)
    #
    # # Draw things on the PDF. Here's where the PDF generation happens.
    # # See the ReportLab documentation for the full list of functionality.
    # p.drawString(100, 100, "Hello world.şüğüğüği")
    #
    # data = [['00', '01', '02', '03', '04'],
    #         ['10', '11', '12', '13', '14'],
    #         ['20', '21', '22', '23', '24'],
    #         ['30', '31', '32', '33', '34']]
    # t = Table(data, 5 * [0.4 * inch], 4 * [0.4 * inch])
    # t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
    #                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
    #                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
    #                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
    #                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    #                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
    #                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
    #                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #                        ]))
    #
    # w, h = t.wrapOn(p, 0, 0)
    # t.drawOn(p, 0.75 * inch, 0.5 * inch)
    # # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()
    #
    # # FileResponse sets the Content-Disposition header so that browsers
    # # present the option to save the file.
    # buffer.seek(0)

    return FileResponse(as_attachment=True, filename=pdf)

some_view.short_description = "pdf create"



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent']
    list_filter = ['status', 'parent']

# admin.site.register



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_rentalads_count', 'related_rentalads_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [Category]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Rentalad,
                'category',
                'rentalads_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Rentalad,
                 'category',
                 'rentalads_count',
                 cumulative=False)
        return qs

    def related_rentalads_count(self, instance):
        return instance.rentalads_count
    related_rentalads_count.short_description = 'Related rentalads (for this specific category)'

    def related_rentalads_cumulative_count(self, instance):
        return instance.rentalads_cumulative_count
    related_rentalads_cumulative_count.short_description = 'Related rentalads (in tree)'

admin.site.register(Category, CategoryAdmin2)

class LocationAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_rentalads_count', 'related_rentalads_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [Category]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Location.objects.add_related_count(
                qs,
                Rentalad,
                'location',
                'rentalads_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Location.objects.add_related_count(qs,
                 Rentalad,
                 'location',
                 'rentalads_count',
                 cumulative=False)
        return qs

    def related_rentalads_count(self, instance):
        return instance.rentalads_count
    related_rentalads_count.short_description = 'Related rentalads (for this specific location)'

    def related_rentalads_cumulative_count(self, instance):
        return instance.rentalads_cumulative_count
    related_rentalads_cumulative_count.short_description = 'Related rentalads (in tree)'

admin.site.register(Location, LocationAdmin2)

class RentaladImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('image_tag',)
    extra = 5


class RentaladAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'status', 'category']
    list_filter = ['status', 'category']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RentaladImageInline]
    actions = [make_published, some_view]

admin.site.register(Rentalad, RentaladAdmin)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','rentalad','image_tag']

admin.site.register(Images,ImagesAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','rentalad','rate','id')

admin.site.register(Comment,CommentAdmin)