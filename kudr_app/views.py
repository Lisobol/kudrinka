from django.views.generic import TemplateView, View, ListView
from django.contrib.auth.views import LoginView, logout_then_login
from django.shortcuts import render, redirect
from django.urls import reverse
from kudr_app.forms import *
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from django.forms import modelformset_factory
from datetime import date, time, timedelta
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly
import matplotlib.dates as mdates
import datetime as dt
import csv
from io import BytesIO
import base64
import MySQLdb


# ГЛАВНАЯ СТРАНИЦА
class MainPageView(TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        # choreographer = Choreographer.objects.get(user=logged_user)

        try:
            choreographer = Choreographer.objects.get(user=logged_user)
        except Exception:
            choreographer = None
        try:
            participant = Participant.objects.get(user=logged_user)
        except Exception:
            participant = None

        context['logged_user'] = logged_user
        context['choreographer'] = choreographer
        context['participant'] = participant

        # dance_styles = DanceStyle.objects.all()
        # context['dance_styles'] = dance_styles

        # Новости
        news = News.objects.all().order_by('-date')[:5]

        context['news'] = news

        # Расписание
        gr_ch_sh = GroupChoreographerSchedule.objects.all().order_by('class_schedule__begin_time')
        group = Group.objects.all()
        dance_style = DanceStyle.objects.all()
        weekdays = WeekDay.objects.all()
        class_schedule = ClassSchedule.objects.all()
        context['gr_ch_sh'] = gr_ch_sh
        context['group'] = group
        context['dance_style'] = dance_style
        context['weekdays'] = weekdays
        context['class_schedule'] = class_schedule
        return context


# МОЯ СТРАНИЦА ХОРЕОГРАФА
class MyPageChoreographer(TemplateView):
    template_name = 'my_page_choreographer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        choreographer = Choreographer.objects.get(user=logged_user)
        context['logged_user'] = logged_user
        context['choreographer'] = choreographer

        # Объявления
        announcements = Announcement.objects.all()
        context['announcements'] = announcements

        # Расписание для хореографа
        gr_ch_sh = GroupChoreographerSchedule.objects.filter(choreographer=choreographer)
        group = Group.objects.all().order_by('num')
        dance_style = DanceStyle.objects.all()
        weekdays = WeekDay.objects.all()
        class_schedule = ClassSchedule.objects.all().order_by('begin_time')
        context['gr_ch_sh'] = gr_ch_sh
        context['group'] = group
        context['dance_style'] = dance_style
        context['weekdays'] = weekdays
        context['class_schedule'] = class_schedule

        # Костюмы
        costumes = Costume.objects.all().order_by('dance')
        dances = Dance.objects.all().order_by('name')
        participant_costumes = ParticipantCostume.objects.all().order_by('participant')
        participants = Participant.objects.all().order_by('group', 'last_name')
        context['costumes'] = costumes
        context['dances'] = dances
        context['participants'] = participants
        context['participant_costumes'] = participant_costumes

        # Платежи
        payments = Payment.objects.all().order_by('participant')
        months = Month.objects.all()
        context['payments'] = payments
        context['months'] = months

        # Фонд
        fonds = Fond.objects.all().order_by('sum', 'participant')
        context['fonds'] = fonds
        fond = 0
        for f in fonds:
            fond += f.sum
        context['fond'] = fond

        total = 0
        for f in fonds:
            total += 7000
        context['total'] = total

        # Другие источники финансов
        other_sources = OtherSourceOfFinances.objects.all()
        context['other_sources'] = other_sources
        final_other_sources = 0
        for o in other_sources:
            final_other_sources += o.sum
        context['final_other_sources'] = final_other_sources
        fond_and_other = fond + final_other_sources
        context['fond_and_other'] = fond_and_other

        # Затраты
        expences = Expence.objects.all()
        context['expences'] = expences
        final_expences = 0
        fond_final = fond_and_other
        for e in expences:
            if e.bought == False:
                final_expences += e.final_cost()
            else:
                fond_final -= e.final_cost()
        context['fond_final'] = fond_final
        context['final_expences'] = final_expences

        # Участник-танец-концерт
        d_c = DanceInConcert.objects.all().order_by('concert')
        p_d_c = ParticipantDanceConcert.objects.all()
        dances = Dance.objects.all().order_by('name')
        concerts = Concert.objects.all().order_by('-begin_date')
        p_c = ParticipantConcert.objects.all()
        today = date.today()
        context['today'] = today
        context['d_c'] = d_c
        context['dances'] = dances
        context['concerts'] = concerts
        context['p_c'] = p_c
        context['p_d_c'] = p_d_c

        groups = Group.objects.all()
        p_g = ParticipantGroup.objects.all()
        context['groups'] = groups
        context['participant_group'] = p_g

        # Направления
        dance_styles = DanceStyle.objects.all()
        context['dance_styles'] = dance_styles

        return context


# МОЯ СТРАНИЦА УЧАСТНИКА
class MyPageParticipant(TemplateView):
    template_name = 'my_page_participant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        participant = Participant.objects.get(user=logged_user)
        context['logged_user'] = logged_user
        context['participant'] = participant

        # Объявления
        announcements = Announcement.objects.all()
        context['announcements'] = announcements
        now = timezone.now()
        context['now'] = now

        # Расписание для участника
        gr_ch_sh = GroupChoreographerSchedule.objects.filter(group=participant.group)
        group = Group.objects.filter(id=participant.group.id)
        dance_style = DanceStyle.objects.all()
        weekdays = WeekDay.objects.all()
        class_schedule = ClassSchedule.objects.all()
        context['gr_ch_sh'] = gr_ch_sh
        context['group'] = group
        context['dance_style'] = dance_style
        context['weekdays'] = weekdays
        context['class_schedule'] = class_schedule

        #  Список танцев концертов для участника
        concerts = Concert.objects.all()
        p_c = ParticipantConcert.objects.all().filter(participant=participant)
        d_c = DanceInConcert.objects.all().order_by('num')
        p_d_c = ParticipantDanceConcert.objects.all()
        dances = Dance.objects.all().order_by('name')
        today = date.today()
        context['today'] = today
        context['d_c'] = d_c
        context['dances'] = dances
        context['concerts'] = concerts
        context['p_c'] = p_c
        context['p_d_c'] = p_d_c

        # Контакты преподавателей
        choreographers = Choreographer.objects.all()
        context['choreographers'] = choreographers

        # Костюмы к сдаче
        costumes = Costume.objects.all().order_by('dance')
        participant_costumes = ParticipantCostume.objects.filter(participant=participant)
        context['costumes'] = costumes
        context['participant_costumes'] = participant_costumes

        # Платежи
        payments = Payment.objects.filter(participant=participant)
        months = Month.objects.all()
        context['payments'] = payments
        context['months'] = months

        # Фонд
        fond = Fond.objects.get(participant=participant)
        context['fond'] = fond

        return context


# ГРАФИКИ
class Plots(TemplateView):
    template_name = 'plot.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Concert.objects.get(slug__iexact=slug)

        logged_user = self.request.user
        choreographer = Choreographer.objects.get(user=logged_user)
        context['logged_user'] = logged_user
        context['choreographer'] = choreographer

        participants = Participant.objects.all().order_by('group', 'last_name')
        context['participants'] = participants
        d_c = DanceInConcert.objects.all().order_by('concert')
        p_d_c = ParticipantDanceConcert.objects.all()
        dances = Dance.objects.all().order_by('name')
        concerts = Concert.objects.all().order_by('-begin_date')
        p_c = ParticipantConcert.objects.all()
        context['d_c'] = d_c
        context['dances'] = dances
        context['concerts'] = concerts
        context['p_c'] = p_c
        context['p_d_c'] = p_d_c
        context['c'] = c

        pdc_count = []
        parts = []
        zero = 0
        for p in participants:
            for pc in p_c:
                if pc.participant == p and pc.concert == c and p not in parts:
                    parts.append(p)
                    pdc_count.append([c, p, 0])

            for dc in d_c:
                for d in dances:
                    if d == dc.dance and dc.concert == c:
                        for pdc in p_d_c:
                            if pdc.participant_concert.participant == p and pdc.dance.dance == d and pdc.participant_concert.concert == pdc.dance.concert and pdc.under_question == False:
                                for i in pdc_count:
                                    if i[0] == c and i[1] == p:
                                        i[2] += 1

        # times = []
        # d_times = []
        # for p in parts:
        #     for dc in d_c:
        #         if dc.concert == c:
        #             d_times.append(dc)
        #     for d_time in d_times:
        #         for pdc in p_d_c:
        #             if d_time.dance == pdc.dance.dance and p == pdc.participant_concert.participant:
        #                 times.append(0)
        #             elif d_time.dance == pdc.dance.dance:
        #                 times.append(d_time.dance.duration)
        # context['times']=times

        context['pdc_count'] = pdc_count

        data_names = []
        data_values = []
        for i in pdc_count:
            data_names.append('{} {}'.format(i[1].last_name, i[1].initials()))
            data_values.append(i[2])
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 10})
        plt.title('Кол-во номеров у человека (без учета ?)', color='darkred')
        ax = plt.axes()
        ax.yaxis.grid(True, zorder=1, color='darkred')
        xs = range(len(data_names))
        plt.bar([x for x in xs], [d for d in data_values],
                width=0.2, color='indianred', alpha=1,
                zorder=2)
        plt.xticks(xs, data_names, color='darkred')
        fig.autofmt_xdate(rotation=25)
        fig.savefig('bars.png')
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        context['image_base64'] = image_base64

        return context


