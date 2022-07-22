"""Mixins for model CRUD operations.

Instances of RESTManager should derive these mixins according to the operations possible
on their corresponding RESTObject in the Reporter API.

"""

# pylint: disable = too-few-public-methods

from collections.abc import Sequence
from typing import Any, Dict, Generic, List, Optional, Type, TYPE_CHECKING, TypeVar

from reporter.base import RESTList, RESTManager, RESTObject
from reporter.client import Reporter


__all__ = [
    "CreateMixin",
    "CRUDMixin",
    "DeleteMixin",
    "GetMixin",
    "ListMixin",
    "SearchMixin",
    "UpdateMixin",
]


O = TypeVar("O", bound=RESTObject)


class CreateMixin(Generic[O]):
    """Manager can create object."""

    _path: str
    _obj_cls: Type[O]
    reporter: Reporter

    def create(
        self,
        attrs: Dict[str, Any],
        file: Optional[Any] = None,
    ) -> O:
        """Create a new object.

        Args:
            attrs: Attributes for the created object.
            file: A file to upload when creating the object, if any.

        Returns:
            The response from the server, serialized into the object type.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        files = {"file": file} if file is not None else None

        result = self.reporter.http_request(
            verb="post",
            path=self._path,
            post_data=attrs,
            files=files,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RESTManager)
        return self._obj_cls(self.reporter, result.json())


class DeleteMixin(Generic[O]):
    """Manager can delete object."""

    _path: str
    _obj_cls: Type[O]
    reporter: Reporter

    def delete(self, id_: str):
        """Delete an object.

        Args:
            id_: The ID of the object to delete.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = f"{self._path}/{id_}"

        self.reporter.http_request(
            verb="delete",
            path=path,
        )


class GetMixin(Generic[O]):
    """Manager can retrieve object."""

    _path: str
    _includes: Dict[str, Type[O | Sequence[O]]] = {}
    _obj_cls: Type[O]
    reporter: Reporter

    def get(
        self,
        id_: str,
        include: Optional[List[str]] = None,
    ) -> O:
        """Retrieve a single object.

        Args:
            id_: The ID of the object to retrieve.

        Returns:
            The response from the server, serialized into the object type.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        query_data = {}

        if include:
            query_data["include"] = ",".join(include)
        path = f"{self._path}/{id_}"

        result = self.reporter.http_request(
            verb="get",
            path=path,
            query_data=query_data,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RESTManager)

        return self._obj_cls(self.reporter, result.json())


class GetRawMixin(Generic[O]):
    """Manager can retrieve raw file contents."""

    _path: str
    _obj_cls: Type[O]
    reporter: Reporter

    def get(self, id_: str) -> bytes:
        """Retrieve a single object.

        Args:
            id_: Object ID

        Returns:
            The raw response data.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        path = f"{self._path}/{id_}"

        result = self.reporter.http_request(
            verb="get",
            path=path,
            headers={"Accept": "*/*"},
        )

        return result.content


class _ListMixin(Generic[O]):
    """Parent class for ListMixin and SearchMixin."""

    _path: str
    _includes: Dict[str, Type[O | Sequence[O]]] = {}
    _obj_cls: Type[O]
    reporter: Reporter

    def _get_list(  # pylint: disable = too-many-arguments, too-many-locals
        self,
        extra_path: str = "",
        filter: Optional[Dict[str, str]] = None,  # pylint: disable = redefined-builtin
        sort: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs: Any,
    ) -> RESTList:
        """Retrieve a list of objects.

        Args:
            extra_path: Extra text to add to the request URL path
            filter: query string parameters for HTTP request of the form
                filter[field]
            sort: How to sort retrieved items
            include: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            kwargs: Extra options to send to the server

        Returns:
            A RESTList of objects.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = self._path + extra_path

        query_data = kwargs

        if filter is None:
            filter = {}
        for (key, value) in filter.items():
            query_data[f"filter[{key}]"] = value

        if include:
            query_data["include"] = ",".join(include)

        if sort is not None and sort != []:
            query_data["sort"] = ",".join(sort)

        if page is not None:
            query_data["page[number]"] = str(page)

        if page_size is not None:
            query_data["page[size]"] = str(page_size)

        result = self.reporter.http_request(
            verb="get", path=path, query_data=query_data
        )

        json = result.json()
        if TYPE_CHECKING:
            assert isinstance(self, RESTManager)
        data = [self._obj_cls(self.reporter, attrs) for attrs in json["data"]]
        links = json["links"]
        meta = json["meta"]

        return RESTList(data=data, links=links, meta=meta)


class ListMixin(_ListMixin):
    """Manager can list objects."""

    def list(  # pylint: disable = too-many-arguments
        self,
        filter: Optional[Dict[str, str]] = None,  # pylint: disable = redefined-builtin
        sort: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> RESTList:
        """Retrieve a list of objects.

        Args:
            filter: query string parameters for HTTP request of the form
                filter[field]
            sort: How to sort retrieved items
            include: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]

        Returns:
            A RESTList of objects.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        return self._get_list(
            extra_path="",
            filter=filter,
            sort=sort,
            include=include,
            page=page,
            page_size=page_size,
        )


class SearchMixin(_ListMixin):
    """Manager can search for objects."""

    def search(  # pylint: disable = too-many-arguments
        self,
        term: Optional[str] = None,
        filter: Optional[Dict[str, str]] = None,  # pylint: disable = redefined-builtin
        sort: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> RESTList:
        """Search for a list of objects.

        Args:
            term: Term to search for
            filter: query string parameters for HTTP request of the form
                filter[field]
            sort: How to sort retrieved items
            include: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]

        Returns:
            A RESTList of objects.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        return self._get_list(
            extra_path="/search",
            filter=filter,
            sort=sort,
            include=include,
            page=page,
            page_size=page_size,
            term=term,
        )


class UpdateMixin(Generic[O]):
    """Manager can update objects."""

    _path: str
    _obj_cls: Type[O]
    reporter: Reporter

    def update(
        self,
        id_: str,
        attrs: Dict[str, Any],
    ) -> O:
        """Update an object of type self._obj_cls.

        Args:
            id_: ID of the object to update
            attrs: Attributes to update

        Returns:
            The response from the server, serialized into the object type.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        path = f"{self._path}/{id_}"

        result = self.reporter.http_request(
            verb="patch",
            path=path,
            post_data=attrs,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RESTManager)
        return self._obj_cls(self.reporter, result.json())


class CRUDMixin(CreateMixin, GetMixin, UpdateMixin, DeleteMixin):
    """Composite class of other mixins."""
