SKILL_DATA = [
    {
        'id': 1,
        'name': 'Communicative skill',
    },
    {
        'id': 2,
        'name': 'Growing skill',
        'description': 'Баллы начисляются за результаты тестирования'
    },
    {
        'id': 3,
        'name': 'Activity skill',
        'description': 'Баллы начисляются за активность на занятиях'
    },
    {
        'id': 4,
        'name': 'Vocabulary skill',
    },
    {
        'id': 5,
        'name': 'Search skill'
    },
    {
        'id': 6,
        'name': 'Social skill'
    },
    {
        'id': 7,
        'name': 'Visual skill'
    },
    {
        'id': 8,
        'name': 'Time skill'
    },
    {
        'id': 9,
        'name': 'Constant skill'
    },
    {
        'id': 10,
        'name': 'Development skill'
    },
]

RULE_DATA = [
    {
        'id': 1,
        'name': 'Активное использование английской речи '
                'по теме урока на занятии',
        'skill_id': 1
    },
    {
        'id': 2,
        'name': 'Участие в чате группы или факультета на английском языке',
        'skill_id': 1
    },
    {
        'id': 3,
        'name': 'Участие в разговорном клубе',
        'skill_id': 1
    },
    {
        'id': 4,
        'name': 'Прогресс от предыдущего теста',
        'skill_id': 2
    },
    {
        'id': 5,
        'name': 'Стабильный результат',
        'skill_id': 2
    },
    {
        'id': 6,
        'name': 'Участие в обсуждении по теме',
        'skill_id': 3
    },
    {
        'id': 7,
        'name': 'Выполнение всех заданий',
        'skill_id': 3
    },
    {
        'id': 8,
        'name': 'Вовлеченность в урок',
        'skill_id': 3
    },
    {
        'id': 9,
        'name': 'Изучение новых слов и внесение их в словарь '
                'не по теме урока (самостоятельное изучение)',
        'skill_id': 4
    },
    {
        'id': 10,
        'name': 'Самостоятельный поиск интересной информации '
                'на английском языке или на англоязычную тематику',
        'skill_id': 5
    },
    {
        'id': 11,
        'name': 'Публикация поста в соцсетях на английском языке '
                '(от 3 предложений)',
        'skill_id': 6
    },
    {
        'id': 12,
        'name': 'Просмотр фильма, сериала, видео на английском и '
                'пересказ краткий в чате группы или на уроке',
        'skill_id': 7
    },
    {
        'id': 13,
        'name': 'Самостоятельное чтение англоязычной литературы и '
                'краткий пересказ',
        'skill_id': 7
    },
    {
        'id': 14,
        'name': 'Пунктуальность',
        'skill_id': 8
    },
    {
        'id': 15,
        'name': 'Стабильная посещаемость (от 8 занятий без пропусков)',
        'skill_id': 9
    },
    {
        'id': 16,
        'name': 'Участие в факультативах',
        'skill_id': 10
    },
]

GRADATION_DATA = [
    {
        'name': 'Дети до 12 лет',
        'money': 2,
        'experience': 2,
        'rule_id': 1
    },
    {
        'name': 'Дети от 12 лет',
        'money': 1,
        'experience': 1,
        'rule_id': 1
    },
    {
        'name': 'Общение в чате на английском языке',
        'money': 0.5,
        'experience': 0.5,
        'rule_id': 2
    },
    {
        'name': 'Участие в разговорном клубе',
        'money': 2,
        'experience': 2,
        'rule_id': 3
    },
    {
        'name': 'Прогресс 5%',
        'money': 1,
        'experience': 1,
        'rule_id': 4
    },
    {
        'name': 'Прогресс 10%',
        'money': 2,
        'experience': 2,
        'rule_id': 4
    },
    {
        'name': 'Прогресс до 50%',
        'money': 3,
        'experience': 3,
        'rule_id': 4
    },
    {
        'name': 'Прогресс до 70%',
        'money': 4,
        'experience': 4,
        'rule_id': 4
    },
    {
        'name': 'Стабильный результат',
        'money': 0.5,
        'experience': 0.5,
        'rule_id': 5
    },
    {
        'name': 'Участие в обсуждении по теме',
        'money': 1,
        'experience': 1,
        'rule_id': 6
    },
    {
        'name': 'Выполнение всех заданий',
        'money': 1,
        'experience': 1,
        'rule_id': 7
    },
    {
        'name': 'Вовлеченность в урок',
        'money': 1,
        'experience': 1,
        'rule_id': 8
    },
    {
        'name': 'Изучение новых слов',
        'money': 0.5,
        'experience': 0.5,
        'rule_id': 9
    },
    {
        'name': 'Самостоятельный поиск интересной информации',
        'money': 1.5,
        'experience': 1.5,
        'rule_id': 10
    },
    {
        'name': 'Публикация поста в соцсетях на 1 балл',
        'money': 1,
        'experience': 1,
        'rule_id': 11
    },
    {
        'name': 'Публикация поста в соцсетях на 2 балла',
        'money': 2,
        'experience': 2,
        'rule_id': 11
    },
    {
        'name': 'Публикация поста в соцсетях на 3 балла',
        'money': 3,
        'experience': 3,
        'rule_id': 11
    },
    {
        'name': 'Просмотр фильма, сериала, видео на английском',
        'money': 3,
        'experience': 3,
        'rule_id': 12
    },
    {
        'name': 'Самостоятельное чтение англоязычной литературы',
        'money': 3,
        'experience': 3,
        'rule_id': 13
    },
    {
        'name': 'Пунктуальность',
        'money': 0.5,
        'experience':  0.5,
        'rule_id': 14
    },
    {
        'name': 'Стабильная посещаемость',
        'money': 3,
        'experience': 3,
        'rule_id': 15
    },
    {
        'name': 'Участие в факультативах',
        'money': 2,
        'experience': 2,
        'rule_id': 16
    },
]

PENALTY_DATA = [
    {
        'name': 'Пропуск теста без уважительной причины',
        'experience': 4
    },
    {
        'name': 'Отсутствие активности на занятии и плохое поведение',
        'experience': 1
    },
    {
        'name': 'Опоздание на занятие от 5-10 минут',
        'experience': 1
    },
    {
        'name': 'Отсутствие выполненного домашнего задания',
        'experience': 1
    },
]
