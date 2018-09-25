from django.shortcuts import render, render_to_response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from xceedance.models import Feature
from xceedance.serializers import FeatureSerializer

# Create your views here.

@login_required
def index(request):
    return render_to_response("index.html", {})

class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def get_queryset(self):
        user = self.request.user
        return Feature.objects.filter(reporter=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse(serializer.data)
    