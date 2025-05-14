from nicegui import events, ui

def handle_draw(e: events.GenericEventArguments):
    layer_type = e.args['layerType']
    coords = e.args['layer'].get('_latlng') or e.args['layer'].get('_latlngs')
    ui.notify(f'Drawn a {layer_type} at {coords}')

draw_control = {
    'draw': {
        'polygon': True,
        'marker': True,
        'circle': True,
        'rectangle': True,
        'polyline': True,
        'circlemarker': True,
    },
    'edit': {
        'edit': True,
        'remove': True,
    },
}
m = ui.leaflet(center=(51.505, -0.09), draw_control=draw_control)
m.classes('h-96')
m.on('draw:created', handle_draw)
m.on('draw:edited', lambda: ui.notify('Edit completed'))
m.on('draw:deleted', lambda: ui.notify('Delete completed'))

ui.run()
