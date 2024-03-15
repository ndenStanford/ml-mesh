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
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
    ]
    # These are prompts for generating short summaries for each language
    ML_SHORT_SUMMARY_EN = [
        "Give me a short summary for this text in english: " + "\n" + "{text}" + "\n",
        "ml-short-summary-english",
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
    ]
    ML_SHORT_SUMMARY_FR = [
        "Donnez-moi un petit résumé de ce texte en français: " + "\n" + "{text}" + "\n",
        "ml-short-summary-french",
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
    ]
    ML_SHORT_SUMMARY_CA = [
        "Dóna'm un breu resum d'aquest text en català: " + "\n" + "{text}" + "\n",
        "ml-short-summary-catalan",
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
    ]
    ML_SHORT_SUMMARY_ES = [
        "Dame un breve resumen de este texto en español: " + "\n" + "{text}" + "\n",
        "ml-short-summary-spanish",
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
    ]
    ML_SHORT_SUMMARY_DE = [
        "Geben Sie mir eine kurze Zusammenfassung für diesen Text auf Deutsch: "
        + "\n"
        + "{text}"
        + "\n",
        "ml-short-summary-german",
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
    ]
    ML_SHORT_SUMMARY_IT = [
        "Datemi un breve riassunto di questo testo in italiano: "
        + "\n"
        + "{text}"
        + "\n",
        "ml-short-summary-italian",
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
    ]
    ML_SHORT_SUMMARY_JP = [
        "この文章の要約を日本語で教えてください。: " + "\n" + "{text}" + "\n",
        "ml-short-summary-japanese",
        {
            "model_name": "gpt-3.5-turbo",
            "max_tokens": 512,
            "temperature": 0.7,
            "response_format": None,
        },
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
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": 2048,
            "temperature": 1,
            "response_format": None,
        },
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
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": 2048,
            "temperature": 1,
            "response_format": None,
        },
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
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": 2048,
            "temperature": 1,
            "response_format": None,
        },
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
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": 2048,
            "temperature": 1,
            "response_format": None,
        },
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
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": 2048,
            "temperature": 1,
            "response_format": None,
        },
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
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": 2048,
            "temperature": 1,
            "response_format": None,
        },
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
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": 2048,
            "temperature": 1,
            "response_format": None,
        },
    ]

    # Transcript segmentation prompt
    ML_TRANSCRIPT_SEGMENTATION = [
        """
        You are an expert in news analysis.
        You will be given a paragraph which consists of several different news pieces, and a list of keywords.
        The paragraph is delimited by < and >, and the keywords list is delimited by * and *.

        Your task is: Identify each news piece, then figure out which news piece is related to the given keywords.
        Note: each sentence in the paragraph must be in one news piece.

        You must do the analysis following the steps below:
        1. Go through the whole paragraph to understand the content.
        2. Divide the whole paragraph into several segments. Make sure that each segment focuses on a single news topic.
        3. Analyze the content of each segment, then decide if the given keywords are related to any segment.
        4. In step 3 if a segment is chosen, you need look at the piece before and the piece after the chosen segment. If any of these pieces mention something that's also talked about in the chosen segment, even just a little bit, consider them related. This includes any small reference or mention related to the segment's topics.
        5. If the answer in step 4 is yes, add the related sentence into the chosen segment. And output the news segment.
        6. If the content holds no mention of the keywords at all, return N/A

        Keywords: *{keywords}*
        Content: <{paragraph}>

        Show me your answer in following JSON format. Here [XXX] is placeholder:
        [Related segment]:[The relevant news segment about the keywords]
        [Reason for segment]:[The reason you believe this story relates to the keywords]
        [Segment summary]:[A one sentence summary of the segment extracted]
        [Segment title]:[A title that represents the segment extracted. The title must be in same language as the segment.]
        [segment amount]: [How many news segment in total]
        [Piece before]:[The piece before the chosen segment]
        [Piece after]: [The piece after the chosen segment]
        [Piece before accept]: [Does the piece before the segment hold any relevance to the segment and keywords? You must answer with just Yes or No]
        [Piece after accept]: [Does the piece after the segment hold any relevance to the segment and keywords? You must answer with just Yes or No]
        """,  # noqa: E501
        "ml-transcript-segmentation",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
    ]

    # Transcript segmentation prompt
    ML_TRANSCRIPT_SEGMENTATION_AD_DETECTION = [
        """
        You are an AI trained to distinguish between main content and advertisements in a paragraph.

        The paragraph is delimited by < and >.

        Use the following criteria to guide your analysis:
        1. Content Relevance and Integration: Determine whether the content is closely related to the main theme or appears to be promotional or unrelated to the topic.
        2. Tone and Language: Assess whether the language used is informational, educational, or entertaining consistent with the paragraph's overall tone, or if it uses persuasive language aimed at provoking action (such as 'Buy now', 'Subscribe', or 'Sign up').
        3. Linking Patterns: Examine if the links within the paragraph aim to provide additional information or references, or if they direct readers to a product page, subscription form, or another platform for purchasing or engaging with a service or product.
        4. Placement Within the Paragraph: Consider how each section contributes to the paragraph's narrative or informational structure, or if it seems inserted without contributing to the narrative flow, particularly noting sections that might be placed strategically to capture attention without adding to the content's value.
        5. Disclosure Labels: Look for any labels that might indicate a section is sponsored or an advertisement, such as 'Sponsored', 'Ad', 'Promotion', or similar indicators.
        6. Contextual Evaluation of Calls to Action: Specifically for sentences or sections calling for reader support or action, critically assess these in the context of the paragraph’s overall theme. Such content should not be classified as an advertisement if it directly relates to and supports the paragraph’s main argument or purpose.

        You should follow the steps below:
        1. Read the entire paragraph carefully.
        2. Identify any segment that are advertisements, with the criterias provided above.
        3. Use a 'yes' or 'no' to indicate if any advertisement inside the paragraph and output to me.

        Paragraph: <{paragraph}>

        Show me your result in following JSON format. Here [XXX] is placeholder:
        [Advertisement detect]: [Answer 'yes' or 'no' to indicate if there is any advertisement in the paragraph]
        [Advertisement content]:[The reason for why you think there is advertisement]
        """,  # noqa: E501
        "ml-transcript-segmentation-ad-detection",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_5_ARTICLES_SUMMARY = [
        """
        You are a summarization bot.

        I will give you 5 articles which are delimited by triple backticks.

        I want you to generate a one-paragraph summary for all the articles I give. And you should based on your summary to give me a title for your summary.

        You must use the following step to generate your result:
        1. Read every article carefully and understand the main idea of each article.
        2. Once you have the main point from each article, look for common themes, similarities, or overlapping ideas among them. Group these main points based on these commonalities.
        3. For each group of main points, distill them into a single sentence that encapsulates the shared message or theme.
        4. Order these distilled sentences in a logical or meaningful sequence that provides coherence and flow to the reader.
        5. Write a one-paragraph summarization that concisely represents the information from all the articles, using the ordered distilled sentences as your guide.
        6. Generate a title based on the one-paragraph summarization you generate.

        Input article 1: '''{article1}'''
        Input article 2: '''{article2}'''
        Input article 3: '''{article3}'''
        Input article 4: '''{article4}'''
        Input article 5: '''{article5}'''

        Let's think step by step and show me your answer in following JSON format."[xxx]" is placeholder.
        The main point of each input article: [mean point of each article]
        Title: [The title you generate for these articles]
        Summary: [The summary you generate for these articles]
        """,  # noqa: E501
        "ml-5-articles-summary",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_4_ARTICLES_SUMMARY = [
        """
        You are a summarization bot.

        I will give you 4 articles which are delimited by triple backticks.

        I want you to generate a one-paragraph summary for all the articles I give. And you should based on your summary to give me a title for your summary.

        You must use the following step to generate your result:
        1. Read every article carefully and understand the main idea of each article.
        2. Once you have the main point from each article, look for common themes, similarities, or overlapping ideas among them. Group these main points based on these commonalities.
        3. For each group of main points, distill them into a single sentence that encapsulates the shared message or theme.
        4. Order these distilled sentences in a logical or meaningful sequence that provides coherence and flow to the reader.
        5. Write a one-paragraph summarization that concisely represents the information from all the articles, using the ordered distilled sentences as your guide.
        6. Generate a title based on the one-paragraph summarization you generate.

        Input article 1: '''{article1}'''
        Input article 2: '''{article2}'''
        Input article 3: '''{article3}'''
        Input article 4: '''{article4}'''

        Let's think step by step and show me your answer in following JSON format."[xxx]" is placeholder.
        The main point of each input article: [mean point of each article]
        Title: [The title you generate for these articles]
        Summary: [The summary you generate for these articles]
        """,  # noqa: E501
        "ml-4-articles-summary",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_3_ARTICLES_SUMMARY = [
        """
        You are a summarization bot.

        I will give you 3 articles which are delimited by triple backticks.

        I want you to generate a one-paragraph summary for all the articles I give. And you should based on your summary to give me a title for your summary.

        You must use the following step to generate your result:
        1. Read every article carefully and understand the main idea of each article.
        2. Once you have the main point from each article, look for common themes, similarities, or overlapping ideas among them. Group these main points based on these commonalities.
        3. For each group of main points, distill them into a single sentence that encapsulates the shared message or theme.
        4. Order these distilled sentences in a logical or meaningful sequence that provides coherence and flow to the reader.
        5. Write a one-paragraph summarization that concisely represents the information from all the articles, using the ordered distilled sentences as your guide.
        6. Generate a title based on the one-paragraph summarization you generate.

        Input article 1: '''{article1}'''
        Input article 2: '''{article2}'''
        Input article 3: '''{article3}'''

        Let's think step by step and show me your answer in following JSON format."[xxx]" is placeholder.
        The main point of each input article: [mean point of each article]
        Title: [The title you generate for these articles]
        Summary: [The summary you generate for these articles]
        """,  # noqa: E501
        "ml-3-articles-summary",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_2_ARTICLES_SUMMARY = [
        """
        You are a summarization bot.

        I will give you 2 articles which are delimited by triple backticks.

        I want you to generate a one-paragraph summary for all the articles I give. And you should based on your summary to give me a title for your summary.

        You must use the following step to generate your result:
        1. Read every article carefully and understand the main idea of each article.
        2. Once you have the main point from each article, look for common themes, similarities, or overlapping ideas among them. Group these main points based on these commonalities.
        3. For each group of main points, distill them into a single sentence that encapsulates the shared message or theme.
        4. Order these distilled sentences in a logical or meaningful sequence that provides coherence and flow to the reader.
        5. Write a one-paragraph summarization that concisely represents the information from all the articles, using the ordered distilled sentences as your guide.
        6. Generate a title based on the one-paragraph summarization you generate.

        Input article 1: '''{article1}'''
        Input article 2: '''{article2}'''

        Let's think step by step and show me your answer in following JSON format."[xxx]" is placeholder.
        The main point of each input article: [mean point of each article]
        Title: [The title you generate for these articles]
        Summary: [The summary you generate for these articles]
        """,  # noqa: E501
        "ml-2-articles-summary",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_TOPIC_SUMMARIZATION_SINGLE_ANALYSIS = [
        """
        You are an expert in finding insight from a group of articles.

        I want you to summarize the potential impact on a given category, based on all the input articles together.

        I will give you a target category delimited by < and >,
        and many articles related to this industry delimited by triple backticks.

        Target category: <{target_category}>
        Input articles: {content}

        If none of the articles are related to the target category, output the category followed by 'null', the null value in JSON format. For example, if the category is 'Risk Detection' and no articles are relevant, output should be 'Risk Detection': null.

        You must follow the steps below:
        1. Go through every input article to understand its content.
        2. For every article, think about what it talks about the target category.
        3. Aggregate the insights from step 2 to generate a concise, narrative-style and easy-to-read paragraph to show the content mentioned by all the input articles about the target category.

        Let's think step by step and generate your output in following JSON format. Here 'xxx' is placeholders:
        Article's content about target category: [For each article, what it talks about the target category]
        {target_category}: An overall summary for the content about target category, based on all the input articles
        """,  # noqa: E501
        "ml-topic-summarization-single-analysis",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_TOPIC_SUMMARIZATION_AGGREGATION = [
        """
        You are an expert in news analyzing and summarization.

        I want you to provide a concise summary that combines the main points of the following summaries. Then inference the impact level of this category, based on the summaries provided.

        Those summaries are from multiple articles, focusing on a given aspect of a target category.

        I will give you the target category delimited by < and >,
        and many summaries from articles related to this industry delimited by triple backticks.

        Target category: <{target_category}>
        Input summaries: {Summary}

        If none of the summaries are related to the target category, then output the following in JSON format. Note: Here, 'null' represents the absence of relevant information in JSON format.
        Overall summary: null (indicating no summary can be provided)
        Impact level: Low
        Theme: null

        You must follow the steps below:
        1. Carefully review every summary, ensuring a deep understanding of each one.
        2. Extract the distinct information from each summary, ensuring no repetition but capturing the crux.
        3. Using the extracted information, craft an in-depth, unified one-paragraph summary that elaborates on the main points.
        4. Based on the one-paragraph summary generated in Step 3, generate a theme for {target_category}.
        5. Assess the impact level of this target category based on the one-paragraph summary. To do this, follow these additional steps:
            a. Evaluate if the content suggests a significant change or influence in the industry (High Impact), a moderate change (Medium Impact), or minimal to no change (Low Impact).
            b. Consider the urgency, scope, and the evidence strength in the summaries. Is it urgent and widespread with strong evidence (High)? Noticeable but not urgent, with some evidence (Medium)? Or of low priority and relevance with weak evidence (Low)?
            c. Use this chain-of-thought process to categorize the impact level into either 'Low', 'Medium', or 'High'.

        Let's think step by step and generate your output in following JSON format. Here '[xxx]' is placeholders:
        The distinct information from each summary: [The distinct information in each summary]
        Overall summary: [An overall summary for the content about target category, based on all the input summaries]
        Theme: [The theme for {target_category}, based on the one-paragraph summary]
        Significant change: [if the content suggests a significant change in the {target_category}]
        Impact level: [The impact level of this target category]
        Reason for impact: [The reason for this impact level]
        """,  # noqa: E501
        "ml-topic-summarization-aggregation",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_MULTI_ARTICLES_SUMMARIZATION = [
        """
        You are a summarization bot.

        I will give you several articles and the articles are delimited by triple backticks.

        I want you to generate a one-paragraph summary for all the articles I give.

        You must use the following step to generate your result:
        1. Read every article carefully and understand the main idea of each article.
        2. Once you have the main point from each article, look for common themes, similarities, or overlapping ideas among them. Group these main points based on these commonalities.
        3. For each group of main points, distill them into a single sentence that encapsulates the shared message or theme.
        4. Order these distilled sentences in a logical or meaningful sequence that provides coherence and flow to the reader.
        5. Write a one-paragraph summarization that concisely represents the information from all the articles, using the ordered distilled sentences as your guide.

        Input articles: {content}

        Let's think step by step and show me your answer in following JSON format."xxx" is placeholder.
        The main point of each input article: [mean point of each article]
        Summary: The summary you generate for these articles
        """,  # noqa: E501
        "ml-multi-articles-summarization",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]

    ML_ARICLES_SUMMARY_AGGREGATION = [
        """
        You are an expert in extracting and consolidating insights from articles.

        Your primary objective is to produce a comprehensive one-paragraph summary, that combines the insights from multiple article summaries. Each of those summaries will be provided to you, delimited by triple backticks.

        Further, based on your consolidated summary, you are to generate a theme for all the input summaries.

        The process you must follow is detailed below:
        1. Carefully review every summary, ensuring a deep understanding of each one.
        2. Extract the distinct information from each summary, ensuring no repetition but capturing the crux.
        3. Using the extracted information, craft an in-depth, unified one-paragraph summary that elaborates on the main points.
        4. Finally, formulate a single, overarching theme that captures the essence of all the summaries.

        Input summaries: {Summary}

        Let's proceed methodically. Present your response in the following JSON format, where "xxx" is a placeholder:
        Distinct Information: [Distinct details from each summary]
        Summary: Your synthesized summary based on all the summaries I provided
        Theme: The theme for your consolidated summary
        """,  # noqa: E501
        "ml-articles-summary-aggregation",
        {
            "model_name": "gpt-4-1106-preview",
            "max_tokens": None,
            "temperature": 1,
            "response_format": {"type": "json_object"},
        },
    ]
