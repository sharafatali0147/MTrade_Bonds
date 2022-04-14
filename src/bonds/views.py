from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Bonds, StatusEnum
from .serializers import BondsSerializer, BondsUSDSerializer, create_bond
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BondsViewSet():

    @swagger_auto_schema(methods=['GET'], responses={200: BondsSerializer(many=True)})
    @api_view(['GET'])
    def bonds_list(request):
        
        bonds = Bonds.objects.all()
        serialzer = BondsSerializer(bonds, many=True)

        return JsonResponse({'Bonds': serialzer.data})
    
    
    usd_param = openapi.Parameter('usd', openapi.IN_QUERY, description="Show in USD", type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(method='get', manual_parameters=[usd_param], responses={200: BondsSerializer(many=True)})
    @api_view(['GET'])
    def get_published(request):
        show_in_usd = request.GET['usd'] == 'true'
        bonds = Bonds.objects.all().filter(status=StatusEnum.published)
        print(show_in_usd)
        print(type(show_in_usd))
        if show_in_usd:
            serialzer = BondsUSDSerializer(bonds, many=True)
        else:
            serialzer = BondsSerializer(bonds, many=True)

        return JsonResponse({'Bonds': serialzer.data})


    @swagger_auto_schema(methods=['post'], request_body=create_bond, responses={200: BondsSerializer})
    @api_view(['POST'])
    def bonds_create(request):
        data = request.data
        data['user_id'] =  request.user.id
        serialzer = BondsSerializer(data=data)
        if serialzer.is_valid(raise_exception=True):
            serialzer.save()
        else:
            return Response(status=401)    
        
        return Response(serialzer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(method='POST', responses={200: BondsSerializer})
    @api_view(['POST'])
    def bonds_purchase(request, id):
        try:
            bond = Bonds.objects.get(pk=id)
            update = BondsSerializer(bond).data
            if update['status'] == StatusEnum.sold:
                return Response(f"This bond: {id} is already sold!", status=status.HTTP_303_SEE_OTHER)
            update['status'] = StatusEnum.sold
            update['buyer_id'] = request.user.id
            
        except Bonds.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialzer = BondsSerializer(bond, data=update)
    
        if serialzer.is_valid(raise_exception=True):
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
