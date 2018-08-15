from django.shortcuts import get_object_or_404, render
from .models import SectionPageGalleryImage

# Create your views here.
from django.http import Http404

def details(request, image_name):
    image_object = None

    for gallery_item  in SectionPageGalleryImage.objects.all():
        if gallery_item.image.filename == image_name:
            image_object = gallery_item

    return render(request, 'section/section_page_gallery_image_detail.html', {'image': image_object})