from flask_restful import Resource
from flask import request
import boto3
import pandas as pd
import dotenv
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
    dotenv.load_dotenv(dotenv.find_dotenv())
    client_s3 = boto3.client('s3',
                             region_name='sa-east-1',
                             aws_access_key_id=os.getenv(
                                 'aws_access_key_id'),
                             aws_secret_access_key=os.getenv(
                                 'secret_access_key'))
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
        # breakpoint()
        dv = csv.loc[row, 'Data de Emissão'].split('/')
        dv.reverse()
        dv = f'{dv[0]}/{dv[1]}/{dv[2]}'

        de = csv.loc[row, 'Data de Emissão'].split('/')
        de.reverse()
        de = f'{de[0]}/{de[1]}/{de[2]}'

        new_record = CessaoFundo(
            originador=csv.loc[row, 'Originador'],
            doc_originador=csv.loc[row, 'Doc Originador'],
            cedente=csv.loc[row, 'Cedente'],
            doc_cedente=int(csv.loc[row, 'Doc Cedente']),
            ccb=int(csv.loc[row, 'CCB']),
            id_externo=int(csv.loc[row, 'Id']),
            cliente=csv.loc[row, 'Cliente'],
            cpf_cnpj=csv.loc[row, 'CPF/CNPJ'],  # prestar atençao tipo str
            endereco=csv.loc[row, 'Endereço'],
            cep=str(csv.loc[row, 'CEP']),
            cidade=csv.loc[row, 'Cidade'],
            uf=csv.loc[row, 'UF'],
            valor_do_emprestimo=float(
                csv.loc[row, 'Valor do Empréstimo'].replace(',', '.')),
            valor_parcela=float(csv.loc[0, 'Parcela R$'].replace(',', '.')),
            total_parcelas=int(csv.loc[row, 'Total Parcelas']),
            parcela=int(csv.loc[row, 'Parcela #']),
            data_de_emissao=de,
            data_de_vencimento=dv,
            preco_de_aquisicao=float(csv.loc[row, 'Preço de Aquisição']))

        db.session.add(new_record)
        db.session.commit()
