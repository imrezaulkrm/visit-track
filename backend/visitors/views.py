from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import csrf_exempt

from .models import Visitor

def get_client_ip(request):
    """Request থেকে ক্লায়েন্টের IP address বের করার ফাংশন"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def track_visitor(request):
    """
    Visitor ট্র্যাক করার জন্য।
    একই IP যদি ৫ মিনিটের মধ্যে আগে থেকে থাকে,
    তাহলে নতুন Visitor তৈরি করা হবে না।
    """
    ip = get_client_ip(request)
    five_minutes_ago = now() - timedelta(minutes=5)

    # Check if IP already visited within last 5 mins
    recent_visit_exists = Visitor.objects.filter(ip_address=ip, visit_time__gte=five_minutes_ago).exists()

    if not recent_visit_exists:
        Visitor.objects.create(ip_address=ip)

    return JsonResponse({"message": "Visitor logged"})


@csrf_exempt
def visitor_stats(request):
    """মোট ভিজিটর এবং গত ৫ মিনিটের লাইভ ভিজিটর সংখ্যা রিটার্ন করে"""
    total_visits = Visitor.objects.count()
    live_visitors = Visitor.objects.filter(visit_time__gte=now() - timedelta(minutes=5)).count()

    return JsonResponse({
        "total_visits": total_visits,
        "live_visitors": live_visitors
    })
