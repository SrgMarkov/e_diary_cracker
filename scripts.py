import random
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


def get_child(schoolkid):
    return Schoolkid.objects.get(full_name__contains=schoolkid)


def get_error_description(error):
    print(f'Ошибка при выполнении: {error}')


def fix_marks(schoolkid):
    try:
        Mark.objects.filter(schoolkid=get_child(schoolkid), points__lt=4).update(points=5)
    except (Schoolkid.MultipleObjectsReturned, Schoolkid.DoesNotExist) as error:
        get_error_description(error)


def remove_chastisements(schoolkid):
    try:
        chastisement = Chastisement.objects.filter(schoolkid=get_child(schoolkid))
        chastisement.delete()
    except (Schoolkid.MultipleObjectsReturned, Schoolkid.DoesNotExist) as error:
        get_error_description(error)


def create_commendation(schoolkid, lesson, year=6, group='А'):
    praised_lesson = Lesson.objects.filter(group_letter=group, year_of_study=int(year), subject__title=lesson)\
        .order_by('-date').first()
    if praised_lesson is None:
        return print('Название урока введено с ошибкой')
    try:
        Commendation.objects.create(text=random.choice(praise_phrases), created=praised_lesson.date,
                                    schoolkid=get_child(schoolkid), subject=praised_lesson.subject,
                                    teacher=praised_lesson.teacher)
    except (Schoolkid.MultipleObjectsReturned, Schoolkid.DoesNotExist) as error:
        get_error_description(error)
