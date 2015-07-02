# coding: utf-8


def register_base(app):
    from .models import db
    from .models.auth import bind_oauth
    from .libs import cache
    from .libs.pigeon import mailer

    db.init_app(app)
    bind_oauth(app)
    cache.init_app(app)
    mailer.init_app(app)


def register_base_blueprints(app):
    from .handlers import session, oauth

    from .api import init_app
    init_app(app)

    app.register_blueprint(oauth.bp, url_prefix='/oauth')
    app.register_blueprint(session.bp, url_prefix='/session')


def register_app_blueprints(app):
    from .handlers import front, feeds

    app.register_blueprint(feeds.bp, url_prefix='')
    app.register_blueprint(front.bp, url_prefix='')


def create_app(config=None):
    from .app import create_app
    app = create_app(config)
    register_base(app)
    register_base_blueprints(app)
    register_app_blueprints(app)
    return app
