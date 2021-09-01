from django.db import models
from backend.models import User
from product.models import Product
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from decimal import Decimal

# Create your models here.

class CartMeneger(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None) 
        qs = self.get_queryset().filter(id=cart_id) 
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.object.new(user=request.user)
            new_obj = True
        return cart_obj , new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.object.create(user=user_obj)
    
    


class CartProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1,blank=True,null=True)

    def __str__(self):
        return self.product.product_name



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    products = models.ManyToManyField(CartProduct,related_name='cart_products')
    subtotal = models.DecimalField(max_digits=100,decimal_places=2,default=0.00)
    total = models.DecimalField(max_digits=100,decimal_places=2,default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    object = CartMeneger()

    def __str__(self):
        return str(self.id)

@receiver(m2m_changed, sender=Cart.products.through)
def m2m_changed_cart_reciver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products :
            if x.product.product_discount_price :
                total += x.product.product_discount_price * x.quantity
            else :
                total += x.product.product_price * x.quantity
        if instance.subtotal != total :
            instance.subtotal = total
            # run functions pre_save_cart_receiver
            instance.save()


@receiver(pre_save, sender=Cart)
def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0 :
        instance.total = Decimal(instance.subtotal) * Decimal(settings.SUB_TOTAL_PERCENTAGE)
    else :
        instance.total = 0.00

