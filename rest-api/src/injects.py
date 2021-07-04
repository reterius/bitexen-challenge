from flask_injector import request, FlaskInjector
from injector import Binder

from src.utils.config_util import ConfigUtil

"""
from src.helpers.rabbitmq_helper import RabbitmqHelper
from src.helpers.redis_helper import RedisHelper
from src.utils.config_util import ConfigUtil
from src.utils.dict_util import get_value

from src.repositories.address_repository import AddressRepository
"""


def injects_config(app):
    # db_dsn = get_value("DB_DSN", app.config)
    # db_name = get_value("DB_NAME", app.config)

    """
    cache_dsn = get_value("CACHE_DSN", app.config)
    cache_port = get_value("CACHE_PORT", app.config)
    cache_pass = get_value("CACHE_PASS", app.config)
    cache_db = get_value("CACHE_DB", app.config)

    amqp_host_uri = get_value("AMQP_HOST_URI", app.config)
    amqp_port = get_value("AMQP_HOST_PORT", app.config)
    amqp_username = get_value("AMQP_USERNAME", app.config)
    amqp_pass = get_value("AMQP_PASS", app.config)
    amqp_is_dsn_conn = get_value("AMQP_IS_DSN_CONN", app.config)

    rabbitmq_helper = RabbitmqHelper(amqp_host_uri, amqp_port, amqp_username, amqp_pass, amqp_is_dsn_conn)
    redis_helper = RedisHelper(cache_dsn, cache_port, cache_db, cache_pass)

    address_repository = AddressRepository()
    """

    def configure(binder: Binder):
        binder.bind(ConfigUtil, to=app.config, scope=request, )

        """
        binder.bind(RabbitmqHelper, to=rabbitmq_helper, scope=request, )
        binder.bind(RedisHelper, to=redis_helper, scope=request, )

        binder.bind(AddressRepository, to=address_repository, scope=request, )
        """
        pass

    FlaskInjector(app=app, modules=[configure])
