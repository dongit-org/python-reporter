from typing import Any, Dict, List, Optional, Type

from reporter.base import RESTObject
from reporter.client import Reporter


class CreateMixin(object):
    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def create(self, attrs: Dict[str, Any]) -> RESTObject:
        """Create an object of type self._obj_cls.

        Args:
            attrs: Attributes for the created object
        """

        result = self.reporter.http_request(verb="post",
                                            path=self._path,
                                            query_data=attrs)

        return self._obj_cls(attrs=result.json())


class ListMixin(object):
    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def list(self,
             filter: Optional[Dict[str, str]] = None) -> List[RESTObject]:
        """Retrieve a list of objects.

        Args:
            filter: query string parameters for HTTP request of the form
                filter[field]
        """
        if filter is not None:
            query_data = {
                f"filter[{key}]": value
                for (key, value) in filter.items()
            }
        else:
            query_data = {}

        result = self.reporter.http_request(verb="get",
                                            path=self._path,
                                            query_data=query_data)

        return [self._obj_cls(attrs=data) for data in result.json()["data"]]
