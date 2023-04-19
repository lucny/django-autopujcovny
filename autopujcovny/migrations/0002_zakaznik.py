# Generated by Django 4.2 on 2023-04-19 18:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopujcovny', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zakaznik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jmeno', models.CharField(help_text='Zadejte jméno zákazníka', max_length=100, verbose_name='Jméno')),
                ('prijmeni', models.CharField(help_text='Zadejte příjmení zákazníka', max_length=100, verbose_name='Příjmení')),
                ('adresa', models.CharField(help_text='Zadejte adresu autopůjčovny', max_length=200, verbose_name='Adresa')),
                ('telefon', models.CharField(help_text='Zadejte telefonní číslo zákazníka (včetně předvolby)', max_length=20, validators=[django.core.validators.RegexValidator(message='Zadejte prosím platné telefonní číslo.', regex='^(\\+420)? ?[1-9][0-9]{2}( ?[0-9]{3}){2}$')], verbose_name='Telefon')),
                ('email', models.EmailField(help_text='Zadejte e-mailovou adresu zákazníka', max_length=254, validators=[django.core.validators.EmailValidator('Neplatný e-mail.')], verbose_name='E-mail')),
                ('cislo_rp', models.CharField(help_text='Zadejte číslo řidičského průkazu', max_length=20, verbose_name='Řidičský průkaz')),
            ],
            options={
                'verbose_name': 'Zákazník',
                'verbose_name_plural': 'Zákazníci',
                'ordering': ['prijmeni', 'jmeno'],
            },
        ),
    ]