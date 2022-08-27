from msilib.schema import ListView
from django.shortcuts import render
from core.serializers import  BlotterSerializer, UserSerializer
from core.models import User, Blotter
from rest_framework import viewsets

from rest_framework import filters
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend

import math


from rest_framework.response import Response
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """Handle creating,reading and updating profiles """

    serializer_class=UserSerializer
    queryset = User.objects.all()

    filter_backends =(filters.SearchFilter,)
    search_fields=('email', 'username')

class BlotterViewSet(viewsets.ModelViewSet):
    queryset = Blotter.objects.all()
    serializer_class= BlotterSerializer

    search_fields = ('user', 'ticker')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ticker', 'price','volume']

    def create(self, request, *args, **kwargs):
        body = json.loads(request.body)

        # checar se o usuario existe
        user = User.objects.filter(email = body['email'], name=body['name']).first()
        if(user is None):
            try:
                user = User(name=body['name'], email=body['email'])
                user.save()
            except:
                return Response({"erro":"Parametro(s) invalido(s)"}, 400)
        

        try:
            newBlotter = Blotter(user_id=user.id, ticker=body['ticker'], price=body['price'], volume=body['volume'])
            newBlotter.save()
        except:
             return Response({"erro":"Parametro(s) invalido(s)"}, 400)

        return Response("ok",200)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            # check if many is required
            if isinstance(data, list):
                kwargs["many"] = True

        return super(BlotterViewSet, self).get_serializer(*args, **kwargs)
  

# @csrf_exempt
class listBlotters(viewsets.ModelViewSet):
    queryset = Blotter.objects.all()
    serializer_class = BlotterSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('price',)

    # @csrf_exempt
    def filter_params(self, request, queryset):
        allowed_params = ["ticker", "volume", "price", "page","aggregate"]
        filter_by = {}

        for param in request.query_params:
            if(param not in allowed_params):
                return 400, None # parametro passado nao e valido

        for param in allowed_params:
            filter_by[param] = request.query_params.get(param, None)

     
        try:
            if(filter_by['ticker']):
                    queryset = queryset.filter(ticker__contains = filter_by['ticker'])
            if(filter_by['volume']):
                    queryset = queryset.filter(volume = filter_by['volume'])
            if(filter_by['price']):
                    queryset = queryset.filter(price = filter_by['price'])
        except:  # possivel erro de tipo de variavel
            return 400, None


        return 200, queryset
        
    # @csrf_exempt
    def list(self, request):
        data = []
        code = 200

        # return Response({"error":"Only authenticated users"},403)

        blotters = Blotter.objects.values("id",
                                    "user",
                                    "ticker",
                                    "volume",
                                    "price")
        
    
        if(len(request.query_params)):
            code, blotters = self.filter_params(request, blotters)

        if(code!=200):
            return Response({"erro":"Parametro(s) invalido(s)"}, code)


        # paginacao
        total_pages = len(blotters)
        page = int(request.query_params.get("page",1))
        LIMIT = 10
        OFFSET = LIMIT*(page-1) 

        blotters = blotters[OFFSET:OFFSET+LIMIT] # deixando aqui ganha tempo de processamento mas perde-se o numero de paginas

        aggregate = request.query_params.get('aggregate', None)
            
    
        dict_controller = {}
        for blotter in blotters:
            # print(blotter)
            user = User.objects.filter(user_id = blotter['id']).values('id','name', 'email').first()
            if(aggregate is not None):
                # dict_controller = {}
                identifier = blotter['ticker']+user['email'] # identifica um unico agrupamento (ticker, user_email)
                if(identifier not in dict_controller):
                    dict_controller[identifier] = {
                        "ticker": blotter["ticker"],
                        "gmv": blotter['price']*blotter['volume'],
                        "volume": blotter['volume'],
    
                        "user": user["id"],
                        "user_name": user["name"],
                        "user_email": user["email"]
                    }
                else:
                    dict_controller[identifier] = {
                        "ticker": blotter["ticker"],
                        "gmv": dict_controller[identifier]['gmv']+blotter['price']*blotter['volume'],
                        "volume": dict_controller[identifier]['volume']+blotter['volume'],

                        "user": user["id"],
                        "user_name": user["name"],
                        "user_email": user["email"]
                    }
            else:
                data.append({
                    "id": blotter["id"],
                    "ticker": blotter["ticker"],
                    "volume": blotter["volume"],
                    "price": blotter["price"],
                    "user": user["id"],
                    "user_name": user["name"],
                    "user_email": user["email"]
                })


        if(aggregate):
            # print(dict_controller)
            for blot in dict_controller:
                data.append({
           
                    "ticker": dict_controller[blot]["ticker"],
                    "volume": dict_controller[blot]["volume"],
                    "price": math.ceil(dict_controller[blot]["gmv"]/dict_controller[blot]["volume"]),
                    "user": dict_controller[blot]["volume"],
                    "user_name": dict_controller[blot]["user_name"],
                    "user_email": dict_controller[blot]["user_email"]
                })
        # print(data)
 

        res = json.dumps(data) 

        return Response({"data":res, "total_pages":total_pages}, code)
        
   