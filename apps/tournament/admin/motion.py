from django.contrib.admin import ModelAdmin


class MotionAdmin(ModelAdmin):
    list_display = ['id', 'is_public', 'language', 'motion', 'infoslide']
    ordering = ['-id']
    actions = ['published_motion']

    def published_motion(self, request, queryset):
        from apps.tournament.utils import detect_motion_language

        for motion in queryset.all():
            motion.is_public = True
            detect_motion_language(motion)

    published_motion.short_description = 'Добавить в Telegram'
