from Tool import Tool


class Scanner(Tool):
    def __init__(self, name, *args, **kwargs):
        Tool.__init__(self, name, *args, **kwargs)

    def send_data_via_http(self, data):
        pass
