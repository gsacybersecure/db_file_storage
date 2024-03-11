# third party
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
from wsgiref.util import FileWrapper
try:
    from django.utils.translation import ugettext as _
except ImportError:
    from django.utils.translation import gettext as _

# project
from db_file_storage.storage import DatabaseFileStorage


storage = DatabaseFileStorage()


@staff_member_required
def get_file(request, add_attachment_headers, extra_headers=None):
    name = request.GET.get('name')

    try:
        _file = storage.open(name)
    except Exception:
        return HttpResponseBadRequest(_('Invalid request'))

    response = HttpResponse(
        FileWrapper(_file),
        content_type=_file.mimetype
    )
    response['Content-Length'] = _file.tell()
    if add_attachment_headers:
        response['Content-Disposition'] = 'attachment; filename=%(name)s' % {'name': _file.filename}

    for name, value in (extra_headers or {}).items():
        response[name] = value

    return response
