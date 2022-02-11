from datacenter.models import Passcard, Visit, format_duration
from django.shortcuts import render
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    this_passcard_visits = []
    for visit in Visit.objects.filter(passcard__owner_name=passcard.owner_name):
        this_passcard_visits.append(
            {
                'entered_at': localtime(visit.entered_at),
                'duration': format_duration(visit.get_duration()),
                'is_strange': visit.is_long()
            }
        )
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
