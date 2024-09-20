import csv
import openpyxl

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Country, Manufacturer, Car, Comment
from .serializers import CountrySerializer, ManufacturerSerializer, CarSerializer, CommentSerializer


def index(request):
    return render(request, 'index.html')


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        file_format = request.query_params.get('format')
        if file_format:
            return self.export_data(request, self.queryset, 'countries', file_format)
        return super().list(request, *args, **kwargs)


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ExportDataMixin:
    def export_data(self, request, queryset, filename, file_format):
        if file_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'  # noqa #isort: ignore
            writer = csv.writer(response)
            for obj in queryset:
                writer.writerow([str(obj)])
            return response
        elif file_format == 'xlsx':
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'  # noqa #isort: ignore
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            for i, obj in enumerate(queryset, start=1):
                sheet[f'A{i}'] = str(obj)
            workbook.save(response)
            return response
        return None


class CountryViewSet(viewsets.ModelViewSet, ExportDataMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request, *args, **kwargs):
        format_type = request.query_params.get('format')
        if format_type in ['csv', 'xlsx']:
            return self.export_data(request, self.get_queryset(), 'countries', format_type)
        return super().list(request, *args, **kwargs)


class ManufacturerViewSet(viewsets.ModelViewSet, ExportDataMixin):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def list(self, request, *args, **kwargs):
        format_type = request.query_params.get('format')
        if format_type in ['csv', 'xlsx']:
            return self.export_data(request, self.get_queryset(), 'manufacturers', format_type)
        return super().list(request, *args, **kwargs)
