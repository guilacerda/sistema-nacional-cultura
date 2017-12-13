from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.forms import ModelForm
from django.template.defaultfilters import filesizeformat

from .models import Usuario, Municipio, Responsavel, Secretario
from .utils import validar_cpf, validar_cnpj, limpar_mascara
import re

content_types = [
    'image/png',
    'image/jpg',
    'image/jpeg',
    'application/pdf',
    'application/msword',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.openxmlformats-officedocument.' +
    'wordprocessingml.document',
    'application/x-rar-compressed',
    'application/zip',
    'application/octet-stream',
    'text/plain']


class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        file = super(RestrictedFileField, self).clean(data, initial)

        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        'O arquivo deve ter menos de %s. Tamanho atual %s'
                        % (filesizeformat(self.max_upload_size),
                            filesizeformat(file._size)))
            else:
                raise forms.ValidationError(
                    'Arquivos desse tipo não são aceitos.')
        except AttributeError:
            pass

        return data


class CadastrarUsuarioForm(UserCreationForm):
    username = forms.CharField(max_length=14, required=True)
    confirmar_email = forms.EmailField(required=True)
    email = forms.EmailField(required=True)
    nome_usuario = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_confirmar_email(self):
        if self.data.get('email') != self.cleaned_data['confirmar_email']:
            raise forms.ValidationError(
                'Confirmação de e-mail não confere.')

        return self.cleaned_data['confirmar_email']

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('Este e-mail já foi cadastrado!')
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def clean_username(self):
        if not validar_cpf(self.cleaned_data['username']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        try:
            User.objects.get(username=''.join(re.findall(
                '\d+',
                self.cleaned_data['username'])))
            raise forms.ValidationError('Esse CPF já foi cadastrado.')
        except User.DoesNotExist:
            return self.cleaned_data['username']

        return self.cleaned_data['username']

    def save(self, commit=True):
        user = super(CadastrarUsuarioForm, self).save(commit=False)
        user.username = limpar_mascara(self.cleaned_data['username'])
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()

        usuario = Usuario()
        usuario.user = user
        usuario.nome_usuario = self.cleaned_data['nome_usuario']
        codigo_ativacao = get_random_string()
        usuario.codigo_ativacao = codigo_ativacao
        if commit:
            usuario.save()

        return user


class CadastrarAdesaoForm(ModelForm):
    termo_posse_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=5242880)
    rg_copia_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=5242880)
    cpf_copia_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=5242880)


    def clean_cpf_prefeito(self):
        if not validar_cpf(self.cleaned_data['cpf_prefeito']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_prefeito']

    def clean_cnpj_prefeitura(self):
        if not validar_cnpj(self.cleaned_data['cnpj_prefeitura']):
            raise forms.ValidationError('Por favor, digite um CNPJ válido!')

        return self.cleaned_data['cnpj_prefeitura']

    class Meta:
        model = Municipio
        fields = '__all__'

class CadastrarEstadoForm(CadastrarAdesaoForm):

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(CadastrarEstadoForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(CadastrarAdesaoForm, self).clean()

        if 'estado' in self.changed_data or 'cidade' in self.changed_data:
            if self.usuario.estado_processo == '6':
                self.add_error('estado', '''Não é possivel modificar o município ou estado após a
                 publicação do plano de trabalho no DOU. Em caso de dúvida entre em contato através do Fale Conosco.''')
            if not self.cleaned_data.get("cidade"):
                estado_validacao = Municipio.objects.filter(
                    estado__sigla=self.cleaned_data['estado'],
                    cidade__isnull=True)
                if estado_validacao:
                    self.add_error('estado', 'Este estado já foi cadastrado!')

    class Meta:
        model = Municipio
        fields = '__all__'

class CadastrarMunicipioForm(CadastrarAdesaoForm):

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(CadastrarMunicipioForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(CadastrarAdesaoForm, self).clean()

        if 'estado' in self.changed_data and 'cidade' in self.changed_data:
            if self.usuario.estado_processo == '6':
                self.add_error('estado', '''Não é possivel modificar o município ou estado após a
                 publicação do plano de trabalho no DOU. Em caso de dúvida entre em contato através do Fale Conosco.''')

            municipio_validacao = Municipio.objects.filter(
                cidade__nome_municipio=self.cleaned_data['cidade'])
            if municipio_validacao:
                self.add_error('estado', 'Este município já foi cadastrado!')

    class Meta:
        model = Municipio
        fields = '__all__'


class CadastrarSecretarioForm(ModelForm):
    def clean_cpf_secretario(self):
        if not validar_cpf(self.cleaned_data['cpf_secretario']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_secretario']

    class Meta:
        model = Secretario
        fields = '__all__'


class CadastrarResponsavelForm(ModelForm):
    def clean_cpf_responsavel(self):
        if not validar_cpf(self.cleaned_data['cpf_responsavel']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_responsavel']

    class Meta:
        model = Responsavel
        fields = '__all__'
