import random
from yes_no_answer import YES, NO, CUTE, UNCUTE


# make_response просто записывает в response наш текст и передает его в ответ
def make_response(text: str, session_state=None):
    if session_state is None:
        session_state = {}
    return {
        'response': {
            'text': f'Осталось денег: {session_state["current_money"]} \n {text}',
        },
        'session_state': session_state,
        'version': '1.0'
    }


# основной обработчик
def handler(event, context):  # в JSON ответе ищем конкретный элемент списка и работаем с ним
    session_state = event['state']['session']
    if 'user_state' not in session_state:
        session_state['user_state'] = ''
    user_state = session_state['user_state']

    if event['session']['new']:
        session_state['current_money'] = 10000
        session_state['salary'] = 0
        session_state['goal'] = '1000050000'
        return welcome_message(event, session_state)

    if 'помощь' in event['request']['original_utterance'].lower() or 'что ты умеешь' in event['request'][
        'original_utterance'].lower():
        return help_message(session_state)

    if 'уволить' in event['request']['original_utterance'].lower():
        session_state['user_state'] = 'work_or_student'
        session_state['salary'] = 0
        return make_unemployed(event, session_state)

    if event['session']['new'] is False:
        current_money = int(session_state['current_money'])
        increaser_point = int(session_state['salary'])
        current_money += increaser_point
        goal = int(session_state['goal'])
        if current_money <= 0:
            return make_response('Кажется, у вас закончились деньги', session_state)
        if current_money >= goal:
            return make_response('''ВЫ НАКОПИЛИ НА СВОЮ МЕЧТУ. Теперь вы можете выийти из навыка, сказав ХВАТИТ. Увидимся!''', session_state)
        current_money -= 1000
        session_state.update({'current_money': str(current_money)})

    if 'ask_name' in user_state:
        return ask_name(event, session_state)
    elif 'show_rules' in user_state:
        return show_rules(event, session_state)
    elif 'ask_goal' in user_state:
        return ask_goal(event, session_state)
    elif 'work_or_student' in user_state:
        return work_or_student(event, session_state)
    elif 'work' in user_state:
        return work(event, session_state)
    elif 'student' in user_state:
        return student(event, session_state)
    elif 'programmer' in user_state:
        return programmer(event, session_state)
    elif 'writ' in user_state:
        return writ(event, session_state)
    elif 'arch' in user_state:
        return arch(event, session_state)
    elif 'doct' in user_state:
        return doct(event, session_state)
    elif 'polit' in user_state:
        return polit(event, session_state)
    elif 'teach' in user_state:
        return teach(event, session_state)
    else:
        return make_response('Ожидайте это в следующей версии', session_state)


def help_message(session_state):
    text = f"""Вам только исполнилось 18, вы человек из небогатой семьи, но вдруг решаете изменить свою жизнь и переехать в Москву. 
Приехав в столицу, вы обнаруживаете, что потеряли почти все ваши деньги. 
Ваша цель:{session_state["goal"]}, \n Ваш бюджет: {session_state["current_money"]}
Так же в любой момент вы можете вызвать панель меню и совершить действие, наподобие открытие бизнеса, 
поступление в вуз и тому подобное."""
    return make_response(text, session_state)


def welcome_message(event, session_state):
    text = 'Привет, друг! Ты попал в супер интересную профориентационную игру "Из грязи в князи", где вы можете ставить себе цели и достигать их. Как тебя зовут?'
    session_state['user_state'] = 'ask_name'
    return make_response(text, session_state)


def ask_name(event, session_state):
    session_state['user_name'] = event['request']['original_utterance']
    text = f'Очень приятно, {session_state["user_name"]} \n Нужно ли тебе озвучить правила?'
    session_state['user_state'] = 'show_rules'
    return make_response(text, session_state)


