from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import consolidate_data
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import ConsolidatedObjects,ObjectsFromCao
from .serializers import SerialConsolidatedObject, SerialObjectFromCao
from .filter import ConsolidateFilter

from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from .tables import TableConsolide

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm

@login_required
def index(request):
    queryset = ConsolidateFilter(request.GET, queryset=ObjectsFromCao.objects.all())
    context = {
        "filtreform": queryset,
        "tables_consolide": TableConsolide(queryset.qs)
    }
    return render(request, 'pages/home.html', context)

@login_required
def menu(request):
   
    context = {
        "datas": "consolidated_data",
        "formulaire": "si besoin"
    }
    return render(request, 'pages/menu.html', context)
#for api
class GetObjectConsolidated(ListAPIView):
    queryset = ObjectsFromCao.objects.all()
    serializer_class = SerialObjectFromCao
    permission_classes = [IsAuthenticated]

#interne
class Getinfobrute(ListAPIView):
    queryset = ObjectsFromCao.objects.all()
    serializer_class = SerialObjectFromCao
    permission_classes = [IsAuthenticatedOrReadOnly]

class ConsolidatedDataView(APIView):
    def get(self, request, *args, **kwargs):
        consolidated_df = consolidate_data()
        consolidated_data = consolidated_df.to_dict(orient="records")
        return Response(consolidated_data)