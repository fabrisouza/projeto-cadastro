import re
import json
import sys
import urllib.request

from django.core.validators import EMPTY_VALUES, RegexValidator
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


    
def validate_CNPJ(value):
    
    error_messages = {
        'invalid': _("Número de CNPJ inválido."),
        'digits_only': _("O campo requer apenas números."),
        'max_digits': _("O campo requer exatamente 14 dígitos."),
    }

    if value in EMPTY_VALUES:
        return u''
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        raise ValidationError(error_messages['digits_only'])

    if len(value) != 14:
        raise ValidationError(error_messages['max_digits'])

    elif equalsNumbers(value):
        raise ValidationError(error_messages['invalid'])

    orig_dv = value[-2:]

    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(5, 1, -1)) + list(range(9, 1, -1)))])
    new_1dv = DV_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(list(range(6, 1, -1)) + list(range(9, 1, -1)))])
    new_2dv = DV_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        raise ValidationError(error_messages['invalid'])

def valida_cnpj(cnpj):
    'Recebe um CNPJ e retorna True se formato válido ou False se inválido'

    cnpj = parse_input(cnpj)
    if len(cnpj) != 14 or not cnpj.isnumeric():
        return False

    verificadores = cnpj[-2:]
    lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    'Calcular o primeiro digito verificador'
    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-2]))):
        soma += int(numero) * int(lista_validacao_um[ind])

    soma = soma % 11
    digito_um = 0 if soma < 2 else 11 - soma

    'Calcular o segundo digito verificador'
    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-1]))):
        soma += int(numero) * int(lista_validacao_dois[ind])

    soma = soma % 11
    digito_dois = 0 if soma < 2 else 11 - soma

    return verificadores == str(digito_um) + str(digito_dois)


def parse_input(i):
    'Retira caracteres de separação do CNPJ'

    i = str(i)
    i = i.replace('.', '')
    i = i.replace(',', '')
    i = i.replace('/', '')
    i = i.replace('-', '')
    i = i.replace('\\', '')
    return i


def busca_cnpj(cnpj):
    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent',
         " Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0")]

    with opener.open(url) as fd:
        content = fd.read().decode()

    dic = json.loads(content)

    if dic['status'] == "ERROR":
        print('CNPJ {0} rejeitado pela receita federal\n\n'.format(cnpj))
    else:
        try:
            print('Nome: {0}'.format(dic['nome']))
            print('Nome fantasia: {0}'.format(dic['fantasia']))
            print('CNPJ: {0}   Data de abertura: {1}'.format(dic['cnpj'], dic['abertura']))
            print('Natureza: {0}'.format(dic['natureza_juridica']))
            print('Situação: {0}  Situação especial: {1}  Tipo: {2}'.format(dic['situacao'],
                                                                            dic['situacao_especial'],
                                                                            dic['tipo']))
            print('Motivo Situação especial: {0}'.format(dic['motivo_situacao']))
            print('Data da situação: {0}'.format(dic['data_situacao']))
            print('Atividade principal:')
            print(' '*10 + '{0} - {1}'.format(dic['atividade_principal'][0]['code'],
                                              dic['atividade_principal'][0]['text']))
            print('Atividades secundárias:')
            for elem in dic['atividades_secundarias']:
                print(' '*10 + '{0} - {1}'.format(elem['code'], elem['text']))

            print('Endereço:')
            print(' '*10 + '{0}, {1}'.format(dic['logradouro'],
                                             dic['numero']))
            print(' '*10 + '{0}'.format(dic['complemento']))
            print(' '*10 + '{0}, {1}'.format(dic['municipio'],
                                             dic['uf']))
            print('Telefone: {0}'.format(dic['telefone']))
            print('Email: {0}\n\n'.format(dic['email']))
        except KeyError:
            pass


def usage():
    pass

if  __name__ == '_main_':
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        usage()

    for arg in sys.argv[1:]:
        if not valida_cnpj(arg):
            print('CNPJ "{0}" tem formato inválido'.format(arg))
        else:
            busca_cnpj(parse_input(arg))