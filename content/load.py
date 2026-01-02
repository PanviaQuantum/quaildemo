import anywidget
import traitlets

from urllib import parse

class LocationWidget(anywidget.AnyWidget):
    _esm = """
    export function render({ model, e1}) {
        model.set("location", String(window.location));
        model.save_changes();
    }
    """
    location = traitlets.Unicode().tag(sync=True)
    
    @property
    def query_params(self):
        return parse.parse_qs(parse.urlsplit(self.location).query)

    location_widget = LocationWidget()
    location_widget
  
