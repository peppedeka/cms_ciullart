# Generated by Django 2.0.3 on 2018-08-17 17:00

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_homepage_section_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='related_link',
            field=wagtail.core.fields.StreamField([('rel_page', wagtail.core.blocks.PageChooserBlock('section_page', 'section.SectionIndexPage'))], blank=True),
        ),
    ]