def show_rules(event, session_state):
    text = ''
    if event['request']['original_utterance'].lower() in YES:
        text = '''Вам только исполнилось 18, вы человек из небогатой семьи, но вдруг решаете изменить свою жизнь и переехать в Москву. 
                Приехав в столицу, вы обнаруживаете, что потеряли почти все ваши деньги. 
                Теперь вам предстоит осуществить все ваши цели в Москве с самого нуля.
                Так же в любой момент вы можете вызвать панель меню и совершить действие, наподобие открытие бизнеса, 
                поступление в вуз и тому подобное. '''
    text += ''' \n  Сколько вы хотите заработать (не менее 500000 и не более 20000000 рублей)?'''
    session_state['user_state'] = 'ask_goal'
    return make_response(text, session_state)


def ask_goal(event, session_state):
    c = event['request']['nlu']['entities']
    try:
        c = c[0]
    except IndexError:
        bag = ['Так-с, затрудняюсь ответить', 'Ой-ой, боюсь, что я вас не расслышала, повторите, пожалуйста',
               'Простите, я вас не поняла. Повторите, пожалуйста', 'Я не расслышала, повторите, пожалуйста']
        text = random.choice(bag)
        return make_response(text, session_state)

    if c.get('type') != 'YANDEX.NUMBER':
        bag = ['Так-с, затрудняюсь ответить', 'Ой-ой, боюсь, что я вас не расслышала, повторите, пожалуйста',
               'Простите, я вас не поняла. Повторите, пожалуйста', 'Я не расслышала, повторите, пожалуйста']
        text = random.choice(bag)
        return make_response(text, session_state)
    elif c['value'] > 20000000:
        text = 'Боюсь, сумма слишком большая, выберите до 20000000'
        return make_response(text, session_state)
    elif c['value'] < 500000:
        text = 'Вы себя не дооцениваете, выберете сумму более 500000'
        return make_response(text, session_state)
    else:
        text = 'Отлично!'
        session_state['goal'] = c['value']
        session_state['user_state'] = 'work_or_student'
        text += '''\n\nВы можете устроиться на работу с маленькой зарплатой сейчас, или пойти учиться, но для этого вам нужно
будет сдать вступительный экзамен.'''
        return make_response(text, session_state)

def make_unemployed(event, session_state):
    text = '''Вы успешно уволились с работы. Теперь вы снова можете устроиться на работу с маленькой 
    зарплатой сейчас, или пойти учиться'''
    return make_response(text, session_state)

def work_or_student(event, session_state):
    answer = event['request']['original_utterance'].lower()
    if 'работ' in answer or 'професс' in answer:
        session_state['user_state'] = 'work'
        if 'work' not in session_state:
            text = '''Работа? Ну что ж. Кем же вы тогда хотите работать?
        Дворник? Продавец? Уборщица? Консультант? А может охранник в школе? Или же доставщик пиццы?'''
        else:
            text = 'Вы пошли на работу'
        return make_response(text, session_state)
    if 'уч' in answer:
        session_state['user_state'] = 'student'
        text = '''Учёба? Хм, очень интересно. На кого же вы собираетесь поступать?
Программист? Архитектор? Журналист? Врач? Юрист? Или преподаватель?'''
        return make_response(text, session_state)
    bag = ['Так-с, затрудняюсь ответить', 'Ой-ой, боюсь, что я вас не расслышала, повторите, пожалуйста',
           'Простите, я вас не поняла. Повторите, пожалуйста', 'Я не расслышала, повторите, пожалуйста']
    text = random.choice(bag)
    return make_response(text, session_state)


