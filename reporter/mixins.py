from typing import Any, Dict, List, Optional, Type

from reporter.base import RESTList, RESTObject
from reporter.client import Reporter


__all__ = [
    "CreateMixin",
    "GetMixin",
    "ListMixin",
    "SearchMixin",
]


class CreateMixin(object):
    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def create(
        self,
        attrs: Dict[str, Any],
        file: Optional[Any] = None,
    ) -> RESTObject:
        """Create an object of type self._obj_cls.

        Args:
            attrs: Attributes for the created object
            file: The file to upload when creating the object
        """

        files = {"file": file} if file is not None else None

        result = self.reporter.http_request(
            verb="post",
            path=self._path,
            post_data=attrs,
            files=files,
        )

        return self._obj_cls(attrs=result.json())


class GetMixin(object):
    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def get(
        self,
        id: str,
        includes: List[str] = [],
    ) -> RESTObject:
        """Retrieve a single object.

        Expects a JSON response from the server.

        Args:
            id: object ID
        """

        query_data = {}

        if includes:
            query_data["include"] = ",".join(includes)
        path = f"{self._path}/{id}"

        result = self.reporter.http_request(
            verb="get",
            path=path,
            query_data=query_data,
        )

        return self._obj_cls(attrs=result.json())


class GetRawMixin(object):
    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def get(self, id: str) -> bytes:
        """Retrieve a single object.

        Returns the raw response data.

        Args:
            id: Object ID
        """

        path = f"{self._path}/{id}"

        result = self.reporter.http_request(
            verb="get",
            path=path,
            headers={"Accept": "*/*"},
        )

        return result.content


class _ListMixin(object):
    """Parent class for ListMixin and SearchMixin"""

    _path: str
    _obj_cls: Type[RESTObject]
    reporter: Reporter

    def _get_list(
        self,
        extra_path: str = "",
        filter: Dict[str, str] = {},
        sorts: List[str] = [],
        includes: List[str] = [],
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs: Any,
    ) -> RESTList:
        """Retrieve a list of objects.

        Args:
            extra_path: Extra text to add to the request URL path
            filter: query string parameters for HTTP request of the form
                filter[field]
            sorts: How to sort retrieved items
            includes: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            kwargs: Extra options to send to the server
        """
        path = self._path + extra_path

        query_data = kwargs

        for (key, value) in filter.items():
            query_data[f"filter[{key}]"] = value

        if includes:
            query_data["include"] = ",".join(includes)

        if sorts is not None:
            query_data["sort"] = ",".join(sorts)

        if page is not None:
            query_data[f"page[number]"] = str(page)

        if page_size is not None:
            query_data[f"page[size]"] = str(page_size)

        result = self.reporter.http_request(
            verb="get", path=path, query_data=query_data
        )

        json = result.json()
        data = [self._obj_cls(attrs=attrs) for attrs in json["data"]]
        links = json["links"]
        meta = json["meta"]

        return RESTList(data=data, links=links, meta=meta)


class ListMixin(_ListMixin):
    def list(
        self,
        filter: Dict[str, str] = {},
        sorts: List[str] = [],
        includes: List[str] = [],
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> RESTList:
        """Retrieve a list of objects.

        Args:
            filter: query string parameters for HTTP request of the form
                filter[field]
            sorts: How to sort retrieved items
            includes: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
        """
        return self._get_list(
            extra_path="",
            filter=filter,
            sorts=sorts,
            includes=includes,
            page=page,
            page_size=page_size,
        )


class SearchMixin(_ListMixin):
    def search(
        self,
        term: Optional[str] = None,
        filter: Dict[str, str] = {},
        sorts: List[str] = [],
        includes: List[str] = [],
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> RESTList:
        """Search for a list of objects.

        Args:
            term: Term to search for
            filter: query string parameters for HTTP request of the form
                filter[field]
            sorts: How to sort retrieved items
            includes: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
        """

        return self._get_list(
            extra_path="/search",
            filter=filter,
            sorts=sorts,
            includes=includes,
            page=page,
            page_size=page_size,
            term=term,
        )
