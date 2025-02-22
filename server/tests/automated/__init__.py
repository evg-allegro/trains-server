import abc
import sys
from functools import partial
from unittest import TestCase

from tests.api_client import APIClient
from config import config

log = config.logger(__file__)


class TestServiceInterface(metaclass=abc.ABCMeta):
    api = abc.abstractproperty()

    @abc.abstractmethod
    def defer(self, func, *args, can_fail=False, **kwargs):
        pass


class TestService(TestCase, TestServiceInterface):
    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    def defer(self, func, *args, can_fail=False, **kwargs):
        self._deferred.append((can_fail, partial(func, *args, **kwargs)))

    def _create_temp_helper(
        self,
        service,
        object_name,
        create_endpoint,
        delete_endpoint,
        create_params,
        *,
        client=None,
        delete_params=None,
    ):
        client = client or self.api
        res, data = client.send(f"{service}.{create_endpoint}", create_params)

        object_id = data["id"]
        self.defer(
            client.send,
            f"{service}.{delete_endpoint}",
            can_fail=True,
            data={object_name: object_id, "force": True, **(delete_params or {})},
        )
        return object_id

    def create_temp(self, service, *, client=None, delete_params=None, **kwargs) -> str:
        return self._create_temp_helper(
            service=service,
            create_endpoint="create",
            delete_endpoint="delete",
            object_name=service.rstrip("s"),
            create_params=kwargs,
            client=client,
            delete_params=delete_params,
        )

    def create_temp_version(self, *, client=None, **kwargs) -> str:
        return self._create_temp_helper(
            service="datasets",
            create_endpoint="create_version",
            delete_endpoint="delete_version",
            object_name="version",
            create_params=kwargs,
            client=client,
        )

    def setUp(self, version="1.7"):
        self._api = APIClient(base_url=f"http://localhost:8008/v{version}")
        self._deferred = []
        header(self.id())

    def tearDown(self):
        log.info("Cleanup...")
        for can_fail, func in reversed(self._deferred):
            try:
                func()
            except Exception as ex:
                if not can_fail:
                    log.exception(ex)
        self._deferred = []


def header(info, title="=" * 20):
    print(title, info, title, file=sys.stderr)