# КОНТАКТЫ
class ContactsView(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        # choreographer = Choreographer.objects.get(user=logged_user)

        try:
            choreographer = Choreographer.objects.get(user=logged_user)
        except Exception:
            choreographer = None
        try:
            participant = Participant.objects.get(user=logged_user)
        except Exception:
            participant = None

        context['logged_user'] = logged_user
        context['choreographer'] = choreographer
        context['participant'] = participant

        return context


# УСПЕШНАЯ РЕГИСТРАЦИЯ
class SuccessfulRegistrationView(TemplateView):
    template_name = "successfully_registered.html"


# КОНТАКТЫ
class ChoreographersView(TemplateView):
    template_name = "choreogaphers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        # choreographer = Choreographer.objects.get(user=logged_user)

        try:
            choreographer = Choreographer.objects.get(user=logged_user)
        except Exception:
            choreographer = None
        try:
            participant = Participant.objects.get(user=logged_user)
        except Exception:
            participant = None

        context['logged_user'] = logged_user
        context['choreographer'] = choreographer
        context['participant'] = participant

        return context


# О НАС
class AboutUsView(ContactsView):
    template_name = "about_us.html"


class TapDanceView(ContactsView):
    template_name = "tap_dance.html"


class RussianDanceView(ContactsView):
    template_name = "russian_dance.html"


class WorldDanceView(ContactsView):
    template_name = "world_dance.html"


class ModernDanceView(ContactsView):
    template_name = "modern_dance.html"


# КОНЦЕРТЫ
class ConcertsPage(TemplateView):
    template_name = 'concerts_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        try:
            choreographer = Choreographer.objects.get(user=logged_user)
        except Exception:
            choreographer = None
        try:
            participant = Participant.objects.get(user=logged_user)
        except Exception:
            participant = None

        context['logged_user'] = logged_user
        context['choreographer'] = choreographer
        context['participant'] = participant

        concerts = Concert.objects.all().order_by('-begin_date')
        # dances = Dance.objects.all()
        # d_c = DanceInConcert.objects.all().order_by('num')
        today = date.today()

        context['today'] = today
        context['concerts'] = concerts
        # context['dances'] = dances
        # context['dances_in_concert'] = d_c
        return context


# АВТОРИЗАЦИЯ
class LoginPageView(LoginView):
    template_name = "login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = reverse('login')
        return context

    def get_success_url(self):
        return reverse('main_page')


def logout_view(request):
    logout_then_login(request)
    return HttpResponseRedirect('/')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # form.avatar = request.FILES['avatar']
        is_val = form.is_valid()
        data = form.cleaned_data
        exists = User.objects.filter(email=data['email'])
        if exists:
            form.add_error('email', ['Такой email уже занят'])
            is_val = False
        if data['password'] != data['password2']:
            is_val = False
            form.add_error('password2', ['Пароли должны совпадать'])
        if User.objects.filter(username=data['username']).exists():
            form.add_error('username', ['Такой логин уже занят'])
            is_val = False
        if is_val:
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user.save()
            return HttpResponseRedirect('/success')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


# МИКСИНЫ


class NewObjectMixin:
    form = None
    template = None
    redirect_url = None

    def get(self, request):
        form1 = self.form()
        return render(request, self.template, {'form': form1})

    def post(self, request):
        bound_form = self.form(request.POST, request.FILES)

        errors = []
        if bound_form.is_valid():
            try:
                new = bound_form.save()
            except Exception:
                errors.append('Такой элемент уже существует')
            if not errors:
                return redirect(self.redirect_url)


        return render(request, self.template, context={'form': bound_form, 'errors':errors})


class UpdateMixin:
    model = None
    template = None
    redirect_url = None
    model_form = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, 'obj': obj})

    def post(self, request, slug):

        if self.model == Participant:
            logged_user = request.user
            try:
                Choreographer.objects.get(user=logged_user)
            except Exception:
                self.redirect_url = 'my_page_participant'
            try:
                Participant.objects.get(user=logged_user)
            except Exception:
                self.redirect_url = 'my_page_choreographer'

        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, request.FILES, instance=obj)
        errors = []
        if bound_form.is_valid():
            try:
                upd_obj = bound_form.save()
            except Exception:
                errors.append('Такой элемент уже существует')
            if not errors:
                return redirect(self.redirect_url)

        return render(request, self.template, context={'form': bound_form, 'obj': obj, 'errors':errors})


class DeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={'obj': obj, })

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))


# НОВОСТИ
class AddNews(NewObjectMixin, View):
    form = NewsForm
    template = 'new/new_news.html'
    redirect_url = 'main_page'


class NewsPage(View):
    # template_name = 'show_news.html'

    def get(self, request):
        logged_user = self.request.user
        # choreographer = Choreographer.objects.get(user=logged_user)

        try:
            choreographer = Choreographer.objects.get(user=logged_user)
        except Exception:
            choreographer = None
        try:
            participant = Participant.objects.get(user=logged_user)
        except Exception:
            participant = None

        news = News.objects.all().order_by('-date')
        paginator = Paginator(news, 10)
        page = request.GET.get('page')
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render(request, 'show_news.html',
                      context={'news': news, 'logged_user': logged_user, 'participant': participant,
                               'choreographer': choreographer})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     news = News.objects.all().order_by('-date')
    #     context['news'] = news
    #     return context


class OneNewsPage(TemplateView):
    template_name = 'one_news_main.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.get(slug__iexact=slug)
        context['news'] = news
        return context


class UpdateNews(UpdateMixin, View):
    model = News
    template = 'update/update_news.html'
    model_form = NewsForm
    redirect_url = 'main_page'


class DeleteNews(DeleteMixin, View):
    model = News
    template = 'delete/delete_news.html'
    redirect_url = 'main_page'


