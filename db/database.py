from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class CessaoFundo(db.Model):
    id_cessao = db.Column(db.Integer, primary_key=True)
    originador = db.Column(db.String(250), nullable=False)
    # esta em string para manter o formato do dado
    doc_originador = db.Column(db.String(50), nullable=False)
    cedente = db.Column(db.String(250), nullable=False)
    doc_cedente = db.Column(db.BigInteger, nullable=False)
    ccb = db.Column(db.BigInteger, nullable=False)
    id_externo = db.Column(db.Integer, nullable=False)
    cliente = db.Column(db.String(250), nullable=False)
    cpf_cnpj = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(250), nullable=False)
    cep = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(250), nullable=False)
    uf = db.Column(db.String(50), nullable=False)
    # VALOR_DO_EMPRESTIMO DECIMAL(10,2) NOT NULL
    valor_do_emprestimo = db.Column(
        db.Float, nullable=False)
    # VALOR_PARCELA DECIMAL(10,2) NOT NULL
    valor_parcela = db.Column(db.Float, nullable=False)
    total_parcelas = db.Column(db.Integer, nullable=False)
    parcela = db.Column(db.Integer, nullable=False)
    # prestar atençao no formato de data
    data_de_emissao = db.Column(
        db.Date, default=datetime.datetime.now(), nullable=False)
    data_de_vencimento = db.Column(
        db.Date, default=datetime.datetime.now(), nullable=False)
    # PRECO_DE_AQUISICAO DECIMAL(10,2) NOT NULL
    preco_de_aquisicao = db.Column(db.Float, nullable=False)
