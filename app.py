from flask import Flask

""""A aplicação receberá dois parâmetros bucket_name e object_key,
    referente a um arquivo CSV em um bucket do s3, via requisição HTTP."""
# receber requisição dois parâmetros bucket_name e object_key

# acessar o bucket para ler o arquivo


def app_factory():
    app = Flask(__name__)
    add_db(app)
    add_resource(app)

    return app


def add_resource(app):
    from rest.basic_resource import HomeResource

    from flask_restful import Api

    api = Api(app)
    api.add_resource(HomeResource, '/')


def add_db(app):
    from db.database import db
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:mysecretpassword@0.0.0.0:5432/postgres"

    db.init_app(app)

    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app_factory().run(debug=True)
