from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from planotrabalho.models import PlanoTrabalho
from adesao.models import Municipio, Cidade, Usuario
from api.serializers import MunicipioSerializer, UsuarioSerializer, PlanoTrabalhoSerializer


# MUNICIPIOS
# Lista todos os municipios
class  MunicipioList(generics.ListAPIView):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    queryset = Municipio.objects.filter().order_by('-id')
    serializer_class = MunicipioSerializer
    

# Retorna um municipio especificado pela pk
class MunicipioDetail(generics.RetrieveAPIView):
    queryset = Municipio.objects.filter().order_by('-id') 
    serializer_class = MunicipioSerializer

# PLANO TRABALHO
# Lista todos os planos de trabalho 
class PlanoTrabalhoList(generics.ListAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer 
    

# Retorna um plano de trabalho especificado pela pk
class PlanoTrabalhoDetail(generics.RetrieveAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id') 
    serializer_class = PlanoTrabalhoSerializer 

# USUÁRIOS

# Lista todos os usuários
class UsuarioList(generics.ListAPIView):
    queryset = Usuario.objects.filter().order_by('-id')
    serializer_class = UsuarioSerializer
    
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('nome_usuario','municipio')

# Retorna um usuário especificado pela pk
class UsuarioDetail(generics.RetrieveAPIView):
    queryset = Usuario.objects.filter().order_by('-id') 
    serializer_class = UsuarioSerializer
        

        