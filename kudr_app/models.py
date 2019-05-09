from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.utils.text import slugify
from transliterate import translit, detect_language

User._meta.get_field('email')._unique = True

class Choreographer(models.Model):
    last_name = models.TextField(verbose_name="Фамилия", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    first_name = models.TextField(verbose_name="Имя", max_length=50)
    patronymic = models.TextField(verbose_name="Отчество", blank=True, max_length=50)
    phone = models.TextField(verbose_name="Номер телефона", blank=True, max_length=50)
    email = models.EmailField(max_length=50, unique=True, blank=True)
    picture = models.ImageField(upload_to='media/choreographers', null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=300)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name = 'Хореограф'
        verbose_name_plural = 'Хореографы'

    def initials(self):
        return '{}. {}.'.format(self.first_name[0:1].upper(), self.patronymic[0:1].upper())

    def get_absolute_url(self):
        return reverse('choreographer', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_choreographer', kwargs={'slug': self.slug})

    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)

    def save(self, *args, **kwargs):
        # if not self.id:
        a = '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)
        if detect_language(self.last_name) is not None or detect_language(self.first_name) is not None or detect_language(self.patronymic) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a,allow_unicode=True)
        super(Choreographer, self).save(*args, **kwargs)


class DanceStyle(models.Model):
    dance_style = models.TextField(verbose_name="Танцевальное направление", max_length=50)

    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    picture = models.ImageField(upload_to='media/dance_style', null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=10000)

    class Meta:
        verbose_name = 'Танцевальное направление'
        verbose_name_plural = 'Танцевальные направления'


    def __str__(self):
        return self.dance_style

    def get_absolute_url(self):
        return reverse('dance_style', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_dance_style', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if detect_language(self.dance_style) is not None:
            self.slug = slugify(translit(self.dance_style, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(self.dance_style)
        super(DanceStyle, self).save(*args, **kwargs)


class ChoreographerDanceStyle(models.Model):
    dance_style = models.ForeignKey(DanceStyle, on_delete=models.CASCADE)
    choreographer = models.ForeignKey(Choreographer, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.TextField(verbose_name="Название группы", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    ages = models.TextField(verbose_name="Возрастная категория", blank=True, max_length=50)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=300)
    payment = models.PositiveIntegerField(verbose_name="Сумма оплаты", blank=True, default=2000)
    num = models.PositiveIntegerField(verbose_name="Порядковый номер", blank=True, null=True)

    def __str__(self):
        return self.name

    def get_groups(self):
        return Group.objects.filter(item=self)

    def get_absolute_url(self):
        return reverse('group', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_group', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['num']

    def save(self, *args, **kwargs):

        if detect_language(self.name) is not None:
            self.slug = slugify(translit(self.name, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)


# УБРАТЬ КАСКАД ИЗ ЮЗЕРА
class Participant(models.Model):
    last_name = models.TextField(verbose_name="Фамилия", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    first_name = models.TextField(verbose_name="Имя", max_length=50)
    patronymic = models.TextField(verbose_name="Отчество", blank=True, max_length=50)
    phone = models.TextField(verbose_name="Номер телефона", blank=True, max_length=50)
    email = models.EmailField(verbose_name="Email", max_length=50, unique=True)
    picture = models.ImageField(upload_to='media/participants', null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    # gender = models.TextField(verbose_name="Пол", blank=True, max_length=50)

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    def __str__(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)

    def initials(self):
        return '{}. {}.'.format(self.first_name[0:1].upper(), self.patronymic[0:1].upper())

    # def get_absolute_url(self):
    #     return reverse('participant', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_participant', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        ordering = ['group', 'last_name', 'first_name', 'patronymic']

    def save(self, *args, **kwargs):
        a = '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)
        if detect_language(self.last_name) is not None or detect_language(
                self.first_name) is not None or detect_language(self.patronymic) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a)
        super(Participant, self).save(*args, **kwargs)


class ParticipantGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # ПОМЕНЯТЬ
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)


class WeekDay(models.Model):
    day_of_the_week = models.TextField(verbose_name="День недели", blank=True, max_length=50)

    def __str__(self):
        return self.day_of_the_week

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'



class ClassSchedule(models.Model):
    begin_time = models.TimeField(verbose_name="Время начала", null=True, max_length=50)
    end_time = models.TimeField(verbose_name="Время окончания", null=True, max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    address = models.TextField(verbose_name="Адрес", blank=True, max_length=350)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    def __str__(self):
        return '{} - {}'.format(self.begin_time, self.end_time)

    def get_absolute_url(self):
        return reverse('class_schedule', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_class_schedule', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Расписание класса'
        verbose_name_plural = 'Расписание классов'
        ordering = ['begin_time']

    def save(self, *args, **kwargs):
        a = '{} {}'.format(str(self.begin_time), str(self.end_time))
        self.slug = slugify(a)

        super(ClassSchedule, self).save(*args, **kwargs)


class GroupChoreographerSchedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    choreographer = models.ForeignKey(Choreographer, on_delete=models.CASCADE)
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    dance_style = models.ForeignKey(DanceStyle, on_delete=models.CASCADE)
    day_of_the_week = models.ForeignKey(WeekDay, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name="URL", max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('schedule_part', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_schedule_part', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
        ordering = ['group']

    def save(self, *args, **kwargs):
        a = '{} {} {} {} {}'.format(str(self.group), str(self.class_schedule), str(self.day_of_the_week),
                                    str(self.dance_style), str(self.choreographer))
        if detect_language(a) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a)
        super(GroupChoreographerSchedule, self).save(*args, **kwargs)


class Concert(models.Model):
    name = models.TextField(verbose_name="Название концерта", max_length=50, default="Концерт")
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    begin_date = models.DateField(verbose_name="Дата начала", null=True)
    end_date = models.DateField(verbose_name="Дата окончания", blank=True, null=True)
    begin_time = models.TimeField(verbose_name="Время начала", blank=True, null=True, max_length=50)
    end_time = models.TimeField(verbose_name="Время окончания", blank=True, null=True, max_length=50)
    place = models.TextField(verbose_name="Место проведения", blank=True, max_length=50)
    address = models.TextField(verbose_name="Адрес", blank=True, max_length=50)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    def __str__(self):
        return '{} {} {} {} - {}'.format(self.name, self.place, self.begin_date, self.begin_time, self.end_time)

    class Meta:
        verbose_name = 'Концерт'
        verbose_name_plural = 'Концерты'
        ordering = ['begin_date']

    def get_absolute_url(self):
        return reverse('concert', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_concert', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        a = '{} {} {}'.format(self.name, self.begin_date, self.begin_time)

        if detect_language(self.name) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a)
        super(Concert, self).save(*args, **kwargs)


class Dance(models.Model):
    name = models.TextField(verbose_name="Название танца", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)

    duration = models.TimeField(verbose_name="Длительность", blank=True)
    picture = models.ImageField(upload_to='media/dance', null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Танец'
        verbose_name_plural = 'Танцы'

    def get_absolute_url(self):
        return reverse('dance', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_dance', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if detect_language(self.name) is not None:
            self.slug = slugify(translit(self.name, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(self.name)

        super(Dance, self).save(*args, **kwargs)


class DanceInConcert(models.Model):
    dance = models.ForeignKey(Dance, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Порядковый номер танца в концерте", blank=True, null=True)
    slug = models.SlugField(verbose_name="URL", max_length=250, unique=True)

    # num_persons = models.PositiveIntegerField(verbose_name="Количество человек", blank=True)
    # description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    # def __str__(self):
    #     return '{} {} {}'.format( self.dance, self.concert)
    #

    # def get_absolute_url(self):
    #     return reverse('d', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_dance_in_concert', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Танец в концерте'
        verbose_name_plural = 'Танцы в концерте'
        ordering = ['concert']

    def __str__(self):
        return '{} {}'.format(self.concert, self.dance)

    def save(self, *args, **kwargs):

        a = '{} {}'.format(self.concert.slug, self.dance.slug)
        self.slug = slugify(a)
        super(DanceInConcert, self).save(*args, **kwargs)


class ParticipantConcert(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name="URL", max_length=250, unique=True)

    class Meta:
        verbose_name = 'Участник-концерт'
        verbose_name_plural = 'Участник-концерт'
        ordering = ['concert']

    def get_absolute_url(self):
        return reverse('participants_concert', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_participant_concert', kwargs={'slug': self.slug})

    def __str__(self):
        return '{} {}'.format(self.concert, self.participant)

    def save(self, *args, **kwargs):

        a = '{} {}'.format(self.concert.slug, self.participant.slug)
        self.slug = slugify(a)
        super(ParticipantConcert, self).save(*args, **kwargs)



class ParticipantDanceConcert(models.Model):
    participant_concert = models.ForeignKey(ParticipantConcert, on_delete=models.CASCADE)
    dance = models.ForeignKey(DanceInConcert, on_delete=models.CASCADE)
    under_question = models.BooleanField(default=False)
    slug = models.SlugField(verbose_name="URL", max_length=250, unique=True)

    # num = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    # participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    # dance = models.ForeignKey(Dance, on_delete=models.CASCADE)
    # concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse('participants_dances_concerts', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_participant_dance_concert', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Участник-танец-концерт'
        verbose_name_plural = 'Участник-танец-концерт'
        ordering = ['participant_concert']

    def __str__(self):
        return '{} {}'.format(self.participant_concert, self.dance)


    def save(self, *args, **kwargs):
        a = '{} {}'.format(self.participant_concert.slug, self.dance.slug)
        self.slug = slugify(a)
        super(ParticipantDanceConcert, self).save(*args, **kwargs)


class News(models.Model):
    title = models.TextField(verbose_name="Заголовок", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)

    text = models.TextField(verbose_name="Текст", blank=True, max_length=10000)
    picture = models.ImageField(upload_to='media/news', null=True, blank=True)
    date = models.DateTimeField(verbose_name="Дата", blank=True)

    # video = models.TextField(verbose_name="", blank=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.date)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['date']

    def get_absolute_url(self):
        return reverse('new', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_news', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        a = '{}{}'.format(self.title, str(self.date))

        if detect_language(self.title) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a)
        super(News, self).save(*args, **kwargs)


class PhotoGallery(models.Model):
    name = models.TextField(verbose_name="Название", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    main_picture = models.ImageField(upload_to='media/photo_gallery',default='media/default/photo/НОМЕР4.jpg')

    description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фотогалерея'
        verbose_name_plural = 'Фотогалереи'

    def get_absolute_url(self):
        return reverse('photo_gallery', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_photo_gallery', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):

        if detect_language(self.name) is not None:
            self.slug = slugify(translit(self.name, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(self.name)
        super(PhotoGallery, self).save(*args, **kwargs)


class PhotoInGallery(models.Model):
    name = models.TextField(verbose_name="Название", max_length=50)
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)

    picture = models.ImageField(upload_to='media/photo_gallery', null=True, blank=True)
    date = models.DateTimeField(verbose_name="Дата", blank=True)
    gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    # video = models.TextField(verbose_name="", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фотография в фотогалерее'
        verbose_name_plural = 'Фотографии в фотогалерее'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)

        super(PhotoInGallery, self).save(*args, **kwargs)


class Fond(models.Model):
    sum = models.PositiveIntegerField(verbose_name="Оплачено")
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)

    def percent(self):
        return int(self.sum*100/7000)

    def strpercent(self):
        return str(int(self.sum*100/7000))

    def __str__(self):
        return '{} {}'.format(self.participant, self.sum)

    class Meta:
        verbose_name = 'Фонд'
        verbose_name_plural = 'Фонд'
        ordering = ['sum','participant']

    def get_absolute_url(self):
        return reverse('fond', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_fond', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        a = '{} {}'.format(str(self.participant), self.sum)

        if detect_language(str(self.participant)) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a)
        super(Fond, self).save(*args, **kwargs)


class Month(models.Model):
    month = models.TextField(verbose_name="Месяц", blank=True, max_length=15)

    def __str__(self):
        return self.month

    class Meta:
        verbose_name = 'Месяц'
        verbose_name_plural = 'Месяцы'


class Payment(models.Model):
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(self.participant, self.month, self.participant.group.payment)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['month']

    def get_absolute_url(self):
        return reverse('payment', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_payment', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        a = '{} {} {}'.format(str(self.participant), str(self.month), str(self.participant.group.payment))

        if detect_language(str(self.participant)) is not None or detect_language(str(self.month)) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a)
        super(Payment, self).save(*args, **kwargs)


class Costume(models.Model):
    slug = models.SlugField(verbose_name="URL", max_length=50, unique=True)
    dance = models.ForeignKey(Dance, on_delete=models.CASCADE, blank=True)
    name = models.TextField(verbose_name="Название", max_length=50)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=50)

    # КОЛИЧЕСТВО
    # ОТМЕЧАТЬ СКОЛЬКО ЧЕЛОВЕК СДАЛИ

    def __str__(self):
        return '{} {}'.format(self.dance, self.name)

    class Meta:
        verbose_name = 'Элемент костюма'
        verbose_name_plural = 'Элементы костюма'
        ordering = ['dance']

    def get_absolute_url(self):
        return reverse('costume', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_costume', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        a = '{} {}'.format(str(self.dance), self.name)

        if detect_language(self.name) is not None and detect_language(str(self.dance)) is not None:
            self.slug = slugify(translit(a, reversed=True), allow_unicode=True)
        else:
            self.slug = slugify(a)
        super(Costume, self).save(*args, **kwargs)


class ParticipantCostume(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    costume = models.ForeignKey(Costume, on_delete=models.CASCADE)
    date_return_before = models.DateTimeField(verbose_name="Вернуть до", blank=True)
    returned = models.BooleanField(default=False)
    slug = models.SlugField(verbose_name="URL", max_length=250, unique=True)

    class Meta:
        verbose_name = 'Участник-костюм'
        verbose_name_plural = 'Участник-костюм'
        ordering = ['costume']

    def __str__(self):
        return '{} {} {}'.format(self.participant, self.costume, self.date_return_before)

    def get_update_url(self):
        return reverse('update_participant_costume', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        a = '{} {}'.format(self.participant.slug, self.costume.slug)
        self.slug = slugify(a)

        super(ParticipantCostume, self).save(*args, **kwargs)
