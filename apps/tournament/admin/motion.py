from django.contrib.admin import ModelAdmin


class MotionAdmin(ModelAdmin):
    list_display = ['id', 'is_public', 'motion', 'infoslide']
    ordering = ['-id']
    actions = ['published_motion']

    def published_motion(self, request, queryset):
        queryset.update(is_public=True)

    published_motion.short_description = 'Добавить в Telegram'
