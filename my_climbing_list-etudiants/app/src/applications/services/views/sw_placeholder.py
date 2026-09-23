from django.http import HttpResponse


def sw_placeholder_view(request):
    file_path = service_worker_path = 'static/base/pwa/config/sw/swPlaceHolder.js'

    with open(file_path, "r", encoding="utf-8") as f:
        sw_placeholder_script = f.read()

    response = HttpResponse(sw_placeholder_script, content_type="application/javascript")
    return response
