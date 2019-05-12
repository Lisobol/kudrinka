"""Kudrinka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from Kudrinka import settings
from kudr_app.views import *

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),
    path('admin/', admin.site.urls),
    url(r'^registration/$', registration, name='registration'),
    url(r'^success/$', SuccessfulRegistrationView.as_view(), name='success'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login/$', LoginPageView.as_view(), name='login'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts'),
    url(r'^about_us/$', AboutUsView.as_view(), name='about_us'),
    path('news/<str:slug>/', OneNewsPage.as_view(), name='new'),
    url(r'^tap_dance/$', TapDanceView.as_view(), name='tap_dance'),
    url(r'^russian_dance/$', RussianDanceView.as_view(), name='russian_dance'),
    url(r'^world_dance/$', WorldDanceView.as_view(), name='world_dance'),
    url(r'^modern_dance/$', ModernDanceView.as_view(), name='modern_dance'),

    # url(r'^add_dance/$', add_dance, name='add_dance'),
    # url(r'^add_group/$', add_group, name='add_group'),
    # url(r'^add_dance_style/$', add_dance_style, name='add_dance_style'),
    # url(r'^add_choreographer/$', add_choreographer, name='add_choreographer'),
    # url(r'^add_participant/$', add_participant, name='add_participant'),

    url(r'^new_participant/$', AddParticipant.as_view(), name='new_participant'),
    # url(r'^participants/$', ParticipantsPage.as_view(), name='participants'),
    # path('participants/<str:slug>/', ParticipantPage.as_view(), name='participant'),
    path('participants/<str:slug>/update', UpdateParticipant.as_view(), name='update_participant'),
    # path('participants/<str:slug>/update1', UpdateParticipant1.as_view(), name='update_participant1'),

    path('participants/<str:slug>/delete', DeleteParticipant.as_view(), name='delete_participant'),

    url(r'^new_dance/$', AddDance.as_view(), name='new_dance'),
    # url(r'^dances/$', DancesPage.as_view(), name='dances'),
    # path('dances/<str:slug>/', DancePage.as_view(), name='dance'),
    path('dances/<str:slug>/update', UpdateDance.as_view(), name='update_dance'),
    path('dances/<str:slug>/delete', DeleteDance.as_view(), name='delete_dance'),

    url(r'^new_photo_in_gallery/$', AddPhotoInGallery.as_view(), name='new_photo_in_gallery'),

    url(r'^new_news/$', AddNews.as_view(), name='new_news'),
    url(r'^news/$', NewsPage.as_view(), name='news'),
    path('news/<str:slug>/', OneNewsPage.as_view(), name='one_news'),
    path('news/<str:slug>/update', UpdateNews.as_view(), name='update_news'),
    path('news/<str:slug>/delete', DeleteNews.as_view(), name='delete_news'),

    url(r'^new_concert/$', AddConcert.as_view(), name='new_concert'),
    url(r'^concerts/$', ConcertsPage.as_view(), name='concerts'),
    # path('concerts/<str:slug>/', ConcertPage.as_view(), name='concert'),
    path('concerts/<str:slug>/update', UpdateConcert.as_view(), name='update_concert'),
    path('concerts/<str:slug>/delete', DeleteConcert.as_view(), name='delete_concert'),

    url(r'^new_dance_in_concert/$', AddDanceInConcert.as_view(), name='new_dance_in_concert'),
    path('dances_in_concert/<str:slug>/update', UpdateDanceInConcert.as_view(), name='update_dance_in_concert'),
    path('dances_in_concert/<str:slug>/delete', DeleteDanceInConcert.as_view(), name='delete_dance_in_concert'),

    url(r'^new_participant_concert/$', AddParticipantConcert.as_view(), name='new_participant_concert'),
    url(r'^participants_concert/$', ParticipantsConcertsPage.as_view(), name='participants_concert'),
    path('participants_concert/<str:slug>/update', UpdateParticipantConcert.as_view(),
         name='update_participant_concert'),
    path('participants_concert/<str:slug>/delete', DeleteParticipantConcert.as_view(),
         name='delete_participant_concert'),

    url(r'^new_group/$', AddGroup.as_view(), name='new_group'),
    # url(r'^groups/$', GroupsPage.as_view(), name='groups'),
    # path('groups/<str:slug>/', GroupPage.as_view(), name='group'),
    path('groups/<str:slug>/update', UpdateGroup.as_view(), name='update_group'),
    path('groups/<str:slug>/delete', DeleteGroup.as_view(), name='delete_group'),

    url(r'^new_photo_gallery/$', AddPhotoGallery.as_view(), name='new_photo_gallery'),
    url(r'^photo_gallery/$', PhotoGalleriesPage.as_view(), name='photo_galleries'),
    path('photo_gallery/<str:slug>/', PhotoGalleriesPage.as_view(), name='photo_gallery'),
    path('photo_gallery/<str:slug>/update', UpdatePhotoGallery.as_view(), name='update_photo_gallery'),
    path('photo_gallery/<str:slug>/delete', DeletePhotoGallery.as_view(), name='delete_photo_gallery'),

    url(r'^new_dance_style/$', AddDanceStyle.as_view(), name='new_dance_style'),
    # url(r'^dance_styles/$', DanceStylesPage.as_view(), name='dance_styles'),
    # path('dance_styles/<str:slug>/', DanceStylePage.as_view(), name='dance_style'),
    path('dance_styles/<str:slug>/update', UpdateDanceStyle.as_view(), name='update_dance_style'),
    path('dance_styles/<str:slug>/delete', DeleteDanceStyle.as_view(), name='delete_dance_style'),

    url(r'^new_class_schedule/$', AddClassSchedule.as_view(), name='new_class_schedule'),
    url(r'^class_schedules/$', ClassSchedulesPage.as_view(), name='class_schedules'),
    path('class_schedules/<str:slug>/', ClassSchedulePage.as_view(), name='class_schedule'),
    path('class_schedules/<str:slug>/update', UpdateClassSchedule.as_view(), name='update_class_schedule'),
    path('class_schedules/<str:slug>/delete', DeleteClassSchedule.as_view(), name='delete_class_schedule'),

    url(r'^new_schedule/$', AddSchedule.as_view(), name='new_schedule'),
    url(r'^schedule/$', SchedulePage.as_view(), name='schedule'),
    path('schedule/<str:slug>/', SchedulePartPage.as_view(), name='schedule_part'),
    path('schedule/<str:slug>/update', UpdateSchedulePart.as_view(), name='update_schedule_part'),
    path('schedule/<str:slug>/delete', DeleteSchedulePart.as_view(), name='delete_schedule_part'),
    # url(r'^schedule_part/$', SchedulePartPage.as_view(), name='schedule_part'),

    url(r'^new_choreographer/$', AddChoreographer.as_view(), name='new_choreographer'),
    url(r'^choreographers/$', ChoreographersView.as_view(), name='choreographers'),

    # url(r'^choreographers/$', ChoreographersPage.as_view(), name='choreographers'),
    # path('choreographers/<str:slug>/', ChoreographerPage.as_view(), name='choreographer'),
    path('choreographers/<str:slug>/update', UpdateChoreographer.as_view(), name='update_choreographer'),
    path('choreographers/<str:slug>/delete', DeleteChoreographer.as_view(), name='delete_choreographer'),

    # path('participants_dances_concerts/<str:slug>/', ParticipantDanceConcertPage.as_view(),
    #      name='participant_dance_concert'),
    url(r'^new_participant_dance_concert/$', AddParticipantDanceConcert.as_view(), name='new_participant_dance_concert'),

    # url(r'^participants_dances_concerts/$', ParticipantDanceConcertPage.as_view(), name='participant_dance_concert'),
    path('participants_dances_concerts/<str:slug>/update', UpdateParticipantDanceConcert.as_view(),
         name='update_participant_dance_concert'),
    path('participants_dances_concerts/<str:slug>/delete', DeleteParticipantDanceConcert.as_view(),
         name='delete_participant_dance_concert'),

    url(r'^new_fond/$', AddFond.as_view(), name='new_fond'),
    url(r'^fonds/$', FondsPage.as_view(), name='fonds'),
    path('fonds/<str:slug>/', FondPage.as_view(), name='fond'),
    path('fonds/<str:slug>/update', UpdateFond.as_view(), name='update_fond'),
    path('fonds/<str:slug>/delete', DeleteFond.as_view(), name='delete_fond'),

    url(r'^new_payment/$', AddPayment.as_view(), name='new_payment'),
    url(r'^payments/$', PaymentsPage.as_view(), name='payments'),
    path('payments/<str:slug>/', PaymentPage.as_view(), name='payment'),
    path('payments/<str:slug>/update', UpdatePayment.as_view(), name='update_payment'),
    path('payments/<str:slug>/delete', DeletePayment.as_view(), name='delete_payment'),

    url(r'^new_costume/$', AddCostume.as_view(), name='new_costume'),
    # url(r'^costumes/$', CostumesPage.as_view(), name='costumes'),
    # path('costumes/<str:slug>/', CostumePage.as_view(), name='costume'),
    path('costumes/<str:slug>/update', UpdateCostume.as_view(), name='update_costume'),
    path('costumes/<str:slug>/delete', DeleteCostume.as_view(), name='delete_costume'),

    url(r'^new_expence/$', AddExpence.as_view(), name='new_expence'),
    path('expences/<str:slug>/update', UpdateExpence.as_view(), name='update_expence'),
    path('expences/<str:slug>/delete', DeleteExpence.as_view(), name='delete_expence'),

    url(r'^new_other_source/$', AddOtherSourceOfFinance.as_view(), name='new_other_source'),
    path('other_sources/<str:slug>/update', UpdateOtherSourceOfFinance.as_view(), name='update_other_source'),
    path('other_sources/<str:slug>/delete', DeleteOtherSourceOfFinance.as_view(), name='delete_other_source'),

    url(r'^new_announcement/$', AddAnnouncement.as_view(), name='new_announcement'),
    path('announcements/<str:slug>/update', UpdateAnnouncement.as_view(), name='update_announcement'),
    path('announcements/<str:slug>/delete', DeleteAnnouncement.as_view(), name='delete_announcement'),

    url(r'^new_participant_costume/$', AddParticipantCostume.as_view(), name='new_participant_costume'),
    path('participant_costume/<str:slug>/update', UpdateParticipantCostume.as_view(), name='update_participant_costume'),
    path('participant_costume/<str:slug>/delete', DeleteParticipantCostume.as_view(), name='delete_participant_costume'),

    path('plot/<str:slug>', Plots.as_view(),name='plot'),

    url(r'^my_page_choreographer/$', MyPageChoreographer.as_view(), name='my_page_choreographer'),
    url(r'^my_page_participant/$', MyPageParticipant.as_view(), name='my_page_participant'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
