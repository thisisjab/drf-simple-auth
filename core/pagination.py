from rest_framework.pagination import PageNumberPagination


class UserDefaultPagination(PageNumberPagination):
    page_size = 10