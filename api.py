from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)

class Articles(Resource):
    def get(self):
        data = pd.read_json('articles.json')
        data = data.to_dict()
        return {'data': data["articles"]}, 200 

api.add_resource(Articles, '/articles')

app.run()