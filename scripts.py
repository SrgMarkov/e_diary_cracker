import random
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datacenter.models import Lesson, Schoolkid, Mark, Chastisement, Commendation


praise_phrases = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
                  'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
                  'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!',
                  'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
                  'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!',
                  'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!',
                  'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!',
                  'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
                  'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                  'Теперь у тебя точно все получится!']


def fix_marks(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
        while Mark.objects.filter(schoolkid=child, points__lt=4).count() != 0:
            marks = Mark.objects.filter(schoolkid=child, points__lt=4).first()
            marks.points = 5
            marks.save()
    except MultipleObjectsReturned as error:
        print(f'Ошибка при выполнении: {error}')
    except ObjectDoesNotExist as error:
        print(f'Ошибка при выполнении: {error}')


def remove_chastisements(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
        chastisement = Chastisement.objects.filter(schoolkid=child)
        chastisement.delete()
    except MultipleObjectsReturned as error:
        print(f'Ошибка при выполнении: {error}')
    except ObjectDoesNotExist as error:
        print(f'Ошибка при выполнении: {error}')


def create_commendation(schoolkid, lesson, year=6, group='А'):
    praised_lesson = Lesson.objects.filter(group_letter=group, year_of_study=int(year), subject__title=lesson)\
        .order_by('-date').first()
    if praised_lesson is None:
        return print('Название урока введено с ошибкой')
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
        Commendation.objects.create(text=random.choice(praise_phrases), created=praised_lesson.date, schoolkid=child,
                                    subject=praised_lesson.subject, teacher=praised_lesson.teacher)
    except MultipleObjectsReturned as error:
        print(f'Ошибка при выполнении: {error}')
    except ObjectDoesNotExist as error:
        print(f'Ошибка при выполнении: {error}')
