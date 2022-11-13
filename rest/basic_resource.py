from flask_restful import Resource
from flask import request
import boto3
import pandas as pd
import os


class HomeResource(Resource):
    def get(self):
        # receber requisição dois parâmetros bucket_name e object_key
        bucket_name = request.args.get('bucket_name')
        object_key = request.args.get('object_key')

        # connect to bucket, get csv contents, save in a temp file
        get_csv(bucket_name, object_key)
        # parse data from temp.csv and save in db
        save_in_db()


def get_csv(bucket_name, object_key):
    """ Conects to a bucket and get a csv object,
        converts into a new csv and return this new csv"""
    client_s3 = boto3.client('s3',
                             region_name='sa-east-1',
                             aws_access_key_id=os.environ.get(
                                 'aws_access_key_id'),
                             aws_secret_access_key=os.environ().get('secret_access_key'))
    # get csv object
    csv_obj = client_s3.get_object(Bucket=bucket_name, Key=object_key)
    # raw text
    text = csv_obj['Body'].read().decode('ISO-8859-1')

    with open('temp.csv', 'w+') as f:
        # file too long to read directly from the response
        # reading from a local file makes parsing easier
        f.write(text)


def save_in_db():
    from db.database import CessaoFundo, db

    csv = pd.read_csv('temp.csv', delimiter=';')

    for row in range(len(csv)):
        new_record = CessaoFundo(
            originador=csv.loc[row, 'Originador'],
            doc_originador=csv.loc[row, 'Doc Originador'],
            cedente=csv.loc[row, 'Cedente'],
            doc_cedente=csv.loc[row, 'Doc Cedente'],
            ccb=csv.loc[row, 'CCB'],
            id_externo=csv.loc[row, 'Id'],
            cliente=csv.loc[row, 'Cliente'],
            cpf_cnpj=csv.loc[row, 'CPF/CNPJ'],
            endereco=csv.loc[row, 'Endereço'],
            cep=csv.loc[row, 'CEP'],
            cidade=csv.loc[row, 'Cidade'],
            uf=csv.loc[row, 'UF'],
            valor_do_emprestimo=csv.loc[row, 'Valor do Empréstimo'],
            valor_parcela=csv.loc[row, 'Parcela R$'],
            total_parcelas=csv.loc[row, 'Total Parcelas'],
            data_de_emissao=csv.loc[row, 'Data de Emissăo'],
            data_de_vencimento=csv.loc[row, 'Data de Vencimento'],
            preco_de_aquisicao=csv.loc[row, 'Preço de Aquisiçăo'])

        db.session.add(new_record)
        db.commit()
