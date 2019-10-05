# Django REST Framework
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status

# Validators
from .validators import validate_date


class ListModelFilterBetweenDatesMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        """Check for 'from' and 'to' date query params to return a date range
           of moods. Date must be formatted as "YYYY-MM-DD" """
        from_date = request.query_params.get('from', None)
        to_date = request.query_params.get('to', None)

        # 'from' and 'to' fields must come either both or none.
        if bool(from_date) ^ bool(to_date):
            return Response(
                {'message': "'from' and 'to' params must come together"},
                status=status.HTTP_400_BAD_REQUEST)
        elif from_date and to_date:
            try:
                validate_date(from_date)
                validate_date(to_date)
            except ValueError as err:
                return Response({'message': err.args[0]},
                                status=status.HTTP_400_BAD_REQUEST)

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
