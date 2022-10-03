from rest_framework.pagination import PageNumberPagination


class SubscriptionPagination(PageNumberPagination):
    page_size_query_param = 'recipes_limit'
