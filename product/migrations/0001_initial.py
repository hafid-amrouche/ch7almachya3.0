# Generated by Django 4.1.2 on 2023-10-03 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('name_ar', models.CharField(max_length=50, null=True)),
                ('name_fr', models.CharField(max_length=50, null=True)),
                ('name_en', models.CharField(max_length=50, null=True)),
                ('slug', models.SlugField(default='')),
                ('order', models.IntegerField(blank=True, default=0)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='brands_flags/')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('name_ar', models.CharField(max_length=30, null=True)),
                ('name_fr', models.CharField(max_length=30, null=True)),
                ('name_en', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('name_ar', models.CharField(max_length=30, null=True)),
                ('name_fr', models.CharField(max_length=30, null=True)),
                ('name_en', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('name_ar', models.CharField(max_length=30, null=True)),
                ('name_fr', models.CharField(max_length=30, null=True)),
                ('name_en', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GearBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('name_ar', models.CharField(max_length=30, null=True)),
                ('name_fr', models.CharField(max_length=30, null=True)),
                ('name_en', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('name_ar', models.CharField(max_length=30, null=True)),
                ('name_fr', models.CharField(max_length=30, null=True)),
                ('name_en', models.CharField(max_length=30, null=True)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('name_ar', models.CharField(max_length=50, null=True)),
                ('name_fr', models.CharField(max_length=50, null=True)),
                ('name_en', models.CharField(max_length=50, null=True)),
                ('slug', models.SlugField(default='')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='countries_flags/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_category', models.CharField(default='', max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(default='slug')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('engine', models.CharField(default='', max_length=30)),
                ('given_price', models.IntegerField(blank=True, null=True)),
                ('images_list', models.TextField(default='')),
                ('likes_count', models.IntegerField(default=0)),
                ('dislikes_count', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=50)),
                ('used', models.BooleanField(default=True)),
                ('image', models.TextField(default='')),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('exchange', models.BooleanField(default=False)),
                ('year', models.IntegerField(default=1900)),
                ('views', models.IntegerField(default=0)),
                ('is_all_options', models.BooleanField(default=False)),
                ('options_list', models.TextField(default='[]')),
                ('destance', models.IntegerField(default=999999999)),
                ('phone_number', models.TextField(default='')),
                ('city', models.CharField(default='', max_length=30)),
                ('description', models.TextField(default='')),
                ('oxid', models.TextField(default='')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.color')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.document')),
                ('fuel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.fuel')),
                ('gear_box', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.gearbox')),
                ('options', models.ManyToManyField(to='product.option')),
            ],
        ),
    ]