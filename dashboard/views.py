from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from interactions.models import Interaction
from django.db.models import Count


@login_required
def dashboard_view(request):
    recent = Interaction.objects.filter(initiator=request.user).order_by('-created_at')[:10]
    top = (Interaction.objects.filter(initiator=request.user, type__in=['call','message'])
           .values('receiver_id','phone').annotate(c=Count('id')).order_by('-c')[:5])
    spam = (Interaction.objects.filter(type='spam')
            .values('phone').annotate(c=Count('id')).order_by('-c')[:5])
    return render(request, 'dashboard.html', {'recent': recent, 'top': top, 'spam': spam})

# Create your views here.
