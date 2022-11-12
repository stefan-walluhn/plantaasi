class Plant:
    def __init__(self, *waterings):
        self.waterings = waterings

    def run(self):
        for watering in self.waterings:
            watering.run()
