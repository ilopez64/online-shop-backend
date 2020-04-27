from rest_framework import serializers
from .models import User, Discount, Item, Purchase, PurchasedItem
from . import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User serializer for our user objects"""
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name',
                'password','date_joined')
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discount
        fields = ('id','start_date','end_date','percent_off')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id','discount','item_type','title','item_length','year_released','creator','genre','price','url')

class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id','user_id','final_price','transaction_date','payment_method')
        extra_kwargs = {'user_id' : {'read_only' : True}}

class PurchasedItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PurchasedItem
        fields = ('item_id','invoice_id')

class PurchaseHistorySerializer(serializers.Serializer):
    id = PurchaseSerializer(many=True)
    item_id = PurchasedItemSerializer(many=True)