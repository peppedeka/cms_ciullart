from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.api import APIField
from wagtail.core import blocks

from section.models import SectionIndexPage;


class HomePage(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True,null=True
    )



    related_link = StreamField([
        ('rel_page', blocks.PageChooserBlock('section.SectionIndexPage'))
    ], blank=True)

    def get_context(self, request):
            # Update context to include only published posts, ordered by reverse-chron
            context = super().get_context(request)
            sectionpages = SectionIndexPage.objects.all();
            context['sections'] = sectionpages
            return context

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        StreamFieldPanel('related_link'),
        ImageChooserPanel('image'),
    ]

    api_fields = [
        APIField('image'),
        APIField('feed_image', serializer=ImageRenditionField('fill-500x500', source='image')),
    ]
