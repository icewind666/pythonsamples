# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.TextField(verbose_name='Название клиента', max_length=500)),
                ('contact_person', models.CharField(verbose_name='Контактное лицо', max_length=255)),
                ('contact_phone', models.CharField(verbose_name='Контактный телефон', max_length=255)),
                ('contact_email', models.CharField(verbose_name='Контактный email', max_length=255)),
                ('description', models.TextField(verbose_name='Описание клиента', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(verbose_name='Дата создания')),
                ('last_login_date', models.DateTimeField(verbose_name='Последний вход')),
                ('login', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(verbose_name='Администратор?')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='Название статуса', max_length=255)),
                ('description', models.TextField(verbose_name='Описание статуса', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='StatusChangeAction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('change_date', models.DateTimeField(verbose_name='Дата установки статуса')),
                ('comment', models.TextField(max_length=3000)),
                ('client', models.ForeignKey(related_name='+', to='rentv_crm.Client')),
                ('manager', models.ForeignKey(related_name='+', to='rentv_crm.Manager')),
                ('new_status', models.ForeignKey(related_name='+', to='rentv_crm.Status')),
                ('old_status', models.ForeignKey(related_name='+', to='rentv_crm.Status')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='manager',
            field=models.ForeignKey(verbose_name='Курирующий менеджер', to='rentv_crm.Manager'),
        ),
        migrations.AddField(
            model_name='client',
            name='status',
            field=models.ForeignKey(verbose_name='Статус клиента', to='rentv_crm.Status'),
        ),
    ]
