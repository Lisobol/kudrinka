from django import forms
from kudr_app.models import *
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm, UserChangeForm


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Повторите ввод')
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    # avatar = forms.ImageField(label='avatar',required=False)


class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=50, widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ParticipantForm(forms.ModelForm):
    class Meta(object):
        model = Participant
        fields = ['last_name', 'first_name', 'patronymic', 'phone', 'email',
                  'picture', 'birth_date', 'group', 'description']
        widgets = {
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'patronymic': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите отчество'}),
            'phone': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'birth_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату рождения'}),
            'picture': forms.FileInput(),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            'group': forms.RadioSelect(),
        }


class ChoreographerForm(forms.ModelForm):
    class Meta(object):
        model = Choreographer
        fields = ['last_name', 'first_name', 'patronymic', 'phone', 'email',
                  'picture', 'description']
        widgets = {
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'patronymic': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите отчество'}),
            'phone': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
            'picture': forms.FileInput(),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'})
        }


class DanceStyleForm(forms.ModelForm):
    class Meta(object):
        model = DanceStyle
        fields = ['dance_style', 'description']
        widgets = {

            'dance_style': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название стиля'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'})
        }


class GroupForm(forms.ModelForm):
    class Meta(object):
        model = Group
        fields = ['name', 'ages', 'description', 'num']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название группы'}),
            'ages': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите возрастную категорию'}),
            'num': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер группы по порядку'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'})
        }


class ScheduleForm(forms.ModelForm):
    class Meta(object):
        model = GroupChoreographerSchedule
        fields = ['group', 'choreographer', 'dance_style', 'day_of_the_week', 'begin_time', 'end_time', 'address',
                  'description']
        widgets = {
            'group': forms.RadioSelect(),
            'choreographer': forms.RadioSelect(),
            'dance_style': forms.RadioSelect(),
            'day_of_the_week': forms.RadioSelect(),
            'begin_time': forms.TimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите время начала'}),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите время окончания'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'})

        }


class DanceInConcertForm(forms.ModelForm):
    class Meta(object):
        model = DanceInConcert
        fields = ['dance', 'concert', 'num']
        widgets = {
            'dance': forms.RadioSelect(),
            'concert': forms.RadioSelect(),
            'num': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер танца в концерте'}),
        }


class ParticipantConcertForm(forms.ModelForm):
    class Meta(object):
        model = ParticipantConcert
        fields = ['participant', 'concert']
        widgets = {
            'participant': forms.RadioSelect(),
            'concert': forms.RadioSelect(),
        }


class ParticipantDanceConcertForm(forms.ModelForm):
    class Meta(object):
        model = ParticipantDanceConcert
        fields = ['participant_concert', 'dance', 'under_question']
        widgets = {
            'participant_concert': forms.RadioSelect(),
            'dance': forms.RadioSelect(),
        }


class ConcertForm(forms.ModelForm):
    class Meta(object):
        model = Concert
        fields = ['name', 'begin_date', 'end_date', 'begin_time', 'end_time',
                  'place', 'address', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название концерта'}),
            'begin_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату начала'}),
            'end_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату окончания'}),
            'begin_time': forms.TimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите время начала'}),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите время окончания'}),
            'place': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите место проведения'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'})
        }


class DanceForm(forms.ModelForm):
    class Meta(object):
        model = Dance
        fields = ['name', 'duration', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'duration': forms.TimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите длительность'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'})
        }


class NewsForm(forms.ModelForm):
    class Meta(object):
        model = News
        fields = ['title', 'text', 'picture', 'date']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'text': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите текст'}),
            'picture': forms.FileInput(),
            'date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату'}),
        }


class PhotoGalleryForm(forms.ModelForm):
    class Meta(object):
        model = PhotoGallery
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'})

        }


class PhotoInGalleryForm(forms.ModelForm):
    class Meta(object):
        model = PhotoInGallery
        fields = ['name', 'picture', 'date', 'gallery', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату'}),
            # picture': forms.FileInput(attrs={'multiple': True}),
            'picture': forms.FileInput(),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
            'gallery': forms.RadioSelect(),
        }


class FondForm(forms.ModelForm):
    class Meta(object):
        model = Fond
        fields = ['sum', 'participant','all_fonds_null']
        widgets = {
            'participant': forms.RadioSelect(),
            'all_fonds_null':forms.CheckboxInput(),
            'sum': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите сумму'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta(object):
        model = Payment
        fields = ['month', 'participant']
        widgets = {
            'month': forms.RadioSelect(),
            'participant': forms.RadioSelect(),
        }


class CostumeForm(forms.ModelForm):
    class Meta(object):
        model = Costume
        fields = ['dance', 'name', 'description']
        widgets = {
            'dance': forms.RadioSelect(),
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите описание'}),
        }


class ParticipantCostumeForm(forms.ModelForm):
    class Meta(object):
        model = ParticipantCostume
        fields = ['costume', 'participant', 'date_return_before', 'returned']
        widgets = {
            'date_return_before': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату, к которой необходимо вернуть'}),
            # picture': forms.FileInput(attrs={'multiple': True}),
            'returned': forms.CheckboxInput(),
            'costume': forms.RadioSelect(),
            'participant': forms.RadioSelect(),

        }


class ExpenceForm(forms.ModelForm):
    class Meta(object):
        model = Expence
        fields = ['name', 'num', 'cost', 'date', 'bought']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'num': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите количество'}),
            'cost': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите цену единицы'}),
            'date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату покупки'}),
            'bought': forms.CheckboxInput(),
        }


class OtherSourceOfFinanceForm(forms.ModelForm):
    class Meta(object):
        model = OtherSourceOfFinances
        fields = ['name', 'sum']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'sum': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите сумму'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta(object):
        model = Announcement
        fields = ['title', 'text', 'participant', 'date', 'date_until', 'group']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'text': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите текст'}),
            'date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату'}),
            'date_until': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите дату, до которой объявление актуально'}),
            'participant': forms.RadioSelect(),
            'group': forms.RadioSelect(),
        }
