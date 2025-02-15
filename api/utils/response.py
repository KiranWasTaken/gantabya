from rest_framework.response import Response
from django.utils import timezone


def success(data=None, message="Success", page=0, size=0, count=0, total=None):
    res = {"error": 0, "message": message}
    if data is not None:
        res.update(data=data)
    if page != 0 or isinstance(data, list):
        res.update(page=page, size=size, count=count)
    if total is not None:
        res.update(total=total)
    # return Response(res)
    return Response(res, status=200, content_type="application/json; charset=utf-8")


def error(data=None, message="Error", status=400):
    if data:
        message = str(data)
    res = {"data": data, "message": message, "error": status}
    # print("Error ::", res)
    return Response(res, status=status)


def paginated(data, request, forced_size=None):
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("size", 10))
    if forced_size:
        size = forced_size
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    count = data.count() if type(data) != list else len(data)
    paginated_data = data[start_idx:end_idx]
    return paginated_data, page, size, count


def get_start_end_date(request, default_time_period=None):
    if default_time_period == "day":
        default_start_date = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        default_end_date = (
            default_start_date
            + timezone.timedelta(days=1)
            - timezone.timedelta(seconds=1)
        )
    elif default_time_period == "week":
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        default_start_date = now - timezone.timedelta(days=7)
        default_end_date = (
            now + timezone.timedelta(days=1) - timezone.timedelta(seconds=1)
        )
    elif default_time_period == "month":
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        default_start_date = now - timezone.timedelta(days=28)
        default_end_date = (
            now + timezone.timedelta(days=1) - timezone.timedelta(seconds=1)
        )

    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    if start_date and start_date != "" and end_date and end_date != "":
        start_date = timezone.now().strptime(start_date, "%Y-%m-%d")
        end_date = timezone.now().strptime(end_date, "%Y-%m-%d")
        end_date += timezone.timedelta(days=1) - timezone.timedelta(seconds=1)
    elif default_time_period:
        start_date = default_start_date
        end_date = default_end_date
    else:
        start_date = None
        end_date = None
    return start_date, end_date
