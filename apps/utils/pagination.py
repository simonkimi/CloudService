from rest_framework.pagination import PageNumberPagination


class StanderPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'p'
    max_page_size = 10000
    page_size_query_param = 's'
