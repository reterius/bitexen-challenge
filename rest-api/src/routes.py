from src.resources.stat_resource import StatResource, StatItemResource


def routes_config(api):
    api.add_resource(StatResource, "/stats")
    api.add_resource(StatItemResource, "/stats/<string:_id>")
