# app/__init__.py
# function wraps the creation of a new Flask object, and returns it after it's loaded up with configuration settings
#  using app.config and connected to the DB using db.init_app(app)

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bloglist
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    #app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # it will be deprecated for performance reason
    db.init_app(app)

    @app.route('/bloglists',methods=['POST','GET'])
    def bloglists():
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            if name:
                bloglist = Bloglist(name=name)
                bloglist.save()
                response = jsonify({
                    'id': bloglist.id,
                    'name': bloglist.name,
                    'date_created': bloglist.date_created,
                    'date_modified': bloglist.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            bloglists = Bloglist.get_all()
            results = []

            for bloglist in bloglists:
                obj = {
                    'id': bloglist.id,
                    'name': bloglist.name,
                    'date_created': bloglist.date_created,
                    'date_modified': bloglist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bloglists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bloglist_manipulation(id, **kwargs):
     # retrieve a bloglist using it's ID
        bloglist = Bloglist.query.filter_by(id=id).first()
        if not bloglist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            bloglist.delete()
            return {
            "message": "bloglist {} deleted successfully".format(bloglist.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bloglist.name = name
            bloglist.save()
            response = jsonify({
                'id': bloglist.id,
                'name': bloglist.name,
                'date_created': bloglist.date_created,
                'date_modified': bloglist.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bloglist.id,
                'name': bloglist.name,
                'date_created': bloglist.date_created,
                'date_modified': bloglist.date_modified
            })
            response.status_code = 200
            return response

    return app