from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.parsers import JSONParser
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer, DiscountSerializer, ItemSerializer, PurchaseSerializer, PurchasedItemSerializer
from .models import User, Discount, Item, Purchase, PurchasedItem
from . import permissions

#from rest_framework import APIView
#from rest_framework import generics
#from rest_framework import mixins

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnUser,)

class DiscountViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)            
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    #def get(self, request):
     #   return self.list(request)

class ItemViewSet(viewsets.ModelViewSet):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)            
    filter_backend = (filters.SearchFilter,)
    search_fields = ['title'] 
    queryset = Item.objects.all()
    serializer_class = ItemSerializer  

    #def get(self, request):
     #   return self.list(request)

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer  
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.PostOwnPurchase,IsAuthenticated)            

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_id=self.request.user)

    #def get(self, request):
     #   return self.list(request)

class PurchasedItemViewSet(viewsets.ModelViewSet):
    queryset = PurchasedItem.objects.all()
    serializer_class = PurchasedItemSerializer 
    #def get(self, request):
     #   return self.list(request)     

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token"""
    serializer_class = AuthTokenSerializer

    def create(self,request):
        """Uses the ObtainAuthToken APIView to validate and create a token"""
        return ObtainAuthToken().post(request)

class PurchaseHistoryViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.PostOwnPurchase,IsAuthenticated)   
    def get_queryset(self):
        qs = self.queryset.filter(user_id=self.request.user)
        return qs
 
