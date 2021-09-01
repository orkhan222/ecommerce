from django.db import models
from billing.models import BillingProfile

# Create your models here.

ADDRESS_TYPE=(
    ('billing', 'Billing Address'),
    ('shipping', 'Shipping Address')
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=30,blank=True,null=True)
    nickname = models.CharField(max_length=30,blank=True,null=True)
    address_type = models.CharField(max_length=30,choices=ADDRESS_TYPE)
    address_line_1 = models.CharField(max_length=50,blank=True,null=True)
    address_line_2 = models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    postal_code = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        else:
            return (self.name) 
    
    def get_shortname_address(self):
        for_name = self.name
        if self.nickname:
            for_name = "{} | {}".format(self.nickname, for_name)
        return "{for_name} {line1} {city}".format(
            for_name = for_name or "",
            line1 = self.address_line_1,
            city = self.city
        )
    
    def get_address(self):
        for_name = self.name
        return "{for_name}\n{line1}\n{line2}\n{city}\n{state}\n{postal_code},\n{country}".format(
            for_name = for_name or "",
            line1 = self.address_line_1,
            line2 = self.address_line_2 or "",
            city = self.city,
            state = self.state,
            postal_code = self.postal_code,
            country = self.country
        )
