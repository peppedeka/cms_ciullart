from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.api import APIField

from section.models import SectionIndexPage;


class HomePage(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True,null=True
    )

    def get_context(self, request):
            # Update context to include only published posts, ordered by reverse-chron
            context = super().get_context(request)
            sectionpages = SectionIndexPage.objects.all();
            context['sections'] = sectionpages
            return context

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('image'),
    ]

    api_fields = [
        APIField('image'),
        APIField('feed_image', serializer=ImageRenditionField('fill-500x500', source='image')),
    ]
