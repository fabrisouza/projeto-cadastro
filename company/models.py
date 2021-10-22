from django.db import models
from register.models import Client
from .validators import validate_CNPJ, valida_cnpj
from django.db.models.fields.related import ManyToManyField
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    useres = models.ManyToManyField(Client)
    cnpj = models.CharField("CNPJ", max_length=18, validators=[validate_CNPJ, valida_cnpj], blank=True, null=True)
    address = models.CharField(max_length=90, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    

#    def get_companys(self):
#        return ",".join([str(p) for p in self.useres.all()])
#
#    def __unicode__(self):
#        return "{0}".format(self.useres)

    def __str__(self):
        return self.cnpj
