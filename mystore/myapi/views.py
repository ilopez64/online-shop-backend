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
from rest_framework.response import Response

from .serializers import UserSerializer, DiscountSerializer, ItemSerializer, PurchaseSerializer, PurchasedItemSerializer#, PurchaseHistorySerializer
from .models import User, Discount, Item, Purchase, PurchasedItem
from . import permissions
import itertools

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating users"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)            
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class ItemViewSet(viewsets.ModelViewSet):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,) 
    queryset = Item.objects.all()
    serializer_class = ItemSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'item_type','creator']

    #def get(self, request):
     #   return self.list(request)

class PurchaseViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.PostOwnPurchase,IsAuthenticated)  
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer            

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        qs = self.queryset.filter(user_id=self.request.user)
        return qs

    #def get(self, request):
     #   return self.list(request)

class PurchasedItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.PostOwnPurchase,IsAuthenticated)  
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

#class PurchaseHistoryViewSet(viewsets.ViewSet):
#    authentication_classes = (TokenAuthentication,)
    #permission_classes = (permissions.PostOwnPurchase,IsAuthenticated)  

#    def list(self, request):
#        queryset = list(itertools.chain(Purchase.objects.all(), PurchasedItem.objects.all()))
#        serializer = PurchaseHistorySerializer(queryset, many=True)
#        return Response(serializer.data) 

    #def get_queryset(self):
    #    qs = self.queryset.filter(user_id=self.request.user)
    #    return qs
 