# КОНЦЕРТ
class AddConcert(NewObjectMixin, View):
    form = ConcertForm
    template = 'new/new_concert.html'
    redirect_url = 'my_page_choreographer'


#
#
# class ConcertPage(TemplateView):
#     template_name = 'show_concert.html'
#
#     def get_context_data(self, slug, **kwargs):
#         context = super().get_context_data(**kwargs)
#         concert = Concert.objects.get(slug__iexact=slug)
#         dances = Dance.objects.all()
#         d_c = DanceInConcert.objects.all().order_by('num')
#         context['concert'] = concert
#         context['dances'] = dances
#         context['dances_in_concert'] = d_c
#         return context


class UpdateConcert(UpdateMixin, View):
    model = Concert
    template = 'update/update_concert.html'
    model_form = ConcertForm
    redirect_url = 'my_page_choreographer'


class DeleteConcert(DeleteMixin, View):
    model = Concert
    template = 'delete/delete_concert.html'
    redirect_url = 'my_page_choreographer'


# ГРУППА
class AddGroup(NewObjectMixin, View):
    form = GroupForm
    template = 'new/new_group.html'
    redirect_url = 'my_page_choreographer'


# class GroupsPage(TemplateView):
#     template_name = 'show_groups.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         groups = Group.objects.all().order_by('ages')
#         participants = Participant.objects.all()
#         p_g = ParticipantGroup.objects.all()
#         context['groups'] = groups
#         context['participants'] = participants
#         context['participant_group'] = p_g
#         return context
#
#
# class GroupPage(TemplateView):
#     template_name = 'show_group.html'
#
#     def get_context_data(self, slug, **kwargs):
#         context = super().get_context_data(**kwargs)
#         group = Group.objects.get(slug__iexact=slug)
#         participants = Participant.objects.all()
#         p_g = ParticipantGroup.objects.all()
#         context['group'] = group
#         context['participants'] = participants
#         context['participant_group'] = p_g
#         return context


class UpdateGroup(UpdateMixin, View):
    model = Group
    template = 'update/update_group.html'
    model_form = GroupForm
    redirect_url = 'my_page_choreographer'


class DeleteGroup(DeleteMixin, View):
    model = Group
    template = 'delete/delete_group.html'
    redirect_url = 'my_page_choreographer'


