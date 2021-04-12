from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .services import UserService
from .models import *
from django.db.models import Sum
from Zolve.settings import MINIMUM_VALUE
from django.db import transaction


class WalletViewSet(GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post"]
    serializers_dict = {
    }

    @transaction.atomic()
    @action(
        methods=["post"], detail=False, authentication_classes=[], permission_classes=[]
    )
    def login(self, request):
        data = request.data
        mobile = data.get('mobile')
        password = data.get('otp')
        user = UserService.get_user(mobile=mobile)
        if not user:
            return Response({
                'status':400, 'message':'User does not exists'
            })
        if user:
            return Response({"token": UserService.access_token(user)})
        return Response({
                'status':400, 'message':'User does not exists'
            })

    @transaction.atomic()
    @action(
        methods=["post"], detail=False, authentication_classes=[], permission_classes=[]
    )
    def signup(self, request):
        data = request.data
        response = UserService.create_signup(data)
        return Response(response)
    

    @transaction.atomic()
    @action(
        methods=["get"], detail=False,)
    def get_balance(self, request):
        
        value_dict = Transaction.objects.select_for_update().filter(wallet=request.user)
        if value_dict:
            balance= value_dict.last().balance
        else:
            balance = Decimal('0.0')
        return Response({'balance': balance})

    @classmethod
    @transaction.atomic()
    @action(
        methods=["post"], detail=False,)
    def withdraw(self, request):
        value= request.data.get('value')
        # cust_id = request.data.get('customer_id')
        cust_data = Transaction.objects.select_for_update().filter(wallet=request.user)
        balance = 0
        if cust_data:
            balance = cust_data.last().balance
        if not isinstance(value, int) and not isinstance(value, Decimal):
            raise ValueError("Value must be a Python int or Decimal")
        if value < 0:
            raise ValueError("You can't withdraw the wallet amount. Insufficient funds.")
        if (balance - value) < MINIMUM_VALUE:
            raise ValueError("You can't withdraw the wallet amount. Minimum value required in wallet.")
        balance -= value
        info = Transaction.objects.create(date=datetime.datetime.now(),
            value=value * Decimal('-1.0'),transaction_type='debit', balance=balance,wallet=request.user)
        return Response({'transaction_id':info.id})

    @classmethod
    @transaction.atomic()
    @action(
        methods=["post"], detail=False,)
    def deposit(self, request):
        value= request.data.get('value')

        cust_data = Transaction.objects.select_for_update().filter(wallet=request.user)
        balance=0
        if cust_data:
            balance = cust_data.last().balance
        
        if not isinstance(value, int) and not isinstance(value, Decimal):
            raise ValueError("Value must be a Python int or Decimal")
        if value <= 0:
            raise ValueError("You can't deposit a negative/zero amount")
        balance += value
        info = Transaction.objects.create(date=datetime.datetime.now(),
            value=value,transaction_type='credit',balance=balance,wallet = request.user)
        return Response({'transaction_id':info.id})
        


    

    



    
    

    
    
