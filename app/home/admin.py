from django.contrib import admin
from .models import Pregunta, Opcion, Respuesta, RespuestaSummary
from django.db.models import Count, Sum, DateTimeField

admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(Respuesta)

@admin.register(RespuestaSummary)
class RespuestaSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/respuesta_summary_change_list.html'
    date_hierarchy = 'fecha_creacion'
    list_filter = (
        'opcion',
    )
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
                request,
                extra_context=extra_context,
            )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError) as error:
            print("Exception")
            print(error)
            return response

        metrics = {
                'total': Count('id'),
                }
        response.context_data['summary'] = list(
                qs
                .values('opcion__opcion_texto')
                .annotate(**metrics)
                .order_by('-total')
            )
        return response
