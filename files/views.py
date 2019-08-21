from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Count, Q
from django.db.models.functions import TruncDay
from django.http import HttpResponseBadRequest, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, CreateView
from wsgiref.util import FileWrapper
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from files.forms import FileHolderCreateForm, UrlHolderCreateForm
from files.models import UrlHolder, FileHolder
from files.serializers import UrlHolderSerializer, FileHolderSerializer


class SafetyViewSetMixin(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]


class FileViewSet(SafetyViewSetMixin):
    queryset = FileHolder.objects.filter(expires_at__gt=timezone.now())
    serializer_class = FileHolderSerializer
    lookup_field = 'slug'

    @action(detail=True)
    def download(self, request, slug):
        file = self.get_object()
        if request.GET.get('password') != file.password:
            return HttpResponseBadRequest("Wrong password")
        file.click_count = F('click_count') + 1
        file.save()
        response = HttpResponse(FileWrapper(file.file), content_type='text')
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response

    @action(detail=False, queryset=FileHolder.objects.all())
    def statistics(self, request):
        files = dict(
            FileHolder.objects
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .order_by('day')
            .annotate(
                count=Count('pk', filter=Q(click_count__gt=0))
            )
            .values_list('day', 'count')
        )
        urls = dict(
            UrlHolder.objects
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .order_by('day')
            .annotate(
                count=Count('pk', filter=Q(click_count__gt=0))
            )
            .values_list('day', 'count')
        )

        days = set(list(urls.keys()) + list(files.keys()))

        data = [{
            str(day): {
                'files': files.get(day, 0),
                'links': urls.get(day, 0)
            }
            for day in days
        }]

        return Response(data=data)


class UrlViewSet(SafetyViewSetMixin):
    queryset = UrlHolder.objects.filter(expires_at__gt=timezone.now())
    serializer_class = UrlHolderSerializer


class FileHolderCreateView(LoginRequiredMixin, CreateView):
    model = FileHolder
    form_class = FileHolderCreateForm

    def get_success_url(self):
        return f"{reverse('files-detail', kwargs={'slug': self.object.slug})}?password={self.object.password}&created=true"


class FileHolderDetailView(LoginRequiredMixin, DetailView):
    queryset = FileHolder.objects.filter(expires_at__gt=timezone.now())
    model = FileHolder

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.get('password') != self.object.password:
            return HttpResponseBadRequest("Wrong password")
        if not request.GET.get('created'):
            self.object.click_count = F('click_count') + 1
            self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class UrlHolderCreateView(LoginRequiredMixin, CreateView):
    model = UrlHolder
    form_class = UrlHolderCreateForm

    def get_success_url(self):
        return f"{reverse('urls-detail', kwargs={'slug': self.object.slug})}?password={self.object.password}&created=true"


class UrlHolderDetailView(LoginRequiredMixin, DetailView):
    queryset = UrlHolder.objects.filter(expires_at__gt=timezone.now())
    model = UrlHolder

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.GET.get('password') != self.object.password:
            return HttpResponseBadRequest("Wrong password")
        if not request.GET.get('created'):
            self.object.click_count = F('click_count') + 1
            self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
