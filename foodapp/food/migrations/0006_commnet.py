# Generated by Django 4.1 on 2024-06-16 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0005_alter_fooddetail_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100, unique=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('food_detail_commet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foof_detail_comment', to='food.fooddetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]
