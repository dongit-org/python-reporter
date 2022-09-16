"""Mixins for model CRUD operations.

Instances of RestManager should derive these mixins according to the operations possible
on their corresponding RestObject in the Reporter API.

"""

# pylint: disable = too-few-public-methods

from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TYPE_CHECKING,
    TypeVar,
    Sequence,
    Union,
)

from reporter.base import RestList, RestManager, RestObject
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


O = TypeVar("O", bound=RestObject)


class CreateMixin(Generic[O]):
    """Manager can create object."""

    _path: str
    _obj_cls: Type[O]
    reporter: Reporter

    def create(
        self,
        attrs: Dict[str, Any],
        file: Optional[Any] = None,
        **kwargs: Any,
    ) -> O:
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
        return self._obj_cls(self.reporter, result.json())


class DeleteMixin(Generic[O]):
    """Manager can delete object."""

    _path: str
    _obj_cls: Type[O]
    reporter: Reporter

    def delete(
        self,
        id_: str,
        **kwargs: Any,
    ):
        """Delete an object.

        Args:
            id\\_: The ID of the object to delete.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = f"{self._path}/{id_}"

        self.reporter.http_request(
            verb="delete",
            path=path,
            **kwargs,
        )


class GetMixin(Generic[O]):
    """Manager can retrieve object."""

    _path: str
    _includes: Dict[str, Type[Union[O, Sequence[O]]]] = {}
    _obj_cls: Type[O]
    reporter: Reporter

    def get(
        self,
        id_: str,
        include: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> O:
        # Regarding the id\\_: https://github.com/sphinx-doc/sphinx/issues/7857
        """Retrieve a single object.

        Args:
            id\\_: The ID of the object to retrieve.
            include: Related data to include in the response.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

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
            **kwargs,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RestManager)

        return self._obj_cls(self.reporter, result.json())


class GetRawMixin(Generic[O]):
    """Manager can retrieve raw file contents."""

    _path: str
    _obj_cls: Type[O]
    reporter: Reporter

    def get(
        self,
        id_: str,
        **kwargs: Any,
    ) -> bytes:
        """Retrieve a single object.

        Args:
            id\\_: Object ID
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

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
            **kwargs,
        )

        return result.content


class _ListMixin(Generic[O]):
    """Parent class for ListMixin and SearchMixin."""

    _path: str
    _includes: Dict[str, Type[Union[O, Sequence[O]]]] = {}
    _obj_cls: Type[O]
    reporter: Reporter

    def _get_list(  # pylint: disable = too-many-arguments, too-many-locals
        self,
        extra_path: str = "",
        term: Optional[str] = None,
        filter_: Optional[Dict[str, str]] = None,
        sort: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs: Any,
    ) -> RestList:
        """Retrieve a list of objects.

        Args:
            extra_path: Extra text to add to the request URL path
            term: A search term.
            filter\\_: query string parameters for HTTP request of the form
                filter[field]
            sort: How to sort retrieved items
            include: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            A RestList of objects.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = self._path + extra_path

        query_data = {}

        if term is not None:
            query_data["term"] = term

        if filter_ is None:
            filter_ = {}
        for (key, value) in filter_.items():
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
            verb="get",
            path=path,
            query_data=query_data,
            **kwargs,
        )

        json = result.json()
        if TYPE_CHECKING:
            assert isinstance(self, RestManager)
        data = [self._obj_cls(self.reporter, attrs) for attrs in json["data"]]
        links = json["links"]
        meta = json["meta"]

        return RestList(data=data, links=links, meta=meta)


class ListMixin(_ListMixin):
    """Manager can list objects."""

    def list(  # pylint: disable = too-many-arguments
        self,
        filter_: Optional[Dict[str, str]] = None,
        sort: Optional[List[str]] = None,
        include: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs: Any,
    ) -> RestList:
        """Retrieve a list of objects.

        Args:
            filter\\_: query string parameters for HTTP request of the form
                filter[field]
            sort: How to sort retrieved items
            include: Types of related data to include
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            A RestList of objects.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        return self._get_list(
            extra_path="",
            filter_=filter_,
            sort=sort,
            include=include,
            page=page,
            page_size=page_size,
            **kwargs,
        )


class SearchMixin(_ListMixin):
    """Manager can search for objects."""

    def search(  # pylint: disable = too-many-arguments
        self,
        term: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        **kwargs: Any,
    ) -> RestList:
        """Search for a list of objects.

        Args:
            term: Term to search for
            page: ID of the page to return - page[number]
            page_size: Number of items to return per page - page[size]
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            A RestList of objects.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        return self._get_list(
            extra_path="/search",
            page=page,
            page_size=page_size,
            term=term,
            **kwargs,
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
        **kwargs: Any,
    ) -> O:
        """Update an object of type self._obj_cls.

        Args:
            id\\_: ID of the object to update
            attrs: Attributes to update
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

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
            **kwargs,
        )

        if TYPE_CHECKING:
            assert isinstance(self, RestManager)
        return self._obj_cls(self.reporter, result.json())


class CRUDMixin(CreateMixin, GetMixin, UpdateMixin, DeleteMixin):
    """Composite class of other mixins."""
