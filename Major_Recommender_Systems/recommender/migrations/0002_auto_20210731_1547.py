# Generated by Django 3.2 on 2021-07-31 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bestcity',
            options={'managed': False, 'verbose_name': '百强城市'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'managed': False, 'verbose_name': '科目'},
        ),
        migrations.AlterModelOptions(
            name='colleges',
            options={'managed': False, 'verbose_name': '大学'},
        ),
        migrations.AlterModelOptions(
            name='firstlevel',
            options={'managed': False, 'verbose_name': '一级学科'},
        ),
        migrations.AlterModelOptions(
            name='majors',
            options={'managed': False, 'verbose_name': '专业'},
        ),
        migrations.AlterModelOptions(
            name='provinces',
            options={'managed': False, 'verbose_name': '省份'},
        ),
        migrations.AlterModelOptions(
            name='rankings',
            options={'managed': False, 'verbose_name': '排名'},
        ),
        migrations.AlterModelOptions(
            name='total2020',
            options={'managed': False, 'verbose_name': '汇总2020'},
        ),
    ]