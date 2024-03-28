# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin

__all__ = [
    "Webhook",
    "WebhookManager",
]


class Webhook(RestObject):
    pass


class WebhookManager(RestManager, CreateMixin, DeleteMixin):
    _path = "webhooks"
    _obj_cls = Webhook
