# Generated by Django 2.2 on 2021-06-17 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_reads_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='book_reviewed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_reviews', to='dojo_reads_app.Book'),
        ),
    ]
