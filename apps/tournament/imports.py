import gspread
import logging
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from oauth2client.service_account import ServiceAccountCredentials
from .messages import *
from .models import Tournament, User
from .consts import ROLE_MEMBER
from .models import Team


class TeamImportForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'form-elem__input',
        'placeholder': 'Скопируйте ссылку из адресной строки браузера'
    }), label=MSG_TEAM_URL)
    team_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-elem__input',
        'placeholder': 'Скопируйте текст c названием колонки из ячейки таблицы'
    }), label=MSG_TEAM_NAME)

    speaker_1_email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-elem__input',
        'placeholder': 'Скопируйте текст c названием колонки из ячейки таблицы'
    }), label=MSG_S1_EMAIL)
    speaker_1_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-elem__input',
        'placeholder': 'Скопируйте текст c названием колонки из ячейки таблицы'
    }), label=MSG_S1_NAME)

    speaker_2_email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-elem__input',
        'placeholder': 'Скопируйте текст c названием колонки из ячейки таблицы'
    }), label=MSG_S2_EMAIL)
    speaker_2_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-elem__input',
        'placeholder': 'Скопируйте текст c названием колонки из ячейки таблицы'
    }), label=MSG_S2_NAME)


class ImportTeam:

    NUMBER_TITLE_ROW = 1

    # IMPORT STATUS
    STATUS_ADD = 'add'
    STATUS_EXIST = 'exist'
    STATUS_FAIL = 'error'

    def __init__(self, import_form: TeamImportForm):
        self.url = import_form.cleaned_data['url']
        self.alias = {
            MSG_TEAM_NAME: import_form.cleaned_data['team_name'],
            MSG_S1_NAME: import_form.cleaned_data['speaker_1_name'],
            MSG_S1_EMAIL: import_form.cleaned_data['speaker_1_email'],
            MSG_S2_NAME: import_form.cleaned_data['speaker_2_name'],
            MSG_S2_EMAIL: import_form.cleaned_data['speaker_2_email'],
        }
        self.worksheet = None
        self.cells = {}
        self.results = []

    def connect_to_worksheet(self):
        try:
            from DebatesTournament.settings.google_import import SCOPE, GOOGLE_IMPORT_SETTINGS_FILE
            credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_IMPORT_SETTINGS_FILE, SCOPE)
            self.worksheet = gspread.authorize(credentials).open_by_url(self.url).sheet1

        except gspread.SpreadsheetNotFound:
            raise Exception('Не найти документ. Проверьте правильность URL и настройки доступа')

        except Exception as exception:
            logging.error(str(exception))
            raise Exception('Неудалось скачать файл')

    def read_titles(self):
        for key in self.alias.keys():
            try:
                self.cells[key] = self.worksheet.find(self.alias[key])
            except gspread.CellNotFound:
                raise Exception('Поле "%s" не найдено' % self.alias[key])

            if self.cells[key].row != self.NUMBER_TITLE_ROW:
                raise Exception('Поле "%s" должно быть заголовком колонки' % self.alias[key])

    def import_teams(self, tournament: Tournament, is_test):
        for row in self.worksheet.get_all_values()[self.NUMBER_TITLE_ROW:]:
            result = {}
            user_1 = None
            user_2 = None
            try:
                result['s1'] = {}
                result['s1']['user'] = None
                result['s1']['email'] = row[self.cells[MSG_S1_EMAIL].col - 1].strip()
                result['s1']['status'], user_1 = ImportTeam.import_user(
                    result['s1']['email'],
                    row[self.cells[MSG_S1_NAME].col - 1],
                    tournament,
                    is_test
                )
            except Exception as ex:
                result['s1']['status'] = self.STATUS_FAIL
                result['s1']['error'] = str(ex)

            try:
                result['s2'] = {}
                result['s2']['user'] = None
                result['s2']['email'] = row[self.cells[MSG_S2_EMAIL].col - 1].strip()
                result['s2']['status'], user_2 = ImportTeam.import_user(
                    result['s2']['email'],
                    row[self.cells[MSG_S2_NAME].col - 1],
                    tournament,
                    is_test
                )
            except Exception as ex:
                result['s2']['status'] = self.STATUS_FAIL
                result['s2']['error'] = str(ex)

            try:
                result['team'] = {}
                result['team']['name'] = row[self.cells[MSG_TEAM_NAME].col - 1].strip()
                if not result['team']['name']:
                    raise Exception('Название команды не должно быть пустым')

                if result['s1']['status'] == self.STATUS_FAIL:
                    raise Exception('Ошибка при импорте первого спикера')

                result['s1']['user'] = user_1

                if result['s2']['status'] == self.STATUS_FAIL:
                    raise Exception('Ошибка при импорте второго спикера')

                result['s2']['user'] = user_2

                teams = tournament.team_members.filter(name=result['team']['name'])
                if teams:
                    result['team']['status'] = ImportTeam.STATUS_FAIL
                    result['team']['error'] = 'Команда с таким же названием уже участвует в турнире'
                    for team in teams:
                        speakers = [team.speaker_1, team.speaker_2]
                        if user_1 in speakers and user_2 in speakers:
                            result['team']['status'] = ImportTeam.STATUS_EXIST
                            result['team']['error'] = ''
                            break

                else:
                    if not is_test:
                        tournament.teamtournamentrel_set.create(
                            role=ROLE_MEMBER,
                            team=Team.objects.create(
                                name=result['team']['name'],
                                speaker_1=user_1,
                                speaker_2=user_2,
                                info='Импортирована из Google Docs'
                            )
                        )
                    result['team']['status'] = ImportTeam.STATUS_ADD
            except Exception as ex:
                result['team']['status'] = self.STATUS_FAIL
                result['team']['error'] = str(ex)

            self.results.append(result)

        return self.results

    @staticmethod
    def check_email(email: str):
        try:
            validate_email(email)
        except ValidationError:
            raise Exception('Неверный e-mail')

    @staticmethod
    def import_user(email: str, full_name: str, tournament: Tournament, is_test: bool):
        ImportTeam.check_email(email)
        user, is_exist = User.get_or_create(email, full_name, is_test)

        status = ImportTeam.STATUS_EXIST
        if not is_exist:
            status = ImportTeam.STATUS_ADD
            if not is_test:
                password = user.set_random_password()
                user.send_email_about_import(tournament, password)

        return status, user
