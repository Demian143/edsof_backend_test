from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)


def app():
    """"A aplicação receberá dois parâmetros bucket_name e object_key,
    referente a um arquivo CSV em um bucket do s3, via requisição HTTP."""
    # receber requisição dois parâmetros bucket_name e object_key
    # acessar o bucket para ler o arquivo
    pass
