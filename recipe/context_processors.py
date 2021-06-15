import datetime as dt


def year(request):
    year = dt.datetime.now().year
    return {
        'year': year,
        }


def shop_list_size(request):
    if request.user.is_authenticated:
        count = request.user.purchases.all().count()
    else:
        count = 0
    return {
        "shop_list_size": count
    }
