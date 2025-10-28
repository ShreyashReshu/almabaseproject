from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Count
import phonenumbers
from .models import SpamReport
from users.models import User
from contacts.models import Contact


def normalize_phone(phone: str, default_region: str = 'IN'):
    try:
        parsed = phonenumbers.parse(phone, default_region)
        if not phonenumbers.is_possible_number(parsed) or not phonenumbers.is_valid_number(parsed):
            return None
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        return None


class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['id', 'phone', 'created_at']

    def validate_phone(self, value):
        norm = normalize_phone(value)
        if not norm:
            raise serializers.ValidationError('Invalid phone')
        return norm

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)


class SpamReportCreateView(generics.CreateAPIView):
    serializer_class = SpamReportSerializer


class SearchView(APIView):
    def get(self, request):
        q = (request.query_params.get('q') or '').strip()
        if not q:
            return Response({'detail': 'Missing query'}, status=400)
        phone_norm = normalize_phone(q)
        if phone_norm:
            users = list(User.objects.filter(phone=phone_norm).values('id','name','phone'))
            contacts = list(Contact.objects.filter(phone=phone_norm).values('id','name','phone'))
            combined = users + contacts
            for r in combined:
                r['rank'] = 100
        else:
            users = list(User.objects.filter(name__icontains=q).values('id','name','phone'))
            contacts = list(Contact.objects.filter(name__icontains=q).values('id','name','phone'))
            combined = users + contacts
            for r in combined:
                r['rank'] = len(r['name'])

        # dedupe by phone keep highest rank
        best = {}
        for r in combined:
            k = r['phone']
            if k not in best or r['rank'] > best[k]['rank']:
                best[k] = r

        # spam counts
        spam_map = dict(SpamReport.objects.values_list('phone').annotate(c=Count('phone')))
        for r in best.values():
            r['spam_count'] = spam_map.get(r['phone'], 0)

        results = sorted(best.values(), key=lambda x: (x['rank'], x['spam_count']), reverse=True)
        page = int(request.query_params.get('page', 1))
        paginator = Paginator(results, 20)
        page_obj = paginator.get_page(page)
        return Response({
            'query': q,
            'count': paginator.count,
            'results': list(page_obj),
            'page': page_obj.number,
            'num_pages': paginator.num_pages,
        })


class SearchDetailView(APIView):
    def get(self, request, id):
        obj = User.objects.filter(id=id).values('id','name','phone','email').first()
        if not obj:
            obj = Contact.objects.filter(id=id).values('id','name','phone','email').first()
        if not obj:
            return Response({'detail': 'Not found'}, status=404)
        obj['spam_count'] = SpamReport.objects.filter(phone=obj['phone']).count()
        return Response(obj)

# Create your views here.
