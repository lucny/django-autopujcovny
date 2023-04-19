import os, shutil

from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.dispatch import receiver


class Autopujcovna(models.Model):
    def logo_upload_path(self, filename):
        return os.path.join('autopujcovny', str(self.id), filename)

    nazev = models.CharField(max_length=100, verbose_name='Název', help_text='Zadejte název autopůjčovny')
    adresa = models.CharField(max_length=200, verbose_name='Adresa', help_text='Zadejte adresu autopůjčovny')
    telefon = models.CharField(max_length=20, verbose_name='Telefon',
                               help_text='Zadejte telefonní číslo autopůjčovny (včetně předvolby)',
                               validators=[RegexValidator(regex='^(\\+420)? ?[1-9][0-9]{2}( ?[0-9]{3}){2}$',
                                                          message='Zadejte prosím platné telefonní číslo.'
                                                          )])
    email = models.EmailField(max_length=254, verbose_name='E-mail', help_text='Zadejte e-mailovou adresu autopůjčovny',
                              validators=[EmailValidator('Neplatný e-mail.')])
    logo = models.ImageField(upload_to=logo_upload_path, blank=True, null=True, verbose_name='Logo',
                             help_text='Nahrajte logo autopůjčovny')
    informace = models.TextField(blank=True, verbose_name='Informace',
                                 help_text='Zadejte další informace o autopůjčovně')

    class Meta:
        verbose_name = 'Autopůjčovna'
        verbose_name_plural = 'Autopůjčovny'
        ordering = ['nazev']

    def __str__(self):
        return self.nazev

    # přepsání metody delete tak, abychom zajistili smazání všech příloh
    def delete(self, *args, **kwargs):
        # před smazáním záznamu odstraníme i soubor s logem
        if self.logo:
            logo_path = os.path.join('media', 'autopujcovny', str(self.id))
            # metoda shutil.rmtree() zajistí smazání adresáře včetně jeho obsahu
            shutil.rmtree(logo_path)
        # vyvoláme metodu předka, která vymaže celý objekt - záznam o autopůjčovně v databázi
        super().delete(*args, **kwargs)


# Tzv. signál je vyvolán před nebo po určité akci ve spojení s konkrétním modelem
# V tomto případě zajistí, aby hned po uložení nového záznamu o autopůjčovně došlo k přejmenování
# dočasného adresáře None, v němž se nachází soubor loga, podle id čerstvě přidaného záznamu
@receiver(models.signals.post_save, sender=Autopujcovna)
def autopujcovna_post_save(sender, instance, created, **kwargs):
    # vytvoření složky s názvem id nově vytvořeného záznamu
    if created:
        directory_path = os.path.join('media', 'autopujcovny', str(instance.id))
        # přejmenování složky None na složku s id
        old_directory_path = os.path.join('media', 'autopujcovny', 'None')
        if os.path.exists(old_directory_path):
            os.rename(old_directory_path, directory_path)
            # nahrazení řetězce None správným id záznamu v cestě uložené v databázi
            instance.logo.name = instance.logo.name.replace('None', str(instance.id))
            instance.save()