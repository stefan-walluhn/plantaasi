import urequests as requests


class Trigger:
    def __call__(self):
        raise NotImplementedError('trigger must be callable!')


class PumpTrigger(Trigger):
    def __init__(self, pump, duration):
        self.pump = pump
        self.duration = duration

    def __call__(self):
        self.pump.trigger(self.duration)


class PushoverTrigger(Trigger):
    PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

    def __init__(self, user, token, message="gießen!"):
        _data = {'user': user, 'token': token, 'message': message}

        self.data = '&'.join([f'{k}={v}' for k, v in _data.items()])

    def __call__(self):
        response = requests.post(PushoverTrigger.PUSHOVER_URL, data=self.data)

        response.close()
