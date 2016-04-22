from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.views import csrf_exempt
from rest_framework import generics, viewsets
from .serializers import DropletSerializer, UserSerializer
from .models import Droplet


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()


class DropletList(generics.ListCreateAPIView):
    """
    ViewSet that returns all droplets
    """
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DropletList, self).dispatch(request, *args, **kwargs)

    # permission_classes = ()
    queryset = Droplet.objects.all()
    serializer_class = DropletSerializer


class DropletQuery(generics.ListAPIView):
    """
    Viewset that filters based on given latitude and longitude proximity
    """

    serializer_class = DropletSerializer

    @staticmethod
    def to_float(n):
        try:
            return float(n)
        except ValueError:
            return None

    def get_queryset(self):
        queryset = Droplet.objects.all()
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        latitude = self.to_float(latitude)
        longitude = self.to_float(longitude)

        lower_bound = 0.1
        upper_bound = 0.1

        if latitude is not None and longitude is not None:
            queryset = queryset.filter(latitude__range=(latitude-lower_bound, latitude+upper_bound),
                                       longitude__range=(longitude-lower_bound, longitude+upper_bound))

        return queryset

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DropletQuery, self).dispatch(request, *args, **kwargs)
