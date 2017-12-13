from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sucesso-cadastro-usuario/$',
        views.sucesso_usuario,
        name='sucesso_usuario'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'index.html'}, name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'template_name': 'index.html'}, name='logout'),
    url(r'^ativar/usuario/(?P<codigo>[\w]+)/$',
        views.ativar_usuario, name='ativar_usuario'),


    url(r'^home/', views.home, name='home'),
    url(r'^usuario/$', views.CadastrarUsuario.as_view(), name='usuario'),
    url(r'^faleconosco/$', views.fale_conosco, name='faleconosco'),

    # Cadastro e alteração de ente federado 
    url(r'^municipio/selecionar$', views.selecionar_tipo_ente,
        name='selecionar_tipo_ente'),
    url(r'^municipio/$', login_required(views.CadastrarMunicipio.as_view()),
        name='municipio'),
    url(r'^sucesso-cadastro-prefeitura/$',
        views.sucesso_municipio,
        name='sucesso_municipio'),
    url(r'^municipio/cadastrar/0/$',
        login_required(views.CadastrarMunicipio.as_view()),
        name='cadastrar_municipio'),
    url(r'^municipio/cadastrar/1/$',
        login_required(views.CadastrarEstado.as_view()),
        name='cadastrar_estado'),
    url(r'^municipio/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarMunicipio.as_view()),
        name='alterar_municipio'),

    # Cadastro e alteração de responsável
    url(r'^responsavel/$', login_required(views.CadastrarResponsavel.as_view()),
        name='responsavel'),
    url(r'^sucesso-cadastro-responsavel/$',
        views.sucesso_responsavel,
        name='sucesso_responsavel'),
    url(r'^responsavel/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarResponsavel.as_view()),
        name='alterar_responsavel'),
    url(r'^importar/secretario/$',
        views.importar_secretario,
        name='importar_secretario'),

    # Cadastro e alteração de secretário
    url(r'^secretario/$', login_required(views.CadastrarSecretario.as_view()),
        name='secretario'),
    url(r'^sucesso-cadastro-secretario/$',
        views.sucesso_secretario,
        name='sucesso_secretario'),
    url(r'^secretario/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarSecretario.as_view()),
        name='alterar_secretario'),

    # Cadastro e alteração de cadastrador
    url(r'^alterar/cadastrador/$',
        login_required(views.OficioAlteracao.as_view()),
        name='alterar_cadastrador'),

    # Minuta de acordo e termo de solicitação
    url(r'^termo/minuta/$',
        login_required(views.MinutaAcordo.as_view()),
        name='minuta'),
    url(r'^termo/solicitacao/$',
        login_required(views.TermoSolicitacao.as_view()),
        name='solicitacao'),
    url(r'^oficio/alteracao/$',
        login_required(views.OficioAlteracao.as_view()),
        name='alteracao'),

    # Consulta
    url(r'^consultar/$', views.ConsultarMunicipios.as_view(), name='consultar'),
    url(r'^consultar/estados/$', views.ConsultarEstados.as_view(), name='consultar_estados'),
    url(r'^detalhar/(?P<pk>[0-9]+)$', views.Detalhar.as_view(), name='detalhar'),
    ]
