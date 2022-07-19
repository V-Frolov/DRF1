from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.views.generic import TemplateView
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from api.serializers import my_name_Serializer, CalculatorSerializer, StoreSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from .models import Store


class Index(TemplateView):
    template_name = "api/index.html"


@api_view(['GET'])
def today(request):
    data = {
        "date": datetime.today().strftime('%d/%m/%Y'),
        "year": datetime.today().year,
        "month": datetime.today().month,
        "day": datetime.today().day
    }
    return Response(data)


@api_view(['GET'])
def hello_world(request):
    return Response({"msg": "Hello, World!"})


@api_view(['POST', 'GET'])
def my_name(request):
    if request.method == 'POST':
        serializer = my_name_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    if request.method == "GET":
        return Response({"name": "name_of_hacker"})


@api_view(['POST', 'GET'])
def calculator(request):
    if request.method == 'GET':
        return Response({
            'action': "*",
            'number1': 7,
            'number2': 8
        })

    if request.method == "POST":
        serializer = CalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        calc = serializer.validated_data

        if calc['action'] == "+":
            var = calc['number1'] + calc['number2']
        elif calc['action'] == '-':
            var = calc['number1'] - calc['number2']
        elif calc['action'] == '*':
            var = calc['number1'] * calc['number2']
        elif calc['action'] == '/':
            var = calc['number1'] / calc['number2']
        return Response({"result": var})
    return Response([])


class ListStore(APIView):
    def get(self, request, format=None):
        store = Store.objects.all()
        serializer = StoreSerializer(store, many=True)
        return Response(serializer.data)


class AddStore(APIView):
    def get(self, request):
        return Response({
            'name': 'Write your name here',
            'description': 'Write description your store',
            'rate': 7
        })

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class StoreDetail(APIView):
    def get_object(self, pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            raise serializers.ValidationError("Object not found")

    def get(self, request, pk):
        store = self.get_object(pk)
        serializer = StoreSerializer(store)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        store = self.get_object(pk)
        serializer = StoreSerializer(store, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