def work(event, session_state):
    answer = event['request']['original_utterance'].lower()
    if 'двор' in answer:
        session_state['profession'] = 'janitor'
        session_state['salary'] = 1000000
        text = '''Работёнка не для лентяев, но вот зарплата всего 10000. Хотя на первое время хватит. Теперь вы можете уволиться и пойти учиться или выбрать себе новую работу.'''
        return make_response(text, session_state)
    if 'охран' in answer:
        session_state['profession'] = 'security'
        session_state['salary'] = 15000
        text = '''Непростая работка, даже слегка опасная. Зарплата 15000. Вполне неплохо для начала! Теперь вы можете уволиться и пойти учиться или выбрать себе новую работу.'''
        return make_response(text, session_state)
    if 'прод' in answer:
        session_state['profession'] = 'seller'
        session_state['salary'] = 15000
        text = '''Совсем неплохо для начала! Ваша зарплата 15000. Как знать, может это станет началом карьеры вашей мечты. Теперь вы можете уволиться и пойти учиться или выбрать себе новую работу.'''
        return make_response(text, session_state)
    if 'убор' in answer:
        session_state['profession'] = 'cleaner'
        session_state['salary'] = 8000
        text = '''Нехило! Что ж. Зарплата твоя всего 8000 рублей. Но и на эти деньги жить можно. Теперь вы можете уволиться и пойти учиться или выбрать себе новую работу.'''
        return make_response(text, session_state)
    if 'консультант' in answer:
        session_state['profession'] = 'consultant'
        session_state['salary'] = 9000
        text = '''Консультанты - люди добрые. Думаю, вам подходит. Ваша зарплат 9000. Есть к чему стремиться! Теперь вы можете уволиться и пойти учиться или выбрать себе новую работу.'''
        return make_response(text, session_state)
    if 'доставщик' in answer:
        session_state['profession'] = 'consultant'
        session_state['salary'] = 25000
        text = '''Кто не любит пиццу? У доставщика пиццы её полно! Да и зарплата у них неплохая: 25000! Это же работа мечты! Теперь вы можете уволиться и пойти учиться или выбрать себе новую работу.'''
        return make_response(text, session_state)

