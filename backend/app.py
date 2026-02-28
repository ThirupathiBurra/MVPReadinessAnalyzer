import os
from flask import Flask
from flask_cors import CORS
from db.database import init_db
from api.routes import api_bp
from log_config import setup_logging
from api.routes import api_bp

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    if test_config is None:
        app.config.from_object('config.Config')
    else:
        app.config.from_mapping(test_config)
    
    setup_logging(app)
    
    # Ensure database folder exists if using sqlite file
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if db_path != ':memory:':
            os.makedirs(os.path.dirname(os.path.abspath(db_path)) or '.', exist_ok=True)

    init_db(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
