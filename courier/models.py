import decimal
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from backend.models import User
from django.db import models
from order.models import Order
import uuid
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import m2m_changed,post_save,pre_save
from utils.genslug import gen_slug





STATUS= (
    ('catdirildi','catdirildi'),
    ('yoldadir','yoldadir'),
)



class Courier(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    courier_price= models.DecimalField(max_digits=100,decimal_places=2,default=2.00)
    total = models.DecimalField(max_digits=100,decimal_places=2,default=0.00)
    status = models.CharField(blank=True,null=True,max_length=127,choices=STATUS)

    def __str__(self) -> str:
        return str(self.id)

    # def save(self,*args,**kwargs):
    #     if not self.slug:
    #         self.slug=gen_slug(self.user.username)
    #     super().save(*args,**kwargs)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=gen_slug(self.user.username)
        if not self.order:
            self.total = 0
        else:
            self.total = Decimal(self.order.cart.total)  + Decimal(self.courier_price)
        super().save(*args,**kwargs)

    def parse_data_log(self):
        return "ID-si {}, olan kuryer -{} nomreli sifarisi -{} qiymete - {} adrese catdirdi!".format(self.id,self.order.id,self.total,self.order.shipping_address)


# @receiver(post_save, sender=Courier)
# def courier_signal(created, instance, *args,**kwargs):
#     if created is True:
#         instance.total = Decimal(instance.order.cart.total)  + Decimal(instance.courier_price)
#         instance.save()



class LogData(models.Model):
    courier = models.ForeignKey(Courier,on_delete=models.CASCADE,blank=True,null=True)
    log = models.TextField(blank=True,null=True)
    date = DateTimeField(blank=True,null=True,auto_now_add=True)

 
    def __str__(self) -> str:
        return str(self.id)

   
    

@receiver(pre_save, sender=Courier)
def courier_signal( instance, *args,**kwargs):
    if instance.status == 'catdirildi':
        data = instance.parse_data_log()
        create = LogData.objects.create(courier_id=instance.id,log=data)
