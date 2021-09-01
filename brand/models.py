from django.db import models
from utils.genslug import gen_slug
from django.urls import reverse
from category.models import SubCategory,Category

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=50)
    brand_slug = models.SlugField(blank=True)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,null=True,related_name='brands')
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("brand_products", kwargs={"cat_slug":self.sub_category.category.cat_slug,"subcat_slug":self.sub_category.subcat_slug,"brand_slug":self.brand_slug})
    
    def save(self, *args, **kwargs):
        if not self.brand_slug:
            self.brand_slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def products_in_brand(brand_slug):
        brand = Brand.objects.get(brand_slug=brand_slug)
        return brand.products.all()


