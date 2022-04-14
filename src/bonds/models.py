from tkinter.tix import Tree
import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
from src.services.banxico import BanxicoService
from src.users.models import User

class StatusEnum(models.TextChoices):
    published = 'Published', _('Published')
    sold = 'Sold', _('Sold')
    

class Bonds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bond_name = models.CharField(max_length=40, validators=[MinLengthValidator(3)])
    number_of_bonds = models.IntegerField(
        validators=[MaxValueValidator(10000), MinValueValidator(1)]
     )
    selling_price_mxn = models.FloatField(
        validators=[MaxValueValidator(100000000.0000), MinValueValidator(0.0000)]
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
    status = models.CharField(
        max_length=20,
        choices=StatusEnum.choices,
        default=StatusEnum.published,
    )
    buyer_id =  models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='buyer_id')
    
    def selling_price_usd(self):
        return self.selling_price_mxn / BanxicoService().getConversionRate()

    def save(self, *args, **kwargs):
        self.selling_price_mxn = round(self.selling_price_mxn, 4)
        super(Bonds, self).save(*args, **kwargs)

