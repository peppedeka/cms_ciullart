from django.db import models
from django import forms


# Create your models here.
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.api import APIField

@register_snippet
class SectionCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Section categories'

class SectionIndexPage(Page):
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        sectionpages = self.get_children().live().order_by('-first_published_at')
        context['sectionpages'] = sectionpages
        return context

    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', blank=True,null=True
    )

    content_panels = Page.content_panels + [
           ImageChooserPanel('image'),
    ]

    api_fields = [
        APIField('image'),
        APIField('feed_image', serializer=ImageRenditionField('fill-500x500', source='image')),
    ]

class SectionTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        sectionpages = SectionPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['sectionpages'] = sectionpages
        return context

class SectionPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'SectionPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class SectionPage(Page):
    date = models.DateField("Post date")
    description = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=SectionPageTag, blank=True)
    categories = ParentalManyToManyField('section.SectionCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Section information"),
        FieldPanel('description', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class SectionPageGalleryImage(Orderable):
    page = ParentalKey(SectionPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]