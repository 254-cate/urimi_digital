from django.shortcuts import redirect
from functools import wraps


def farmer_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.profile.role != "Farmer":
            return redirect("officerdashboard")

        return view_func(request, *args, **kwargs)

    return wrapper



def officer_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.profile.role != "Officer":
            return redirect("farmerdashboard")

        return view_func(request, *args, **kwargs)

    return wrapper