import logging
import urequests as requests


log = logging.getLogger(__name__)


class Trigger:
    def __call__(self):
        raise NotImplementedError('trigger must be callable!')


class Triggers(Trigger):
    def __init__(self, *triggers):
        self.triggers = triggers

    def __call__(self):
        for trigger in self.triggers:
            trigger()


class PumpTrigger(Trigger):
    def __init__(self, pump, duration):
        self.pump = pump
        self.duration = duration

    def __call__(self):
        log.info("trigger %s for %d seconds", self.pump, self.duration)
        self.pump.trigger(self.duration)


class PushoverTrigger(Trigger):
    PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

    def __init__(self, user, token, message="gießen!"):
        _data = {'user': user, 'token': token, 'message': message}

        self.data = '&'.join(['='.join(i) for i in _data.items()])

    def __call__(self):
        response = requests.post(PushoverTrigger.PUSHOVER_URL, data=self.data)

        response.close()