# ФОТОГАЛЕРЕЯ
# ПОЧИНИТЬ!!!!!
class AddPhotoGallery(View):
    form = PhotoGalleryForm
    template = 'new/new_photo_gallery.html'
    redirect_url = 'photo_galleries'

    def get(self, request):
        form1 = self.form()
        return render(request, self.template, {'form': form1})

    def post(self, request):

        bound_form = self.form(request.POST)
        if bound_form.is_valid():
            pg = PhotoInGallery.objects.create(name=bound_form.cleaned_data['name'],
                                               description=bound_form.cleaned_data['description'])
            for f in request.FILES.getlist('photos'):
                data = f.read()  # Если файл целиком умещается в памяти
                photo = PhotoInGallery(gallery=pg)
                photo.picture.save(f.name, ContentFile(data))
                photo.save()
                return redirect('/')
        #
        # bound_form.save()
        #     return redirect('/')
        return render(request, self.template, context={'form': bound_form})


class PhotoGalleriesPage(TemplateView):
    template_name = 'show_photo_galleries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_galleries = PhotoGallery.objects.all()
        photo_in_gallery = PhotoInGallery.objects.all()
        context['photo_galleries'] = photo_galleries
        context['photo_in_gallery'] = photo_in_gallery
        return context


class PhotoGalleryPage(TemplateView):
    template_name = 'show_photo_gallery.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_gallery = PhotoGallery.objects.get(slug__iexact=slug)
        photo_in_gallery = PhotoInGallery.objects.all()
        context['photo_gallery'] = photo_gallery
        context['photo_in_gallery'] = photo_in_gallery
        return context


class UpdatePhotoGallery(UpdateMixin, View):
    model = PhotoGallery
    template = 'update/update_photo_gallery.html'
    model_form = PhotoGalleryForm
    redirect_url = 'photo_galleries'


class DeletePhotoGallery(DeleteMixin, View):
    model = PhotoGallery
    template = 'delete/delete_photo_gallery'
    redirect_url = 'photo_galleries'


# ФОТО
class AddPhotoInGallery(NewObjectMixin, View):
    form = PhotoInGalleryForm
    template = 'new/new_photo_in_gallery.html'
    redirect_url = 'photo_galleries'


# ТАНЦЕВАЛЬНЫЕ НАПРАВЛЕНИЯ
class AddDanceStyle(NewObjectMixin, View):
    form = DanceStyleForm
    template = 'new/new_dance_style.html'
    redirect_url = 'my_page_choreographer'


#
# class DanceStylesPage(TemplateView):
#     template_name = 'show_dance_styles.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dance_styles = DanceStyle.objects.all()
#         context['dance_styles'] = dance_styles
#         return context
#
#
# class DanceStylePage(TemplateView):
#     template_name = 'show_dance_style_main.html'
#
#     def get_context_data(self, slug, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dance_style = DanceStyle.objects.get(slug__iexact=slug)
#         context['dance_style'] = dance_style
#         return context


class UpdateDanceStyle(UpdateMixin, View):
    model = DanceStyle
    template = 'update/update_dance_style.html'
    model_form = DanceStyleForm
    redirect_url = 'my_page_choreographer'


class DeleteDanceStyle(DeleteMixin, View):
    model = DanceStyle
    template = 'delete/delete_dance_style.html'
    redirect_url = 'my_page_choreographer'


# ВРЕМЯ ЗАНЯТИЙ
class AddClassSchedule(NewObjectMixin, View):
    form = ClassScheduleForm
    template = 'new/new_class_schedule.html'
    redirect_url = 'schedule'


class ClassSchedulesPage(TemplateView):
    template_name = 'show_class_schedules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_schedules = ClassSchedule.objects.all().order_by('begin_time')
        context['class_schedules'] = class_schedules
        return context


class ClassSchedulePage(TemplateView):
    template_name = 'show_class_schedule.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        class_schedule = ClassSchedule.objects.get(slug__iexact=slug)
        context['class_schedule'] = class_schedule
        return context


class UpdateClassSchedule(UpdateMixin, View):
    model = ClassSchedule
    template = 'update/update_class_schedule.html'
    model_form = ClassScheduleForm
    redirect_url = 'schedule'


class DeleteClassSchedule(DeleteMixin, View):
    model = ClassSchedule
    template = 'delete_class_schedule.html'
    redirect_url = 'schedule'


# РАСПИСАНИЕ
class AddSchedule(NewObjectMixin, View):
    form = ScheduleForm
    template = 'new/new_schedule.html'
    redirect_url = 'schedule'


