from rest_framework.pagination import PageNumberPagination

class MedicinePagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'