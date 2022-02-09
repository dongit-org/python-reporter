from typing import Any, Dict, Optional, Type

from reporter.base import RESTList, RESTObject
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

        result = self.reporter.http_request(
            verb="post", path=self._path, post_data=attrs
        )

        return self._obj_cls(attrs=result.json())


class GetMixin(object):
    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def get(self, id: str) -> RESTObject:
        """Retrieve a single object.

        Args:
            id: object ID
        """

        path = f"{self._path}/{id}"

        result = self.reporter.http_request(verb="get", path=path)

        return self._obj_cls(attrs=result.json())


class ListMixin(object):
    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def list(
        self,
        filter: Optional[Dict[str, str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> RESTList:
        """Retrieve a list of objects.

        Args:
            filter: query string parameters for HTTP request of the form
                filter[field]
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
        """
        query_data = {}

        if filter is not None:
            for (key, value) in filter.items():
                query_data[f"filter[{key}]"] = value

        if page is not None:
            query_data[f"page[number]"] = str(page)

        if page_size is not None:
            query_data[f"page[size]"] = str(page_size)

        result = self.reporter.http_request(
            verb="get", path=self._path, query_data=query_data
        )

        json = result.json()
        data = [self._obj_cls(attrs=attrs) for attrs in json["data"]]
        links = json["links"]
        meta = json["meta"]

        return RESTList(data=data, links=links, meta=meta)
