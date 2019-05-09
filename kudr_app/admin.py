from django.contrib import admin
from kudr_app.models import *
from django.contrib.auth.models import User


class ChoreographerInline(admin.StackedInline):
    model = Choreographer


class ParticipantInline(admin.StackedInline):
    model = Participant


admin.site.unregister(User)
admin.site.register(User)

#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
    # inlines = (ChoreographerInline, ParticipantInline,)
    #
    # def choreographers(self, request):
    #     choreographers = []
    #     for c in Choreographer.objects.filter(User=request.name):
    #         choreographers.append(c)
    #     return choreographers


class ChoreographerDanceStyle(admin.TabularInline):
    model = ChoreographerDanceStyle
    extra = 1


@admin.register(Choreographer)
class ChoreographerAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('user', 'last_name', 'slug', 'first_name', 'patronymic', 'phone', 'email', 'picture', 'description')
    list_filter = ('last_name','first_name')
    search_fields = ['last_name', 'first_name', 'email','user']

    inlines = (ChoreographerDanceStyle,)

    def dance_styles(self, request):
        dance_styles = []
        for dance_style in ChoreographerDanceStyle.objects.filter(Choreographer=request.name):
            dance_styles.append(dance_style)
        return dance_styles


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
        'user', 'last_name', 'first_name', 'patronymic', 'phone', 'email', 'picture', 'birth_date',
        'description')
    list_filter = ('last_name', 'first_name', 'patronymic')
    search_fields = ['last_name', 'first_name', 'email','user']


@admin.register(Dance)
class DanceAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'duration', 'picture', 'description')
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


@admin.register(PhotoGallery)
class PhotoGalleryAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ['name']


@admin.register(PhotoInGallery)
class PhotoInGalleryAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('name', 'picture', 'date', 'description')
    list_filter = ('name', 'date')
    search_fields = ['name', 'date']

    def gallery(self, request):
        gallery = PhotoGallery.objects.filter(PhotoGallery=request.name)
        return gallery


class GroupChoreographerSchedule(admin.TabularInline):
    model = GroupChoreographerSchedule
    extra = 0


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('begin_time', 'end_time', 'address', 'description')
    list_filter = ('begin_time', 'end_time')
    search_fields = ['begin_time', 'end_time']

    inlines = (GroupChoreographerSchedule,)

    def choreographer(self, request):
        choreographer = GroupChoreographerSchedule.objects.filter(Choreographer=request.name)
        return choreographer

    def dance_style(self, request):
        dance_style = GroupChoreographerSchedule.objects.filter(DanceStyle=request.name)
        return dance_style

    def group(self, request):
        group = GroupChoreographerSchedule.objects.filter(Group=request.name)
        return group

    def weekday(self, request):
        weekday = GroupChoreographerSchedule.objects.filter(WeekDay=request.name)
        return weekday


# @admin.register(GroupChoreographerSchedule)
# class GroupChoreographerScheduleAdmin(admin.ModelAdmin):
#     empty_value_display = 'null'
#


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
    list_display = ('sum', 'participant', 'slug')
    list_filter = ('participant',)
    # search_fields = ['participant']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    empty_value_display = 'null'
    list_display = ('month', 'participant', 'slug')
    list_filter = ('month', 'participant',)
    # search_fields = ['month', 'participant']


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
    # search_fields = ['participant_concert', 'dance']


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
