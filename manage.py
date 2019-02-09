from sfi import app_factory

app = app_factory()

@app.cli.command('routes')
def list_routes():
    routes = app.url_map
    for route in routes:
        print(route)