def student(event, session_state):
    answer = event['request']['original_utterance'].lower()
    agreement = False
    cute = ['Отличный выбор! Но тебе нужно ответить на один вопрос, чтобы поступить в вуз!',
            'Да ты, видимо, очень отважный! Чтобы поступить в университет ответь правильно на вопрос!',
            'Ого! Просто фантастика! Ну что ж. Сначала сдай экзамен, ответив на вопрос!',
            'Это здорово! Сдай экзамен, и станешь на шаг ближе к карьере твоей мечты.',
            'Похоже, у вас стальная нервная система, раз вы решаетесь на это. Ну хорошо! '
            'Ответьте на один несложный вопрос, чтобы поступить в вуз!']

    writ = ['Кликбейт - это кнопка на печатной машинке?',
            'Все печатные издания были изумлены красотой Мэрилин Монро?',
            'Как расшифровывается СМИ?',
            'Сколько томов в Войне и Мир?',
            'Владимир Маяковский был футуристом?',
            'Есенин был скромным человеком?',
            'Цветаева просила называть себя поэтессой?',
            'Поэтом каково века был Пушкин?',
            'Какое самое популярное СМИ в мире?',
            'У кого больше словарный запас у Пушкина или у Толстого?',
            'Кто является автором произаедения "Анна Каренина"?']
    arch = ['Правда ли что Эйфелева башня не была снесена потому '
            'что с её помощью был проведен первый сеанс телеграфной связи, а позднее размещены радиостанции.',
            'Правда ли что больше всего мостов в Гамбурге?',
            'Архитектурное понятие «мьюз» означает: Гипсовый материал, используемый для создания барельефов или '
            'Ряд малоэтажных домов с гаражами, способ застройки «деревня в городе»?',
            'Архитектурный ордер - это... Тип композиции, использующий определенные элементы и подчиняющийся '
            'определенному стилю или Документ, подтверждающий, что здание прошло соответствующие проверки и может '
            'быть использовано в разных целях',
            'Самой ценной наградой в сфере архитектуры является Притцкеровская премия или Премия Сакураи?',
            'Архитектура неперсонифицированная - Народная архитектура или Коллективное творчество нескольких авторов',
            'Что такое портик? Нижний этаж жилого дома, имеющий хозяйственное назначение или '
            'Невысокая ограждающая стенка или перила.',
            'Анфилада - ряд последовательно примыкающих друг к другу помещений, дверные проемы которых расположены '
            'на одной оси?']
    polit = ['Удовлетворение потребностей является основой деятельности людей?',
             'Социальные классы общества отличаются возрастом?',
             'Отличие человека от животных заключается в умении изготовлять и использовать орудия труда?',
             'Детство - это период в жизни человека с рождения до 11 лет?',
             'В РФ обязательно только 9-летнее образование?',
             'Продолжительность рабочего времени в неделю не должна превышать 40 часов?',
             'Общество - это  совокупность людей, '
             'объединившихся для общения и совместного выполнения какой-либо деятельности?',
             'Право - это допустимое поведение?',
             'Обязанность - это должное поведение?',
             'Стагнация - это развитие общества?']
    doct = ['Микология - это наука о бактериях?',
            'Могут ли лягушки жить в солёной воде?',
            'Белый медведь самый крупный в мире хищник?',
            'Саламандра является теплокровным животным?',
            'Верблюд запасает воду в крови?',
            'Что такое H2О?',
            'К какому классу позвоночных относится Человек?',
            'Кто был основоположником медицины?',
            'Где у кузнечика ухо?',
            'Какое животное суши самое быстрое?']
    program = ['Были ли мониторы у первых компьютеров?',
               'У компании Mac OC открытая файловая система на их устройствах или нет?',
               'Правда ли что чем меньше технический нанометровый процесс, тем лучше?',
               'Самый маленький ПК весил около 1 килограмма?',
               'Верно ли, что компьютер мощностью 1 терафлонепс обрабатывает 100 тысяч операций в секунду?',
               'Ccharp это язык кодового или блокового программирования?',
               'Python интерпретируемый или компилируемый язык программирования?',
               'For это цикл или условный оператор в языке Python?',
               'Переведите 3 в двоичную систему']
    teach = ['Если ты хочешь работать преподавателем тебе нужно получить высшее образование?',
             'Важно ли умение находить общий язык с детьми и поддерживать с ними хорошие отношения?',
             'Преподаватель важная профессия для нашего будущего?',
             'Эмоции ребенка и его переживания – это важные факторы. Вы согласны с этим?',
             'Как давно появилось понятие преподаватель?',
             'Чтобы преподавать в ВУЗЕ необходимо иметь высшее образование не ниже специалиста или магистра?']
    works = ['программ', "архитект", "журнал", "врач", "доктор", "юрист", "бизнес", "препод", 'учит']
    bag = ['Так-с, затрудняюсь ответить', 'Ой-ой, боюсь, что я вас не расслышала, повторите, пожалуйста',
           'Простите, я вас не поняла. Повторите, пожалуйста', 'Я не расслышала, повторите, пожалуйста']
    print('''Учёба? Хм, очень интересно. На кого же вы собираетесь поступать?
Программист? Архитектор? Журналист? Врач? Юрист? Или преподаватель?''')
    for i in works:
        if i in answer:
            agreement = True
            text = f'{random.choice(cute)} \n\n'
            if i == works[0]:
                session_state['question'] = random.choice(program)
                session_state['user_state'] = 'programmer'
                text += session_state['question']
                return make_response(text, session_state)
            elif i == works[1]:
                session_state['question'] = random.choice(arch)
                session_state['user_state'] = 'arch'
                text += session_state['question']
                return make_response(text, session_state)
            elif i == works[2]:
                session_state['question'] = random.choice(writ)
                session_state['user_state'] = 'writ'
                text += session_state['question']
                return make_response(text, session_state)
            elif i == works[3] or i == works[4]:
                session_state['question'] = random.choice(doct)
                session_state['user_state'] = 'doct'
                text += session_state['question']
                return make_response(text, session_state)
            elif i == works[5]:
                session_state['question'] = random.choice(polit)
                session_state['user_state'] = 'polit'
                text += session_state['question']
                return make_response(text, session_state)
            else:
                session_state['question'] = random.choice(teach)
                session_state['user_state'] = 'teach'
                text += session_state['question']
                return make_response(text, session_state)
    if agreement is False:
        text = random.choice(bag)
        return make_response(text, session_state)


