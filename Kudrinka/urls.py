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
from django.conf.urls import url, handler400,handler500
from django.conf.urls.static import static
from django.contrib import admin
from Kudrinka import settings
from kudr_app.views import *
handler404 = e_handler404
handler500 = e_handler500
urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main_page'),
    path('admin/', admin.site.urls),
    path('404/',e_handler404),
    path('404/',e_handler500),
    url(r'^registration/$', registration, name='registration'),
    url(r'^success/$', SuccessfulRegistrationView.as_view(), name='success'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login/$', LoginPageView.as_view(), name='login'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts'),
    url(r'^about_us/$', AboutUsView.as_view(), name='about_us'),
    url(r'^rules/$', RulesView.as_view(), name='rules'),
    path('news/<str:slug>/', OneNewsPage.as_view(), name='new'),
    url(r'^tap_dance/$', TapDanceView.as_view(), name='tap_dance'),
    url(r'^russian_dance/$', RussianDanceView.as_view(), name='russian_dance'),
    url(r'^world_dance/$', WorldDanceView.as_view(), name='world_dance'),
    url(r'^modern_dance/$', ModernDanceView.as_view(), name='modern_dance'),
    url(r'^kids_dance/$', KidsDanceView.as_view(), name='kids_dance'),
    url(r'^gypsy/$', GypsyView.as_view(), name='gypsy'),
    url(r'^flamenco/$', FlamencoView.as_view(), name='flamenco'),
    url(r'^kumbia/$', KumbiaView.as_view(), name='kumbia'),


    url(r'^new_participant/$', AddParticipant.as_view(), name='new_participant'),
    path('participants/<str:slug>/update', UpdateParticipant.as_view(), name='update_participant'),
    path('participants/<str:slug>/delete', DeleteParticipant.as_view(), name='delete_participant'),

    url(r'^new_dance/$', AddDance.as_view(), name='new_dance'),
    path('dances/<str:slug>/update', UpdateDance.as_view(), name='update_dance'),
    path('dances/<str:slug>/delete', DeleteDance.as_view(), name='delete_dance'),

    url(r'^new_news/$', AddNews.as_view(), name='new_news'),
    url(r'^news/$', NewsPage.as_view(), name='news'),
    path('news/<str:slug>/', OneNewsPage.as_view(), name='one_news'),
    path('news/<str:slug>/update', UpdateNews.as_view(), name='update_news'),
    path('news/<str:slug>/delete', DeleteNews.as_view(), name='delete_news'),

    url(r'^new_concert/$', AddConcert.as_view(), name='new_concert'),
    url(r'^concerts/$', ConcertsPage.as_view(), name='concerts'),
    path('concerts/<str:slug>/update', UpdateConcert.as_view(), name='update_concert'),
    path('concerts/<str:slug>/delete', DeleteConcert.as_view(), name='delete_concert'),

    url(r'^new_dance_in_concert/$', AddDanceInConcert.as_view(), name='new_dance_in_concert'),
    path('dances_in_concert/<str:slug>/update', UpdateDanceInConcert.as_view(), name='update_dance_in_concert'),
    path('dances_in_concert/<str:slug>/delete', DeleteDanceInConcert.as_view(), name='delete_dance_in_concert'),

    url(r'^new_participant_concert/$', AddParticipantConcert.as_view(), name='new_participant_concert'),
    path('participants_concert/<str:slug>/update', UpdateParticipantConcert.as_view(),
         name='update_participant_concert'),
    path('participants_concert/<str:slug>/delete', DeleteParticipantConcert.as_view(),
         name='delete_participant_concert'),

    url(r'^new_group/$', AddGroup.as_view(), name='new_group'),
    path('groups/<str:slug>/update', UpdateGroup.as_view(), name='update_group'),
    path('groups/<str:slug>/delete', DeleteGroup.as_view(), name='delete_group'),

    url(r'^new_dance_style/$', AddDanceStyle.as_view(), name='new_dance_style'),
    path('dance_styles/<str:slug>/update', UpdateDanceStyle.as_view(), name='update_dance_style'),
    path('dance_styles/<str:slug>/delete', DeleteDanceStyle.as_view(), name='delete_dance_style'),

    url(r'^new_schedule/$', AddSchedule.as_view(), name='new_schedule'),
    url(r'^schedule/$', SchedulePage.as_view(), name='schedule'),
    path('schedule/<str:slug>/update', UpdateSchedulePart.as_view(), name='update_schedule_part'),
    path('schedule/<str:slug>/delete', DeleteSchedulePart.as_view(), name='delete_schedule_part'),

    url(r'^new_choreographer/$', AddChoreographer.as_view(), name='new_choreographer'),
    url(r'^choreographers/$', ChoreographersView.as_view(), name='choreographers'),

    path('choreographers/<str:slug>/update', UpdateChoreographer.as_view(), name='update_choreographer'),
    path('choreographers/<str:slug>/delete', DeleteChoreographer.as_view(), name='delete_choreographer'),

    url(r'^new_participant_dance_concert/$', AddParticipantDanceConcert.as_view(),
        name='new_participant_dance_concert'),

    path('participants_dances_concerts/<str:slug>/update', UpdateParticipantDanceConcert.as_view(),
         name='update_participant_dance_concert'),
    path('participants_dances_concerts/<str:slug>/delete', DeleteParticipantDanceConcert.as_view(),
         name='delete_participant_dance_concert'),

    url(r'^new_fond/$', AddFond.as_view(), name='new_fond'),
    path('fonds/<str:slug>/update', UpdateFond.as_view(), name='update_fond'),
    path('fonds/<str:slug>/delete', DeleteFond.as_view(), name='delete_fond'),

    url(r'^new_payment/$', AddPayment.as_view(), name='new_payment'),
    path('payments/<str:slug>/update', UpdatePayment.as_view(), name='update_payment'),
    path('payments/<str:slug>/delete', DeletePayment.as_view(), name='delete_payment'),

    url(r'^new_costume/$', AddCostume.as_view(), name='new_costume'),
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
    path('participant_costume/<str:slug>/update', UpdateParticipantCostume.as_view(),
         name='update_participant_costume'),
    path('participant_costume/<str:slug>/delete', DeleteParticipantCostume.as_view(),
         name='delete_participant_costume'),

    path('plot/<str:slug>', Plots.as_view(), name='plot'),
    path('money_plot/', MoneyPlots.as_view(), name='money_plot'),

    url(r'^my_page_choreographer/$', MyPageChoreographer.as_view(), name='my_page_choreographer'),
    url(r'^my_page_participant/$', MyPageParticipant.as_view(), name='my_page_participant'),
    url(r'^my_page_admin/$', MyPageAdmin.as_view(), name='my_page_admin'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
