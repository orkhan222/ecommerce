from django.forms import *
from .models import Order
from django.utils.translation import gettext_lazy as _


class OrderForm(ModelForm):
    class Meta:
        model = Order
        #fields = ['order_id','cart',]
        exclude = ['billing_profile','shipping_address','billing_address','is_active','status','shipping_address_final','billing_address_final','shipping_total','order_id']
        widgets = {
            'order_id': Textarea(attrs={'cols': 8, 'rows': 2}),
            'cart':HiddenInput()
            
        }
        help_texts = {
            'order_id': _('Some useful help text.'),
        }
        error_messages = {
            'order_id': {
                'max_length': _("This writer's name is too long."),
            },
        #exclude = ['is_active',]
        }