class EuropeanSocket:
    def plug_in(self):
        return "220V from European Socket"

class USPlug:
    def connect(self):
        return "110V from US Plug"

class PlugAdapter:
    def __init__(self, us_plug):
        self.us_plug = us_plug

    def plug_in(self):
        return self.us_plug.connect()

# Usage
us_plug = USPlug()
adapter = PlugAdapter(us_plug)
print(adapter.plug_in())  # "110V from US Plug"
