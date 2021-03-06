# Generated by Django 2.0.4 on 2018-04-20 01:46

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('description', models.TextField(verbose_name='Description')),
                ('content', ckeditor.fields.RichTextField()),
                ('gdoc_link', models.URLField(null=True, verbose_name='Google Doc Link')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('in_review', 'In-Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft', max_length=15, verbose_name='Status')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
