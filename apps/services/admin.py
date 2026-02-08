from django.contrib import admin
from .models import HousingOffer, HousingApplication, CarpoolingOffer, ForumPost, ForumComment

@admin.register(HousingOffer)
class HousingOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'housing_type', 'location', 'price', 'created_at', 'application_count')
    list_filter = ('housing_type', 'created_at')
    search_fields = ('title', 'location', 'description')
    ordering = ('-created_at',)

    def application_count(self, obj):
        return obj.applications.count()
    application_count.short_description = 'Candidatures'

@admin.register(HousingApplication)
class HousingApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'offer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('applicant__username', 'applicant__email', 'offer__title', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CarpoolingOffer)
class CarpoolingOfferAdmin(admin.ModelAdmin):
    list_display = ('departure', 'destination', 'driver', 'date_time', 'seats_available', 'price')
    list_filter = ('date_time',)
    search_fields = ('departure', 'destination')
    ordering = ('date_time',)

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'comment_count')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Réponses'

@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
