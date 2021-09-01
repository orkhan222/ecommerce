from django.db import models
from backend.models import User
from django.db.models.signals import *
from django.dispatch import receiver

# Create your models here.

class BillingProfileManager(models.Manager):
    # userin otp statusunu yoxlayir
    def check_user_otp(self, request):
        user = request.user
        user_otp = request.session.get('user_otp_id') # user_otp_id hansidir?
        qs = self.get_queryset().get(user_id=user_otp)
        if user.is_authenticated and qs.user.is_phone_status is True:
            pass
        else:
            qs.user.is_phone_status = True
            qs.user.save()
        return qs 
# burda qs-i return edir, ne menasi var bunu return etmenin? ve bu manager, userin ona gonderilen 
# sifreni duz daxil edib etmediyini yoxluyur?


class BillingProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True,related_name='billing_user')
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    customer_id = models.CharField(max_length=100,blank=True,null=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.user.username
    
    def get_cards(self):
        return self.card_set.all()

    @property
    def default_card(self):
        default_cards = self.get_queryset().filter(active=True, default=True)
        if default_cards.exist():
            return default_cards.first()
        return None

    def set_inactive_card(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False) # burda update() sonrasi db-ye save() edilmeli deyilmi?
        return cards_qs.filter(active=True).count()


@receiver(post_save, sender=User) # line 46-da create argumentine ehtiyac yoxdu mence, silinmelidi? 
def user_billing_profile_create(sender, instance, *args, **kwargs):
    BillingProfile.objects.get_or_create(user=instance)


class CardManager(models.Manager):
    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)


class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=50, blank=True,null=True)
    card_number  = models.CharField(max_length=16, blank=True,null=True)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    cvv = models.IntegerField()
    is_activate = models.BooleanField(default=True)
    is_default = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = CardManager()