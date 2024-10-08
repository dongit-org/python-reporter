"""Mixins for model CRUD operations.

Instances of :class:`~reporter.base.RestManager` should derive these mixins according to the
operations possible on their corresponding :class:`~reporter.base.RestObject` in the Reporter API.

"""

# pylint: disable = too-few-public-methods, redefined-builtin, invalid-name

from typing import (
    Any,
    Callable,
    Generic,
    List,
    Mapping,
    Optional,
    Type,
    TYPE_CHECKING,
    TypeVar,
)

from reporter.base import RestList, RestManager, RestObject
from reporter.client import Reporter


__all__ = [
    "CreateMixin",
    "CrudMixin",
    "DeleteMixin",
    "GetMixin",
    "ListMixin",
    "SearchMixin",
    "UpdateMixin",
]


ChildOfRestObject = TypeVar("ChildOfRestObject", bound=RestObject)


class CreateMixin(Generic[ChildOfRestObject]):
    """Manager can create object."""

    _path: str
    _obj_cast: Callable
    _obj_cls: Type[ChildOfRestObject]
    reporter: Reporter

    def create(
        self,
        attrs: Mapping[str, Any],
        file: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChildOfRestObject:
        """Create a new object.

        Args:
            attrs: Attributes for the created object.
            file: A file to upload when creating the object, if any.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

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
            **kwargs,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RestManager)

        if hasattr(self, "_obj_cast"):
            return self._obj_cast(self.reporter, result.json())
        return self._obj_cls(self.reporter, result.json())


class DeleteMixin(Generic[ChildOfRestObject]):
    """Manager can delete object."""

    _path: str
    _obj_cls: Type[ChildOfRestObject]
    _obj_cast: Callable
    reporter: Reporter

    def delete(
        self,
        id: str,
        **kwargs: Any,
    ) -> None:
        """Delete an object.

        Args:
            id: The ID of the object to delete.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = f"{self._path}/{id}"

        self.reporter.http_request(
            verb="delete",
            path=path,
            **kwargs,
        )


class GetMixin(Generic[ChildOfRestObject]):
    """Manager can retrieve object."""

    _path: str
    _obj_cls: Type[ChildOfRestObject]
    _obj_cast: Callable
    reporter: Reporter

    def get(
        self,
        id: str,
        include: Optional[str | List[str]] = None,
        query_data: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> ChildOfRestObject:
        """Retrieve a single object.

        Args:
            id: The ID of the object to retrieve.
            include: Related data to include in the response.
            query_data: Dict of additional query parameters
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The response from the server, serialized into the object type.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        query_data = dict(query_data) if query_data else {}

        if include:
            query_data["include"] = include

        path = f"{self._path}/{id}"

        result = self.reporter.http_request(
            verb="get",
            path=path,
            query_data=query_data,
            **kwargs,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RestManager)

        if hasattr(self, "_obj_cast"):
            return self._obj_cast(self.reporter, result.json())
        return self._obj_cls(self.reporter, result.json())


class GetRawMixin(Generic[ChildOfRestObject]):
    """Manager can retrieve raw file contents."""

    _path: str
    _obj_cls: Type[ChildOfRestObject]
    _obj_cast: Callable
    reporter: Reporter

    def get(
        self,
        id: str,
        **kwargs: Any,
    ) -> bytes:
        """Retrieve a single object.

        Args:
            id: Object ID
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The raw response data.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        path = f"{self._path}/{id}"

        return self.reporter.get_raw_file(path=path, **kwargs)


class _ListMixin(Generic[ChildOfRestObject]):
    """Parent class for ListMixin and SearchMixin."""

    _path: str
    _obj_cls: Type[ChildOfRestObject]
    _obj_cast: Callable
    reporter: Reporter

    def _get_list(  # pylint: disable = too-many-arguments, too-many-positional-arguments, too-many-locals, redefined-builtin
        self,
        extra_path: str = "",
        term: Optional[str] = None,
        filter: Optional[Mapping[str, str | int | List[str | int]]] = None,
        sort: Optional[str | List[str]] = None,
        include: Optional[str | List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        query_data: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> RestList:
        """Retrieve a list of objects.

        Args:
            extra_path: Extra text to add to the request URL path
            term: A search term.
            filter: query string parameters for HTTP request of the form
                filter[field]
            sort: How to sort retrieved items
            include: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            A :class:`~reporter.base.RestList` of :class:`~reporter.base.RestObject` instances.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = self._path + extra_path

        query_data = dict(query_data) if query_data else {}

        if term is not None:
            query_data["term"] = term

        if filter is None:
            filter = {}
        for key, value in filter.items():
            query_data[f"filter[{key}]"] = value

        if include:
            query_data["include"] = include

        if sort:
            query_data["sort"] = sort

        if page is not None:
            query_data["page[number]"] = str(page)

        if page_size is not None:
            query_data["page[size]"] = str(page_size)

        result = self.reporter.http_request(
            verb="get",
            path=path,
            query_data=query_data,
            **kwargs,
        )

        json = result.json()
        if TYPE_CHECKING:
            assert isinstance(self, RestManager)
        if hasattr(self, "_obj_cast"):
            data = [self._obj_cast(self.reporter, attrs) for attrs in json["data"]]
        else:
            data = [self._obj_cls(self.reporter, attrs) for attrs in json["data"]]
        links = json["links"]
        meta = json["meta"]

        return RestList(data=data, links=links, meta=meta)


class ListMixin(_ListMixin):
    """Manager can list objects."""

    def list(  # pylint: disable = too-many-arguments, too-many-positional-arguments, redefined-builtin
        self,
        filter: Optional[Mapping[str, str | int | List[str | int]]] = None,
        sort: Optional[str | List[str]] = None,
        include: Optional[str | List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        query_data: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> RestList:
        """Retrieve a list of objects.

        Args:
            filter: query string parameters for HTTP request of the form
                filter[field]
            sort: How to sort retrieved items
            include: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            query_data: Dict of additional query parameters
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            A :class:`~reporter.base.RestList` of :class:`~reporter.base.RestObject` instances.

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
            query_data=query_data,
            **kwargs,
        )


class SearchMixin(_ListMixin):
    """Manager can search for objects."""

    def search(  # pylint: disable = too-many-arguments
        self,
        term: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        query_data: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> RestList:
        """Search for a list of objects.

        Args:
            term: Term to search for
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            query_data: Dict of additional query parameters
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            A :class:`~reporter.base.RestList` of :class:`~reporter.base.RestObject` instances.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        return self._get_list(
            extra_path="/search",
            page=page,
            page_size=page_size,
            term=term,
            query_data=query_data,
            **kwargs,
        )


class UpdateMixin(Generic[ChildOfRestObject]):
    """Manager can update objects."""

    _path: str
    _obj_cls: Type[ChildOfRestObject]
    _obj_cast: Callable
    reporter: Reporter

    def update(
        self,
        id: str,
        attrs: Mapping[str, Any],
        **kwargs: Any,
    ) -> ChildOfRestObject:
        """Update an object of type self._obj_cls.

        Args:
            id: ID of the object to update
            attrs: Attributes to update
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The response from the server, serialized into the object type.

        Raises:
            :class:`~reporter.exceptions.ReporterHttpError`: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        path = f"{self._path}/{id}"

        result = self.reporter.http_request(
            verb="patch",
            path=path,
            post_data=attrs,
            **kwargs,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RestManager)
        if hasattr(self, "_obj_cast"):
            return self._obj_cast(self.reporter, result.json())
        return self._obj_cls(self.reporter, result.json())


class CrudMixin(
    CreateMixin, GetMixin, UpdateMixin, DeleteMixin, Generic[ChildOfRestObject]
):
    """Composite class of other mixins."""

    _obj_cls: Type[ChildOfRestObject]
