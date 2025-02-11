# Generated by Django 5.1.6 on 2025-02-11 15:08

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=courses.models.handle_upload)),
                ('acces', models.CharField(choices=[('any', 'Anyone'), ('email_requirement', 'Email requirement')], default='any', max_length=50)),
                ('status', models.CharField(choices=[('pub', 'Published'), ('soon', 'Coming soon'), ('draft', 'Draft')], default='draft', max_length=10)),
            ],
        ),
    ]