class SchedulePage(TemplateView):
    template_name = 'show_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gr_ch_sh = GroupChoreographerSchedule.objects.all().order_by('class_schedule__begin_time')
        group = Group.objects.all()
        dance_style = DanceStyle.objects.all()
        weekdays = WeekDay.objects.all()
        class_schedule = ClassSchedule.objects.all()
        context['gr_ch_sh'] = gr_ch_sh
        context['group'] = group
        context['dance_style'] = dance_style
        context['weekdays'] = weekdays
        context['class_schedule'] = class_schedule
        return context


class SchedulePartPage(TemplateView):
    template_name = 'show_schedule_part.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        gr_ch_sh = GroupChoreographerSchedule.objects.all()

        # gr_ch_sh = GroupChoreographerSchedule.objects.get(slug__iexact=slug)
        group = Group.objects.all()
        dance_style = DanceStyle.objects.all()
        weekdays = WeekDay.objects.all()
        class_schedule = ClassSchedule.objects.all()
        participant = Participant.objects.get(slug__iexact=slug)
        context['participant'] = participant
        context['gr_ch_sh'] = gr_ch_sh
        context['group'] = group
        context['dance_style'] = dance_style
        context['weekdays'] = weekdays
        context['class_schedule'] = class_schedule
        return context


class UpdateSchedulePart(UpdateMixin, View):
    model = GroupChoreographerSchedule
    template = 'update/update_schedule_part.html'
    model_form = ScheduleForm
    redirect_url = 'schedule'


class DeleteSchedulePart(DeleteMixin, View):
    model = GroupChoreographerSchedule
    template = 'delete/delete_schedule_part.html'
    redirect_url = 'schedule'


# ХОРЕОГРАФ
class AddChoreographer(NewObjectMixin, View):
    form = ChoreographerForm
    template = 'new/new_choreographer.html'
    redirect_url = 'schedule'


#
# class ChoreographersPage(TemplateView):
#     template_name = 'show_choreographers.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         choreographer = Choreographer.objects.all()
#         context['choreographer'] = choreographer
#         return context
#
#
# class ChoreographerPage(TemplateView):
#     template_name = 'show_choreographer.html'
#
#     def get_context_data(self, slug, **kwargs):
#         context = super().get_context_data(**kwargs)
#         choreographer = Choreographer.objects.get(slug__iexact=slug)
#         context['choreographer'] = choreographer
#         return context


class UpdateChoreographer(UpdateMixin, View):
    model = Choreographer
    template = 'update/update_choreographer.html'
    model_form = ChoreographerForm
    redirect_url = 'my_page_choreographer'


class DeleteChoreographer(DeleteMixin, View):
    model = Choreographer
    template = 'delete/delete_choreographer.html'
    redirect_url = 'main_page'


# УЧАСТНИКИ
class AddParticipant(NewObjectMixin, View):
    form = ParticipantForm
    template = 'new/new_participant.html'
    redirect_url = 'my_page_choreographer'


# class ParticipantsPage(TemplateView):
#     template_name = 'show_participants.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         groups = Group.objects.all()
#         participants = Participant.objects.all().order_by('last_name')
#         p_g = ParticipantGroup.objects.all()
#         context['groups'] = groups
#         context['participants'] = participants
#         context['participant_group'] = p_g
#         return context
#
#
# class ParticipantPage(TemplateView):
#     template_name = 'show_participant.html'
#
#     def get_context_data(self, slug, **kwargs):
#         context = super().get_context_data(**kwargs)
#         group = Group.objects.all()
#         participant = Participant.objects.get(slug__iexact=slug)
#         p_g = ParticipantGroup.objects.all()
#         context['group'] = group
#         context['participant'] = participant
#         # context['participant_group'] = p_g
#         return context


class UpdateParticipant(UpdateMixin, View):
    model = Participant
    template = 'update/update_participant.html'
    model_form = ParticipantForm
    # redirect_url = 'my_page_choreographer'


class DeleteParticipant(DeleteMixin, View):
    model = Participant
    template = 'delete/delete_participant.html'
    redirect_url = 'my_page_choreographer'


# ТАНЕЦ
class AddDance(NewObjectMixin, View):
    form = DanceForm
    template = 'new/new_dance.html'
    redirect_url = 'my_page_choreographer'


#
# class DancesPage(TemplateView):
#     template_name = 'show_dances.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dances = Dance.objects.all().order_by('name')
#         context['dances'] = dances
#         return context
#
#
# class DancePage(TemplateView):
#     template_name = 'show_dance.html'
#
#     def get_context_data(self, slug, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dance = Dance.objects.get(slug__iexact=slug)
#         context['dance'] = dance
#         return context


