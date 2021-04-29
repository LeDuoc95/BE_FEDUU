from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import pagination
import math

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page'
    max_page_size = 100


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        per_page = self.page.paginator.per_page
        count = self.page.paginator.count
        total_page = math.ceil(count / per_page)
        return Response({
            'links': {
                'prev': self.get_previous_link(),
                'next': self.get_next_link(),
                'page': self.page.number,
                'page_size': per_page,
                'total_record': count,
                'total_page': total_page,
            },
            'data': data
        })

class CustomPagination2(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })
