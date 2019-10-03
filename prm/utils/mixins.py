# Django REST Framework
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status


class ListModelFilterBetweenDatesMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        """Check for 'from' and 'to' date query params to return a date range
           of moods. Date must be formatted as "YYYY-MM-DD" """
        # TODO: Validate date fields
        if bool('from' in request.query_params) ^ \
                bool('to' in request.query_params):
            return Response(
                {'message': 'need to add from and to date params together'},
                status=status.HTTP_400_BAD_REQUEST)
        elif 'from' in request.query_params and 'to' in request.query_params:
            queryset = self.filter_queryset_dates(
                request,
                request.query_params['from'],
                request.query_params['to'])
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def filter_queryset_dates(self, request, from_date, to_date):
        """Filtering the models based on their date fields. Defaults to models
           that have a date field on their models, if not, override this method
           """
        return self.get_queryset().filter(
            date__gte=from_date,
            date__lte=to_date)