class UpdateDance(UpdateMixin, View):
    model = Dance
    template = 'update/update_dance.html'
    model_form = DanceForm
    redirect_url = 'my_page_choreographer'


class DeleteDance(DeleteMixin, View):
    model = Dance
    template = 'delete/delete_dance.html'
    redirect_url = 'my_page_choreographer'


# ТАНЕЦ В КОНЦЕРТЕ
class AddDanceInConcert(NewObjectMixin, View):
    form = DanceInConcertForm
    template = 'new/new_dance_in_concert.html'
    redirect_url = 'my_page_choreographer'


class UpdateDanceInConcert(UpdateMixin, View):
    model = DanceInConcert
    template = 'update/update_dance_in_concert.html'
    model_form = DanceInConcertForm
    redirect_url = 'my_page_choreographer'


class DeleteDanceInConcert(DeleteMixin, View):
    model = DanceInConcert
    template = 'delete/delete_dance_in_concert.html'
    redirect_url = 'my_page_choreographer'


# ТАНЕЦ УЧАСТНИК КОНЦЕРТ
class AddParticipantDanceConcert(NewObjectMixin, View):
    form = ParticipantDanceConcertForm
    template = 'new/new_participant_dance_concert.html'
    redirect_url = 'my_page_choreographer'

#
# class ParticipantDanceConcertPage(TemplateView):
#     template_name = 'show_participant_dance_concert.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         d_c = DanceInConcert.objects.all().order_by('num')
#         p_d_c = ParticipantDanceConcert.objects.all()
#         dances = Dance.objects.all()
#         concerts = Concert.objects.all()
#         participants = Participant.objects.all()
#         p_c = ParticipantConcert.objects.all()
#         context['d_c'] = d_c
#         context['dances'] = dances
#         context['concerts'] = concerts
#         context['participants'] = participants
#         context['p_c'] = p_c
#         context['p_d_c'] = p_d_c
#         return context


class UpdateParticipantDanceConcert(UpdateMixin, View):
    model = ParticipantDanceConcert
    template = 'update/update_participant_dance_concert.html'
    model_form = ParticipantDanceConcertForm
    redirect_url = 'my_page_choreographer'


class DeleteParticipantDanceConcert(DeleteMixin, View):
    model = ParticipantDanceConcert
    template = 'delete/delete_participant_dance_concert.html'
    redirect_url = 'my_page_choreographer'


# УЧАСТНИК КОНЦЕРТА
class AddParticipantConcert(NewObjectMixin, View):
    form = ParticipantConcertForm
    template = 'new/new_participant_concert.html'
    redirect_url = 'my_page_choreographer'


class ParticipantsConcertsPage(TemplateView):
    template_name = 'show_participants_concerts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_c = ParticipantConcert.objects.all()
        participants = Participant.objects.all()
        concerts = Concert.objects.all()
        context['p_c'] = p_c
        context['participants'] = participants
        context['concerts'] = concerts
        return context


class UpdateParticipantConcert(UpdateMixin, View):
    model = ParticipantConcert
    template = 'update/update_participant_concert.html'
    model_form = ParticipantConcertForm
    redirect_url = 'my_page_choreographer'


class DeleteParticipantConcert(DeleteMixin, View):
    model = ParticipantConcert
    template = 'delete/delete_participant_concert.html'
    redirect_url = 'my_page_choreographer'


# ФОНД
class AddFond(NewObjectMixin, View):
    form = FondForm
    template = 'new/new_fond.html'
    redirect_url = 'my_page_choreographer'


class FondsPage(TemplateView):
    template_name = 'show_fonds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fonds = Fond.objects.all().order_by('participant')
        context['fonds'] = fonds
        return context


class FondPage(TemplateView):
    template_name = 'show_fond.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        fond = Fond.objects.get(slug__iexact=slug)
        context['fond'] = fond
        return context


class UpdateFond(UpdateMixin, View):
    model = Fond
    template = 'update/update_fond.html'
    model_form = FondForm
    redirect_url = 'my_page_choreographer'


class DeleteFond(DeleteMixin, View):
    model = Fond
    template = 'delete/delete_fond.html'
    redirect_url = 'my_page_choreographer'


# ПЛАТЕЖ
class AddPayment(NewObjectMixin, View):
    form = PaymentForm
    template = 'new/new_payment.html'
    redirect_url = 'my_page_choreographer'