def programmer(event, session_state):
    answer = event['request']['original_utterance'].lower()
    ask = session_state['question']
    good_answer = False
    if (ask == 'Были ли мониторы у первых компьютеров?' or
            ask == 'У компании Mac OC открытая файловая система на их устройствах или нет?' or
            ask == 'Самый маленький ПК весил около 1 килограмма?' or
            ask == 'Верно ли, что компьютер мощностью 1 терафлопс обрабатывает 100 тысяч операций в секунду?'):
        if answer in NO:
            good_answer = True
        else:
            good_answer = False
    if 'интерпрет' in ask:
        if '1' in answer or 'интерпрет' in answer:
            good_answer = True
        else:
            good_answer = False
    if 'for' in ask:
        if '1' in answer or 'цикл' in answer:
            good_answer = True
        else:
            good_answer = False
    if 'двоичную' in ask:
        if '11' in answer:
            good_answer = True
        else:
            good_answer = False
    if ask == 'Правда ли, что чем меньше технический нанометровый процесс, тем лучше?':
        if answer in YES:
            good_answer = True
        else:
            good_answer = False
    if 'блокового' in ask:
        if 'кодов' in answer.lower() or '1' in answer:
            good_answer = True
        else:
            good_answer = False
    if good_answer:
        session_state['work'] = 'programmer'
        session_state['salary'] = 48000
        return question_ok(session_state)
    else:
        session_state['work'] = ''
        session_state['salary'] = 0
        return question_nok(session_state)


def arch(event, session_state):
    answer = event['request']['original_utterance'].lower()
    ask = session_state['question']
    good_answer = False
    if 'мьюз' in ask:
        if '2' in answer or "ряд" in answer:
            good_answer = True
    if 'ордер' in ask:
        if '1' in answer or "композ" in answer:
            good_answer = True
    if 'премия' in ask:
        if '1' in answer or 'притцк' in answer.lower():
            good_answer = True
    if 'неперсонифицированная' in ask:
        if '1' in answer or 'народн' in answer.lower():
            good_answer = True
    if 'портик' in ask:
        if '2' in answer or 'перил' in answer.lower() or 'стен' in answer.lower():
            good_answer = True
    if 'Эйфелева' in ask or "Гамбург" in ask or 'Анфилада' in ask:
        if answer in YES:
            good_answer = True
    if good_answer:
        session_state['work'] = 'arch'
        session_state['salary'] = 45000
        return question_ok(session_state)
    else:
        session_state['work'] = ''
        session_state['salary'] = 0
        return question_nok(session_state)


def writ(event, session_state):
    answer = event['request']['original_utterance'].lower()
    ask = session_state['question']
    good_answer = False
    if ask == 'Кликбейт - это кнопка на печатной машинке?' or \
            ask == 'Все печатные издания были изумлены красотой Мэрилин Монро?' or \
            ask == 'Есенин был скромным человеком?' or \
            ask == 'Цветаева просила называть себя поэтессой?':
        if answer in NO:
            good_answer = True
    if ask == 'Владимир Маяковский был футуристом?':
        if answer in YES:
            good_answer = True
    if ask == 'Как расшифровывается СМИ?':
        if 'средств' in answer.lower() and 'массов' in answer.lower() and 'инф' in answer.lower():
            good_answer = True
    if ask == 'Сколько томов в Войне и Мир?':
        if int(answer) == 4:
            good_answer = True
    if ask == 'Поэтом каково века был Пушкин?':
        if int(answer) == 19:
            good_answer = True
    if ask == 'Какое самое популярное СМИ в мире?':
        if 'cnn' in answer.lower() or 'снн' in answer.lower():
            good_answer = True
    if ask == 'Кто является автором произведения "Анна Каренина"?':
        if 'толстой' in answer.lower():
            good_answer = True

    if good_answer:
        session_state['work'] = 'writ'
        session_state['salary'] = 29000
        return question_ok(session_state)
    else:
        session_state['work'] = ''
        session_state['salary'] = 0
        return question_nok(session_state)


