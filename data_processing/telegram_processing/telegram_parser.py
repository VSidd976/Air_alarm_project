import pandas as pd
import re
import emoji
import spacy
from pathlib import Path
from langdetect import detect

target_words = [

    # target words for ukranian channels
    "зліт", "ракета", "пуск", "запуск ракети", "ймовірний пуск",
    "активність авіація", "літак в повітрі", "стратег", "міг", "ту-95", "кінджал",
    "пуск з каспій", "ракетна небезпека", "балістична ракета", "іскандер", "калібр",
    "крилата ракета", "шахед", "дрон", "ппо", "збиття", "винищувач", "удар",
    "вибух", "зруйнувати", "травмувати", "обстріл", "небезпека", "загроза",
    "підвищена активність", "військовий техніка", "військо рф", "окупанти",
    "ворожий літак", "повітряний ціль", "влучити", "прильот", "серія вибухів",
    "удар по інфраструктурі", "ракетний обстріл", "артобстріл", "вибухова хвиля",
    "удар по енергетиці", "масовий пуск", "атака дронів", "контратака ворога",
    "переміщення техніки", "ворожий об'єкт", "висока ймовірність удару",
    "можливий обстріл", "загроза застосування озброєння", "спостерігається загроза",
    "небезпека в повітрі", "ймовірна атака", "підвищення активності авіації",
    "формування групи удару", "випуск калібрів", "ракетна загроза", "підвищена загроза",
    "ракета підльоті", "зліт мігів", "міг в повітрі", "стратег в повітрі",
    "приближення ракети", "ціль на підльоті", "траєкторія ракети", "перехоплення цілі",
    "мопед",

    # target words for ukranian channels in russian
    "взлет", "ракета", "пуск", "запуск ракеты", "вероятный пуск",
    "активность авиация", "самолет в воздухе", "стратег", "миг", "ту-95", "кинжал",
    "пуск с каспия", "ракетная угроза", "баллистическая ракета", "искандер", "калибр",
    "крылатая ракета", "шахед", "дрон", "ПВО", "поражение", "истребитель", "удар",
    "взрыв", "разрушить", "повредить", "обстрел", "опасность", "угроза",
    "повышенная активность", "военная техника", "войска рф", "оккупанты",
    "вражеский самолет", "воздушная цель", "попасть", "приход", "серия взрывов",
    "удар по инфраструктуре", "ракетный обстрел", "артобстрел", "взрывная волна",
    "удар по энергетике", "массовый пуск", "атака дронов", "контратака врага",
    "перемещение техники", "вражеский объект", "высокая вероятность удара",
    "возможный обстрел", "угроза применения оружия", "наблюдается угроза",
    "опасность в воздухе", "вероятная атака", "повышение активности авиации",
    "формирование группы удара", "пуск калибров", "ракетная угроза", "повышенная угроза",
    "ракета на подлете", "взлет мигов", "миг в воздухе", "стратег в воздухе",
    "приближение ракеты", "цель на подлете", "траектория ракеты", "перехват цели",
    "мопед",

    # target words for channels from russia
    "войска рф", "оккупанты", "российский военный", "российское правительство", "вооруженные силы рф",
    "российская пропаганда", "мобилизация", "специальная операция", "план специальной операции", "фронт",
    "боевые действия", "контратака", "армия рф", "украинская армия", "защита", "нападение", "победа",
    "российский президент", "путин", "взрывы", "удары", "ракетные удары", "обстрелы", "уничтожение",
    "успех", "штурм", "непобедимость", "победа на фронте", "мирное соглашение", "стратегия", "экономическая блокада",
    "ресурсы рф", "крым", "крымский мост", "аннексия", "мобилизованные", "силы обороны", "оккупированные территории",
    "выборы", "референдум", "депортация", "поддержка", "санкции", "подготовка к наступлению", "регионы рф",
    "террористы", "правоохранители", "контрнаступ", "стратегические цели", "операция в Украине", "поддержка военных",
    "шпионаж", "россияне", "правительство рф", "фальшивые новости", "поддержка власти", "международное сообщество",
    "дезинформация", "новости россии", "граждане рф", "военные преступления", "лидер рф",
    "украинские националисты", "подготовка к войне", "глобальный конфликт", "поддержка войск", "поддержка армии рф",
    "секретные данные", "спецслужбы", "террористические акты", "построение обороны", "угроза ядерного удара",
    "военные провокации", "защита прав россиян", "военный конфликт", "давление на Украину",
    "победа на всех фронтах", "приказ президента", "черная пропаганда", "государственная безопасность"
]