class PaymentsPage(TemplateView):
    template_name = 'show_payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payments = Payment.objects.all().order_by('participant')
        months = Month.objects.all()
        participants = Participant.objects.all()
        context['payments'] = payments
        context['months'] = months
        context['participants'] = participants
        return context


class PaymentPage(TemplateView):
    template_name = 'show_payment.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        payment = Payment.objects.get(slug__iexact=slug)
        context['payment'] = payment

        return context


class UpdatePayment(UpdateMixin, View):
    model = Payment
    template = 'update/update_payment.html'
    model_form = PaymentForm
    redirect_url = 'my_page_choreographer'


class DeletePayment(DeleteMixin, View):
    model = Payment
    template = 'delete/delete_payment.html'
    redirect_url = 'my_page_choreographer'


# КОСТЮМ
class AddCostume(NewObjectMixin, View):
    form = CostumeForm
    template = 'new/new_costume.html'
    redirect_url = 'my_page_choreographer'


#
# class CostumesPage(TemplateView):
#     template_name = 'show_costumes.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         costumes = Costume.objects.all().order_by('dance')
#         dances = Dance.objects.all()
#         participant_costumes = ParticipantCostume.objects.all().order_by('participant')
#         participants = Participant.objects.all()
#         context['costumes'] = costumes
#         context['dances'] = dances
#         context['participants'] = participants
#         context['participant_costumes'] = participant_costumes
#         return context
#
#
# class CostumePage(TemplateView):
#     template_name = 'show_costume.html'
#
#     def get_context_data(self, slug, **kwargs):
#         context = super().get_context_data(**kwargs)
#         costume = Costume.objects.get(slug__iexact=slug)
#         context['costume'] = costume
#
#         return context


class UpdateCostume(UpdateMixin, View):
    model = Costume
    template = 'update/update_costume.html'
    model_form = CostumeForm
    redirect_url = 'my_page_choreographer'


class DeleteCostume(DeleteMixin, View):
    model = Costume
    template = 'delete/delete_costume.html'
    redirect_url = 'my_page_choreographer'


# УЧАСТНИК КОСТЮМ
class AddParticipantCostume(NewObjectMixin, View):
    form = ParticipantCostumeForm
    template = 'new/new_participant_costume.html'
    redirect_url = 'my_page_choreographer'


class UpdateParticipantCostume(UpdateMixin, View):
    model = ParticipantCostume
    template = 'update/update_participant_costume.html'
    model_form = ParticipantCostumeForm
    redirect_url = 'my_page_choreographer'


class DeleteParticipantCostume(DeleteMixin, View):
    model = ParticipantCostume
    template = 'delete/delete_participant_costume.html'
    redirect_url = 'my_page_choreographer'


# ЗАТРАТЫ
class AddExpence(NewObjectMixin, View):
    form = ExpenceForm
    template = 'new/new_expence.html'
    redirect_url = 'my_page_choreographer'


class UpdateExpence(UpdateMixin, View):
    model = Expence
    template = 'update/update_expence.html'
    model_form = ExpenceForm
    redirect_url = 'my_page_choreographer'


class DeleteExpence(DeleteMixin, View):
    model = Expence
    template = 'delete/delete_expence.html'
    redirect_url = 'my_page_choreographer'


# ИСТОЧНИКИ ФИНАНСОВ
class AddOtherSourceOfFinance(NewObjectMixin, View):
    form = OtherSourceOfFinanceForm
    template = 'new/new_other_source.html'
    redirect_url = 'my_page_choreographer'


class UpdateOtherSourceOfFinance(UpdateMixin, View):
    model = OtherSourceOfFinances
    template = 'update/update_other_source.html'
    model_form = OtherSourceOfFinanceForm
    redirect_url = 'my_page_choreographer'


class DeleteOtherSourceOfFinance(DeleteMixin, View):
    model = OtherSourceOfFinances
    template = 'delete/delete_other_source.html'
    redirect_url = 'my_page_choreographer'



# ОБЪЯВЛЕНИЯ
class AddAnnouncement(NewObjectMixin, View):
    form = AnnouncementForm
    template = 'new/new_announcement.html'
    redirect_url = 'my_page_choreographer'


class UpdateAnnouncement(UpdateMixin, View):
    model = Announcement
    template = 'update/update_announcement.html'
    model_form = AnnouncementForm
    redirect_url = 'my_page_choreographer'


class DeleteAnnouncement(DeleteMixin, View):
    model = Announcement
    template = 'delete/delete_announcement.html'
    redirect_url = 'my_page_choreographer'
