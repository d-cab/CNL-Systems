from .index import index_bp

def register_blueprints(app):
    app.register_blueprint(index_bp)