stop_words = [
    "і", "та", "й", "а", "але", "або", "бо", "щоб", "що", "як", "коли", "де", "куди", "звідки", "якщо", "хоч", "хоча",
    "чи", "ніби", "наче", "неначе", "немов",
    "в", "у", "з", "із", "до", "на", "при", "перед", "над", "під", "за", "через", "між", "про", "для", "без", "після",
    "біля", "коло",
    "я", "ти", "він", "вона", "воно", "ми", "ви", "вони", "мене", "мені", "мною", "тебе", "тобі", "тобою", "його", "її",
    "нас", "нам", "нами", "вас", "вам", "вами", "їх", "їм", "ними", "собі", "себе", "собою",
    "цей", "ця", "це", "ці", "той", "та", "те", "ті", "який", "яка", "яке", "які",
    "був", "була", "було", "були", "бути", "є", "буде", "будемо", "будеш", "будете", "бувши",
    "не", "вже", "ще", "лише", "тільки", "саме", "навіть", "також", "от", "ось", "он", "ну", "ж", "би", "б", "хай",
    "нехай", "аби", "хоч", "мов",
    "так", "ні", "може", "мабуть", "звісно", "очевидно", "щось", "хтось", "будь-хто", "дещо", "ніхто", "ніщо",
    "підписатись", "від", "газета"


                          "и", "а", "но", "или", "чтобы", "что", "как", "когда", "где", "куда", "откуда", "если",
    "хотя", "хоть", "либо", "будто", "словно", "так", "так как",
    "в", "на", "по", "под", "над", "из", "у", "от", "при", "между", "через", "без", "после", "перед", "около", "для",
    "про", "об", "обо",
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "мне", "мной", "тебя", "тебе", "тобой", "его", "её",
    "нас", "нам", "нами", "вас", "вам", "вами", "их", "им", "ими", "себя", "себе", "собой",
    "этот", "эта", "это", "эти", "тот", "та", "то", "те", "который", "которая", "которое", "которые",
    "был", "была", "было", "были", "быть", "есть", "будет", "будем", "будешь", "будете", "будучи",
    "не", "уже", "ещё", "лишь", "только", "именно", "даже", "также", "вот", "вон", "ну", "же", "бы", "пусть", "пускай",
    "давай", "мол",
    "да", "нет", "может", "наверное", "конечно", "возможно", "кто-то", "что-то", "кое-что", "никто", "ничто",
    "подписаться", "александр", "алексей", "андрей", "ваш", "видео", "включая", "вместе", "вновь", "год", "дневник",
    "друг", "ее", "ему", "ес", "ещ", "закрыть", "изза", "иметь", "имя", "интервью", "которого", "которой", "которую",
    "которых", "однако", "парень", "подписчик", "пожар", "пока", "показать", "потому", "почему", "поэтому", "почти",
    "правда", "проект", "сайт", "сам", "сами", "самом", "сеть",

    "the", "upd"
]

nlp_uk = spacy.load("uk_core_news_sm")
nlp_ru = spacy.load("ru_core_news_sm")


def clean_text(text):

    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^a-zA-Zа-яА-ЯєіїЄІЇґҐ0-9\s]', '', text)
    text = emoji.replace_emoji(text, replace="")
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\d+', '', text)

    return text


def contains_keywords(text, keywords):
    return any(keyword in text for keyword in keywords)


def lematize_text(text, language):

    if language == 'ru':
        nlp = nlp_ru
    else:
        nlp = nlp_uk

    docs = nlp.pipe(text, batch_size=50, n_process=4)
    return [' '.join(token.lemma_ for token in doc if token.is_alpha) for doc in docs]


def clean_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


def parse_channel(csv_file):
    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['message'])
    df = df.drop(columns=[
        'id',
        'message_id',
        'sender_id',
        'first_name',
        'last_name',
        'username',
        'media_path',
        'reply_to',
        'media_type'
    ])
    df.loc[:, 'date'] = pd.to_datetime(df['date'])
    df.loc[:, 'date'] = df['date'] - pd.Timedelta(hours=10)
    df = df[df['date'] >= '2022-02-24 00:00:00']
    df['message'] = df['message'].apply(clean_text)
    df = df[df['message'] != '']
    language = detect(df['message'].iloc[0])
    df['message'] = lematize_text(df['message'], language)
    df['important'] = df['message'].apply(lambda x: contains_keywords(x, target_words))
    df = df[df['important'] != False]
    df = df.drop(columns='important')
    df['message'] = df['message'].apply(clean_stopwords)
    return df


def main():
    current_dir = Path(__file__).parent
    data_path = current_dir.parent.parent / 'Data_Collection' / 'telegram-scraper'
    first = True
    print("\nTelegram data parsing began")

    for i in Path(data_path).iterdir():
        if not i.is_dir():
            continue

        try:
            csv_file = next(i.rglob('*.csv'))
        except StopIteration:
            continue

        print(f"\nChannel {i.name} is parsing")
        df = parse_channel(csv_file)
        df.to_csv("parsed_telegram_data.csv", mode='a', header=first, index=False)
        first = False
        print(f"Channel {i.name} parsing has ended")

    merged_df = pd.read_csv("parsed_telegram_data.csv")
    merged_df = merged_df.sort_values(by='date').reset_index(drop=True)
    merged_df.to_csv('parsed_telegram_data.csv', index = False)
    print("\nTelegram data parsing has ended")


if __name__ == '__main__':
    main()