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
    # These are prompts for generating short summaries for each language
    ML_SHORT_SUMMARY_EN = [
        "Give me a short summary for this text in english: " + "\n" + "{text}" + "\n",
        "ml-short-summary-english",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SHORT_SUMMARY_FR = [
        "Donnez-moi un petit résumé de ce texte en français: " + "\n" + "{text}" + "\n",
        "ml-short-summary-french",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SHORT_SUMMARY_CA = [
        "Dóna'm un breu resum d'aquest text en català: " + "\n" + "{text}" + "\n",
        "ml-short-summary-catalan",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SHORT_SUMMARY_ES = [
        "Dame un breve resumen de este texto en español: " + "\n" + "{text}" + "\n",
        "ml-short-summary-spanish",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SHORT_SUMMARY_DE = [
        "Geben Sie mir eine kurze Zusammenfassung für diesen Text auf Deutsch: "
        + "\n"
        + "{text}"
        + "\n",
        "ml-short-summary-german",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SHORT_SUMMARY_IT = [
        "Datemi un breve riassunto di questo testo in italiano: "
        + "\n"
        + "{text}"
        + "\n",
        "ml-short-summary-italian",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SHORT_SUMMARY_JP = [
        "この文章の要約を日本語で教えてください。: " + "\n" + "{text}" + "\n",
        "ml-short-summary-japanese",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]

    # These are headline generation prompt3 in their given language
    ML_HEADLINE_EN = [
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
        "ml-headline-generation-en",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    ML_HEADLINE_FR = [
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
        "ml-headline-generation-fr",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    ML_HEADLINE_CA = [
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
        "ml-headline-generation-ca",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    ML_HEADLINE_ES = [
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
        "ml-headline-generation-es",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    ML_HEADLINE_IT = [
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
        "ml-headline-generation-it",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    ML_HEADLINE_DE = [
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
        "ml-headline-generation-de",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]
    ML_HEADLINE_JP = [
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
        "ml-headline-generation-jp",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 1},
    ]

    # Transcript segmentation prompt
    ML_TRANSCRIPT_SEGMENTATION = [
        """
        Your task is detecting the segment of a transcript related to a certain keyword.
        This task is really important to me.
        The transcript is delimited by < and >, and keyword is delimited by * and *.

        The transcript is a list of json objects. Each json object has 2 keys: "start_time" and "content". When you do the analysis, only focus on the value of "content" in each json object.

        You must do the analysis using following steps:
        1. Go through the whole transcript have a high level understanding for the relationship between the keyword and this transcript.
        2. Check every json object to decide if its value of "content" direct or indirect related to the given keyword.
        3. Copy and paste the json objects which relate to the keyword, and output to me.

        Transcript: <{transcript}>
        Keyword:*{keyword}*

        Show me your answer in following Json format. Here [XXX] is placeholder:
        [Relationship with keyword]:[The relationship between keyword and this transcript content]
        [Related segment]:[The segments which you think are related to the keyword]
        [Reason]:[The reason that why you think the segments are related to the keyword]
        [Reason for not choose]:[Your reason for those segments that you think are irrelevent to the keyword]

        """,  # noqa: E501
        "ml-transcript-segmentation",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
    ]
