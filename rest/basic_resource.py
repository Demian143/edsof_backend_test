from flask_restful import Resource
from flask import request, jsonify
import rest.business_rule as br


class HomeResource(Resource):
    def get(self):
        # recevie parameters <bucket_name> and <object_key>
        bucket_name = request.args.get('bucket_name')
        object_key = request.args.get('object_key')

        # connect to bucket, get csv contents, save in a temp.csv file
        br.get_csv(bucket_name, object_key)
        # parse data from temp.csv and save in db
        br.save_in_db()

        return jsonify(message="Csv data stored successfully", status=200)
