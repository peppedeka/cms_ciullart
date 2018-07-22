from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from section.models import SectionIndexPage;


class HomePage(Page):
    description = RichTextField(blank=True)

    def get_context(self, request):
            # Update context to include only published posts, ordered by reverse-chron
            context = super().get_context(request)
            sectionpages = SectionIndexPage.objects.all();
            context['sections'] = sectionpages
            return context

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
    ]

