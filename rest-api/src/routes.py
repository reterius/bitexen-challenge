from src.resources.stat_resource import StatResource


def routes_config(api):
    api.add_resource(StatResource, "/stats")
