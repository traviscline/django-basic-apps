from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson as json

from basic.flagging.models import *


@login_required
def flag(request, slug, ctype_id, object_id, 
        template_name='flagging/flag_confirm.html',
        success_template_name='flagging/flag_success.html'):
    """
    Flags an available flag type object.

    Templates: ``flagging/flag_confirm.html`` and ``flagging/flag_success.html``
    Context:
        object
            Object object
        flag_type
            FlagType object
    """
    flag_type = get_object_or_404(FlagType, slug=slug)
    content_type = ContentType.objects.get(pk=ctype_id)
    model = content_type.model_class()
    obj = model.objects.get(pk=object_id)
    if request.method == 'POST':
        flag, created = Flag.objects.get_or_create(flag_type=flag_type,
                content_type=content_type, object_id=obj.pk, user=request.user)
        if request.is_ajax():
            response = {'success': 'Success'}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        if request.GET.get('next', None):
            return HttpResponseRedirect(request.GET['next'])
        template_name = success_template_name
    return render_to_response(template_name, {
        'object': obj,
        'flag_type': flag_type
    }, context_instance=RequestContext(request))


@login_required
def unflag(request, slug, ctype_id, object_id,
        template_name='flagging/unflag_confirm.html',
        success_template_name='flagging/unflag_success.html'):
    """
    Unflag an available flag types object.

    Templates: ``flagging/unflag_confirm.html`` and ``flagging/unflag_success.html``
    Context:
        object
            Object object
        flag_type
            FlagType object
    """
    flag_type = get_object_or_404(FlagType, slug=slug)
    content_type = ContentType.objects.get(pk=ctype_id)
    model = content_type.model_class()
    obj = model.objects.get(pk=object_id)
    if request.method == 'POST':
        flag = Flag.objects.get(flag_type=flag_type, content_type=content_type,
                object_id=obj.pk, user=request.user)
        flag.delete()
        if request.is_ajax():
            response = {'success': 'Success'}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        if request.GET.get('next', None):
            return HttpResponseRedirect(request.GET['next'])
        template_name = success_template_name
    return render_to_response(template_name, {
        'object': obj,
        'flag_type': flag_type
    }, context_instance=RequestContext(request))
