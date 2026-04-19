import re
from datetime import timedelta

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from races.models import Race


class DurationHMSWidget(forms.TextInput):
    """Renders a DurationField as HH:MM:SS."""

    def format_value(self, value):
        if value is None:
            return ""
        if isinstance(value, timedelta):
            total = int(value.total_seconds())
            h, remainder = divmod(total, 3600)
            m, s = divmod(remainder, 60)
            return f"{h:02d}:{m:02d}:{s:02d}"
        return value


class DurationHMSField(forms.Field):
    widget = DurationHMSWidget

    def clean(self, value):
        value = super().clean(value)
        if not value:
            return None
        match = re.fullmatch(r"(\d+):([0-5]\d):([0-5]\d)", value.strip())
        if not match:
            raise ValidationError("Format attendu : HH:MM:SS (ex: 01:23:45)")
        h, m, s = int(match[1]), int(match[2]), int(match[3])
        return timedelta(hours=h, minutes=m, seconds=s)


class RaceAdminForm(forms.ModelForm):
    time = DurationHMSField(help_text="Format : HH:MM:SS")

    class Meta:
        model = Race
        fields = "__all__"


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    form = RaceAdminForm

    list_display = (
        "name",
        "edition",
        "user",
        "date",
        "distance",
        "elevation_gain",
        "formatted_time",
        "speed",
        "pace",
        "location",
        "global_ranking",
    )
    list_filter = ("date", "user", "location")
    search_fields = ("name", "edition", "location", "user__username")
    date_hierarchy = "date"
    ordering = ("-date",)
    autocomplete_fields = ("user",)
    list_select_related = ("user",)
    readonly_fields = ("speed", "pace")

    fieldsets = (
        (
            "General",
            {
                "fields": ("user", "name", "edition", "date", "location"),
            },
        ),
        (
            "Performance",
            {
                "fields": ("distance", "elevation_gain", "time", "speed", "pace"),
            },
        ),
        (
            "Ranking",
            {
                "fields": (
                    "number_of_participants",
                    "global_ranking",
                    "category_ranking",
                ),
            },
        ),
        (
            "Links",
            {
                "fields": ("strava_url", "results_url"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Time")
    def formatted_time(self, obj):
        if obj.time is None:
            return "-"
        total = int(obj.time.total_seconds())
        h, remainder = divmod(total, 3600)
        m, s = divmod(remainder, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
