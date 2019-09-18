from django.contrib import admin
from kudr_app.models import *
from django.contrib.auth.models import User


class ChoreographerInline(admin.StackedInline):
    model = Choreographer


class ParticipantInline(admin.StackedInline):
    model = Participant


admin.site.unregister(User)
admin.site.register(User)


@admin.register(Choreographer)
class ChoreographerAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('user', 'last_name', 'slug', 'first_name', 'patronymic', 'phone', 'email', 'picture', 'description')
    list_filter = ('last_name','first_name')
    search_fields = ['last_name', 'first_name', 'email','user']


@admin.register(DanceStyle)
class DanceStyleAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('dance_style', 'description')
    list_filter = ('dance_style',)
    search_fields = ['dance_style']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'ages', 'description')
    list_filter = ('ages','name')
    search_fields = ['name', 'ages']

#
class ParticipantGroup(admin.TabularInline):
    model = ParticipantGroup
    extra = 1


class ParticipantConcert(admin.TabularInline):
    model = ParticipantConcert
    extra = 1


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = (
        'user', 'last_name', 'first_name', 'patronymic','group', 'phone', 'email', 'picture', 'birth_date',
        'description','moderator')
    list_filter = ('group','last_name', 'first_name', 'patronymic')
    search_fields = ['last_name', 'first_name', 'email','user']


@admin.register(Dance)
class DanceAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'duration', 'description')
    list_filter = ('name',)
    search_fields = ['name']


class DanceInConcert(admin.TabularInline):
    model = DanceInConcert
    extra = 1


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'begin_date', 'end_date', 'begin_time', 'end_time', 'place', 'address', 'description')
    list_filter = ('name','begin_date', 'end_date', 'begin_time', 'end_time', 'name')
    search_fields = ['begin_date', 'begin_time', 'end_time', 'name', 'place']

    inlines = (DanceInConcert, ParticipantConcert)

    def dances_in_concert(self, request):
        dances_in_concert = []
        for dance in DanceInConcert.objects.filter(Dance=request.name):
            dances_in_concert.append(dance)
        return dances_in_concert

    def participants_concert(self, request):
        participants_concert = []
        for participant in ParticipantConcert.objects.filter(Participant=request.last_name):
            participants_concert.append(participant)
        return participants_concert


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('title', 'text', 'date', 'picture')
    list_filter = ('date', 'title')
    search_fields = ['date', 'title', 'text']


class GroupChoreographerSchedule(admin.TabularInline):
    model = GroupChoreographerSchedule
    extra = 0


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('day_of_the_week',)
    list_filter = ('day_of_the_week',)
    search_fields = ['day_of_the_week']

    inlines = (GroupChoreographerSchedule,)


@admin.register(Fond)
class FondAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('sum', 'participant', 'slug','all_fonds_null')
    list_filter = ('participant',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('month', 'participant', 'slug')
    list_filter = ('month', 'participant',)

@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('month',)
    list_filter = ('month',)
    search_fields = ['month']


@admin.register(ParticipantDanceConcert)
class ParticipantDanceConcertAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('participant_concert', 'dance')
    list_filter = ('participant_concert', 'dance')


class ParticipantCostume(admin.TabularInline):
    model = ParticipantCostume
    extra = 0


@admin.register(Costume)
class CostumeAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('dance', 'name', 'description')
    list_filter = ('dance', 'name')
    search_fields = ['dance', 'name']

    inlines = (ParticipantCostume,)

    def particicpant_costume(self, request):
        participant_costume = ParticipantCostume.objects.filter(Costume=request.name)
        return participant_costume


@admin.register(Expence)
class ExpencesAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'num', 'cost', 'date', 'bought')
    list_filter = ('name', 'cost')
    search_fields = ['name']


@admin.register(OtherSourceOfFinances)
class OtherSourceOfFinancesAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'sum')
    list_filter = ('name', 'sum')
    search_fields = ['name']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('title', 'text', 'participant', 'date', 'date_until','group')
    list_filter = ('group', 'participant')
    search_fields = ['title', 'text', 'date_until']
