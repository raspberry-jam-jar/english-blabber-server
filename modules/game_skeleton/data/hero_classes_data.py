HEROCLASS_DATA = [
    {
        'id': 1,
        'name': 'Студент',
        'parent_id': None,
        'capacity': 100,
        'is_draft': False,
        'skill_ids': [1, 2],
    },
    {
        'id': 2,
        'name': 'Бакалавр',
        'parent_id': 1,
        'capacity': 100,
        'is_draft': False,
        'skill_ids': [1, 2, 3],
    },
    {
        'id': 3,
        'name': 'Магистр',
        'parent_id': 2,
        'capacity': 100,
        'is_draft': False,
        'skill_ids': [1, 2, 3, 4],
    },
    {
        'id': 4,
        'name': 'Профессор',
        'parent_id': 3,
        'capacity': 100,
        'is_draft': False,
        'skill_ids': [1, 2, 3, 4, 5],
    },
]

HEROSKILL_DATA = [
    {
        'id': 1,
        'name': 'Копить баллы'
    },
    {
        'id': 2,
        'name': 'Обменивать баллы на доступные подарки'
    },
    {
        'id': 3,
        'name': 'Быть лидером факультета'
    },
    {
        'id': 4,
        'name': 'Решать за группу о групповом обмене баллов'
    },
    {
        'id': 5,
        'name': 'Делиться своими баллами с другими участниками'
    },
]
