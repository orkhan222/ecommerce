from rest_framework import serializers
from product.models import Product, ProductFile
from brand.models import Brand
from category.models import SubCategory, Category


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    class Meta:
        model = SubCategory
        fields = '__all__'

class BrandSerializers(serializers.ModelSerializer):
    sub_category = SubCategorySerializers()
    class Meta:
        model = Brand
        exclude = ['brand_slug',]

class ProductFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductFile
        exclude = ['product',]

class ProductPrice(serializers.Field):
    def to_representation(self, value):
        price_list = {
            "initial amount" : value.product_price,
            "discount amount" : value.product_discount,
            "discounted price" : value.product_discount_price
        }
        return price_list

class ProductSerializers(serializers.ModelSerializer):
    product_price_list = ProductPrice(source="*")
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ['product_price','product_discount','product_discount_price',] 

    def get_category(self,obj):
        return obj.product_brand.sub_category.category.name

class ProductDetailSerializers(serializers.ModelSerializer):
    product_brand = BrandSerializers(read_only=True)
    productfile_set = ProductFileSerializers(many=True)

    class Meta:
        model = Product
        fields = '__all__' 

