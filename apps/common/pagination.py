from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class DynamicPageSizePagination(PageNumberPagination):
    """
    A custom pagination class that allows dynamic page size based on the request query parameter.

    Attributes:
        page_size_query_param (str): The name of the query parameter used to specify the page size.
        page_size (int): The default page size to use if the query parameter is not provided.
        max_page_size (int): The maximum allowed page size.
    """

    page_size_query_param = "size"
    page_size = getattr(settings, "PAGE_SIZE")
    max_page_size = getattr(settings, "MAX_PAGE_SIZE")
