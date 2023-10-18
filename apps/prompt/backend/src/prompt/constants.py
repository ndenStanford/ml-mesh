"""Constants."""

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum


class PromptEnum(OnclusiveEnum):
    """Enum values for prompts."""

    EN = [
        "Give an abstractive summary while retaining important quotes of speech in less than "
        + "{number}"  # noqa: W503
        + " words: "  # noqa: W503
        + "\n"  # noqa: W503
        + "{text}"  # noqa: W503
        + "\n",  # noqa: W503
        "english-summarization",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SEG = [
        "Do a segmentation unifying the main stories of this text in their given language and "
        + "output a json object where the key is the start time code and "  # noqa: W503
        + "the value is the headline of the main stories: {transcript}",  # noqa: W503
        "ml-transcript-segmentation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 0},
    ]
    # These are headline generation prompt3 in their given language
    HEADLINE_EN = [
        "You are an expert in news writing."
        + "\n"
        + "I have an article delimited by < and >, \
            and I want you to write a title for this article."
        + "\n"
        + "Your title must satisfy all of the following aspects:"
        + "\n"
        + "1. The title must be in English."
        + "\n"
        + "2. The title should include the main idea of the article."
        + "\n"
        + "3. The title must not include any thing that is not mentioned in the article."
        + "\n"
        + "Article: "
        + "<{text}>"
        + "\n",
        "english-headline-generation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    HEADLINE_FR = [
        "Vous êtes un expert dans la rédaction d'articles d'actualité."
        + "\n"
        + "J'ai un article délimité par < et > \
            et je souhaite que vous écriviez un titre pour cet article."
        + "\n"
        + "Votre titre doit satisfaire à tous les aspects suivants:"
        + "\n"
        + "1. Le titre doit être en français."
        + "\n"
        + "2. Le titre doit inclure l'idée principale de l'article."
        + "\n"
        + "3. Le titre ne doit contenir rien qui ne soit pas mentionné dans l'article."
        + "\n"
        + "Article: "
        + "<{text}>"
        + "\n",
        "french-headline-generation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    HEADLINE_CA = [
        "Ets un expert en redacció de notícies."
        + "\n"
        + "Tinc un article delimitat per < i >, \
            i vull que escriguis un títol per a aquest article."
        + "\n"
        + "El teu títol ha de satisfer tots els següents aspectes:"
        + "\n"
        + "1. El títol ha d'estar en català."
        + "\n"
        + "2. El títol ha d'incloure la idea principal de l'article."
        + "\n"
        + "3. El títol no ha d'incloure res que no estigui esmentat a l'article."
        + "\n"
        + "Article: "
        + "<{text}>"
        + "\n",
        "catalan-headline-generation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    HEADLINE_ES = [
        "Eres un experto en escribir noticias."
        + "\n"
        + "Tengo un artículo delimitado por < y >, \
            y quiero que escribas un título para este artículo."
        + "\n"
        + "Tu título debe cumplir con todos los siguientes aspectos:"
        + "\n"
        + "1. El título debe estar en español."
        + "\n"
        + "2. El título debe incluir la idea principal del artículo."
        + "\n"
        + "3. El título no debe incluir nada que no se mencione en el artículo."
        + "\n"
        + "Artículo: "
        + "<{text}>"
        + "\n",
        "spanish-headline-generation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    HEADLINE_IT = [
        "Sei un esperto nella scrittura di notizie."
        + "\n"
        + "Ho un articolo delimitato da < e >, \
            e voglio che tu scriva un titolo per questo articolo."
        + "\n"
        + "Il tuo titolo dovrebbe soddisfare tutti i seguenti aspetti:"
        + "\n"
        + "1. Il titolo deve essere in italiano."
        + "\n"
        + "2. Il titolo dovrebbe includere l'idea principale dell'articolo."
        + "\n"
        + "3. Il titolo non deve includere nulla che non sia menzionato nell'articolo."
        + "\n"
        + "Articolo: "
        + "<{text}>"
        + "\n",
        "italian-headline-generation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    HEADLINE_DE = [
        "Sie sind ein Experte im Nachrichtenschreiben."
        + "\n"
        + "Ich habe einen Artikel, der durch < und > \
            begrenzt ist, und ich möchte, dass Sie einen Titel für diesen Artikel schreiben."
        + "\n"
        + "Ihr Titel muss alle folgenden Aspekte erfüllen:"
        + "\n"
        + "1. Der Titel muss auf Deutsch sein."
        + "\n"
        + "2. Der Titel sollte die Hauptidee des Artikels enthalten."
        + "\n"
        + "3. Der Titel darf nichts enthalten, was nicht im Artikel erwähnt wird."
        + "\n"
        + "Artikel: "
        + "<{text}>"
        + "\n",
        "german-headline-generation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    HEADLINE_JP = [
        "あなたはニュース作成の専門家です。"
        + "\n"
        + "私は<と>で区切られた記事を持っています、\
            そしてあなたにこの記事のためのタイトルを書いてほしいです。"
        + "\n"
        + "あなたのタイトルは以下のすべての側面を満たさなければなりません："
        + "\n"
        + "1. タイトルは日本語であること。"
        + "\n"
        + "2. タイトルには記事の主要なアイデアを含めること。"
        + "\n"
        + "3. タイトルには記事で言及されていないものを含めないこと。"
        + "\n"
        + "記事: "
        + "<{text}>"
        + "\n",
        "japanese-headline-generation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
