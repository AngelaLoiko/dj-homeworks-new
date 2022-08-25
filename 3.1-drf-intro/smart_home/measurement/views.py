from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer
from psycopg2 import OperationalError

class CreateSensorView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def create_sensor(self, request, *args, **kwargs):
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            Sensor(sensor_name=sensor_name, description=description).save()
            return Response({'status': 'Датчик успешно добавлен'})
        except OperationalError as e:
            return Response({'status': f'Ошибка {e}'})

class ChangeSensorView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class CreateMeasurementView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def create_measurement(self, request):
        try:
            sensor = request.POST.get('sensor')
            temperature = request.POST.get('temperature')
            MeasurementSerializer(sensor=sensor, temperature=temperature).save()
            return Response({'status': 'Измерение успешно добавлено'})
        except OperationalError as e:
            return Response({'status': f'Ошибка {e}'})

class SensorDetailsView(RetrieveAPIView):
    queryset = Sensor.objects.all().prefetch_related('sensor')
    serializer_class = SensorDetailSerializer