def doct(event, session_state):
    answer = event['request']['original_utterance'].lower()
    ask = session_state['question']
    good_answer = False
    if 'H2O' in ask:
        if 'вод' in answer.lower():
            good_answer = True
    if 'позвоночн' in ask:
        if 'млек' in answer.lower():
            good_answer = True
    if 'медицин' in ask:
        if 'гиппократ' in answer.lower():
            good_answer = True
    if 'кузнеч' in ask:
        if 'ног' in answer.lower():
            good_answer = True
    if 'быстрое' in ask:
        if 'гепард' in answer.lower():
            good_answer = True
    if (ask == 'Микология - это наука о бактериях?' or ask == 'Могут ли лягушки жить в солёной воде?' or
            ask == 'Саламандра является теплокровным животным?'):
        if answer in NO:
            good_answer = True
    if ask == "Белый медведь самый крупный в мире хищник?" or ask == 'Верблюд запасает воду в крови':
        if answer in YES:
            good_answer = True

    if good_answer:
        session_state['work'] = 'doct'
        session_state['salary'] = 28000
        return question_ok(session_state)
    else:
        session_state['work'] = ''
        session_state['salary'] = 0
        return question_nok(session_state)


def polit(event, session_state):
    answer = event['request']['original_utterance'].lower()
    ask = session_state['question']
    good_answer = False
    if ask == 'Стагнация - это развитие общества?' or 'социальные' in ask:
        if answer in NO:
            good_answer = True
    if (ask == 'Детство- это период в жизни человека с рождения до 11 лет?' or
            ask == 'В РФ обязательно только 9-летнее образование?' or ask == 'Обязанность - это должное поведение?' or
            ask == 'Право - это допустимое поведение?' or ask == 'Общество - это  совокупность людей, объединившихся для '
                                                                 'общения '
                                                                 ' и совместного выполнения какой-либо деятельности?' or
            ask == 'Продолжительность рабочего времени в неделю не должна превышать 40 часов?' or 'удовлетв' in ask or
            'орудия' in ask):
        if answer in YES:
            good_answer = True

    if good_answer:
        session_state['work'] = 'polit'
        session_state['salary'] = 45000
        return question_ok(session_state)
    else:
        session_state['work'] = ''
        session_state['salary'] = 0
        return question_nok(session_state)


def teach(event, session_state):
    answer = event['request']['original_utterance'].lower()
    ask = session_state['question']
    good_answer = False
    if (ask == 'Если ты хочешь работать преподавателем тебе нужно получить высшее образование?' or
            ask == 'Важно ли умение находить общий язык с детьми и поддерживать с ними хорошие отношения?' or
            ask == 'Преподаватель важная профессия для нашего будущего?' or
            ask == 'Эмоции ребенка и его переживания – это важные факторы. Вы согласны с этим?' or
            'магистра' in ask):
        if answer in YES:
            good_answer = True
    if 'понятие' in ask:
        if '5000' in answer or '5 тыс' in answer.lower():
            good_answer = True

    if good_answer:
        session_state['work'] = 'teach'
        session_state['salary'] = 30000
        return question_ok(session_state)
    else:
        session_state['work'] = ''
        session_state['salary'] = 0
        return question_nok(session_state)


def question_ok(session_state):
    text = random.choice(CUTE)
    text += """\n\n Выберите пункт меню:
        Лотерея
        Биржа
        Помощь
        Получить образование
        Работа"""
    session_state['user_state'] = 'menu'
    return make_response(text, session_state)


def question_nok(session_state):
    text = random.choice(UNCUTE)
    text += '''\n\nИли же вы устроитесь сейчас на работу с маленькой зарплатой, или пойдёте учиться, но для этого вам нужно
будет сдать вступительный экзамен.'''
    session_state['user_state'] = 'work_or_student'
    return make_response(text, session_state)
