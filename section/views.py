from django.shortcuts import get_object_or_404, render
from .models import SectionPageGalleryImage
from meta.views import Meta

# Create your views here.
from django.http import Http404

from django.views.generic import View

from meta.views import MetadataMixin


class Details(MetadataMixin, View):

    def get_meta_description(self, context):
        return description

    def get(self, request, image_name):
        image_object = None

        for gallery_item  in SectionPageGalleryImage.objects.all():
            if gallery_item.image.filename == image_name:
                image_object = gallery_item

                title = image_object.image.filename,
                description = image_object.caption


        return render(request, 'section/section_page_gallery_image_detail.html', {'image': image_object})