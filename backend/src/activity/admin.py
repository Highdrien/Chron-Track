from django.contrib import admin
from django.utils.html import format_html

from activity.models import Activity, ActivityLap
from activity.utils import format_duration, format_pace


class ActivityLapInline(admin.TabularInline):
    model = ActivityLap
    extra = 0
    readonly_fields = (
        "lap_number",
        "display_distance",
        "display_duration",
        "display_pace",
        "avg_hr",
        "max_hr",
        "avg_cadence",
        "elevation_gain",
        "calories",
    )
    fields = (
        "lap_number",
        "display_distance",
        "display_duration",
        "display_pace",
        "avg_hr",
        "max_hr",
        "avg_cadence",
        "elevation_gain",
        "calories",
    )
    ordering = ("lap_number",)

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description="Distance")
    def display_distance(self, obj: ActivityLap):
        return f"{obj.distance_km} km"

    @admin.display(description="Duration")
    def display_duration(self, obj: ActivityLap):
        return format_duration(obj.duration)

    @admin.display(description="Pace")
    def display_pace(self, obj: ActivityLap):
        return format_pace(obj.pace)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "start_time",
        "display_distance",
        "display_duration",
        "display_pace",
        "avg_hr",
        "max_hr",
        "elevation_gain",
        "source",
    )
    list_filter = ("source", "sport_type", "user", "start_time")
    search_fields = ("name", "user__username", "external_id")
    date_hierarchy = "start_time"
    ordering = ("-start_time",)
    list_select_related = ("user",)
    readonly_fields = (
        "display_pace",
        "display_speed",
        "display_distance",
        "external_id",
        "created_at",
    )

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "user",
                    "name",
                    "sport_type",
                    "source",
                    "external_id",
                    "start_time",
                )
            },
        ),
        (
            "Performance",
            {
                "fields": (
                    "display_distance",
                    "duration",
                    "display_pace",
                    "display_speed",
                    "elevation_gain",
                    "elevation_loss",
                )
            },
        ),
        (
            "Heart Rate & Cadence",
            {"fields": ("avg_hr", "max_hr", "avg_cadence", "calories")},
        ),
        (
            "Meta",
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )

    inlines = [ActivityLapInline]

    @admin.display(description="Distance")
    def display_distance(self, obj: Activity):
        return f"{obj.distance_km} km"

    @admin.display(description="Duration")
    def display_duration(self, obj: Activity):
        return format_duration(obj.duration)

    @admin.display(description="Pace")
    def display_pace(self, obj: Activity):
        return format_pace(obj.pace)

    @admin.display(description="Speed")
    def display_speed(self, obj: Activity):
        speed = obj.speed_kmh
        if speed is None:
            return "-"
        return format_html("{} km/h", speed)
