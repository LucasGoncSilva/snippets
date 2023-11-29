from typing import Any

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def handle<code: int>(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    return render(
        r,
        'err/error_template.html',
        {...}
    )
