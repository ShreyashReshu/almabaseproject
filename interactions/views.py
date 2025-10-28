from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.utils.dateparse import parse_datetime
from .models import Interaction


class RecentInteractionsView(APIView):
    def get(self, request):
        t = request.query_params.get('type')
        qs = Interaction.objects.filter(initiator=request.user)
        if t:
            qs = qs.filter(type=t)
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * size
        end = start + size
        items = list(qs.order_by('-created_at').values('id','type','receiver_id','phone','metadata','created_at')[start:end])
        return Response({'results': items, 'page': page})


class TopContactsView(APIView):
    def get(self, request):
        n = int(request.query_params.get('n', 5))
        qs = (Interaction.objects
              .filter(initiator=request.user, type__in=['call','message'])
              .values('receiver_id','phone')
              .annotate(c=Count('id'))
              .order_by('-c')[:n])
        return Response({'results': list(qs)})


class SpamAggregatesView(APIView):
    def get(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        qs = Interaction.objects.filter(type='spam')
        if start:
            qs = qs.filter(created_at__gte=parse_datetime(start))
        if end:
            qs = qs.filter(created_at__lte=parse_datetime(end))
        by_phone = list(qs.values('phone').annotate(c=Count('id')).order_by('-c'))
        by_user = list(qs.values('receiver_id').annotate(c=Count('id')).order_by('-c'))
        return Response({'by_phone': by_phone, 'by_user': by_user})

# Create your views here.
