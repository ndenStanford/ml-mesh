"""Prompt storage."""
Prompt_dict = {
    "analysis": {
        "alias": "topic-detection-analysis",
        "template": """
                I want you to summarize the protential impact on the given category in the target industry, based on all the articles together.

                I will give you a target industry delimited by *, the target category delimited by < and >,
                and many articles related to this industry delimited by triple backticks.

                Target industry: *{target_industry}*

                Target category: <{target_category}>

                For the category isn't not related to the articles, output 'Not mentioned'.

                Generate your output in following format:
                For category Risk detection, the articles suggest that the risk detection in the science and technology industry is
                related to the dependency on imported components, especially semiconductor ones, volatility in weather patterns,
                and the limited understanding about the universe including black holes.

                {content}
                """,  # noqa: E501
    },
    "aggregate": {
        "alias": "topic-analysis-aggregation",
        "template": """
                I want you to provide a concise summary that combines the main points of the following summaries.

                Those summaries are from multiple articles, focusing on a given aspect of a target industry.

                I will give you the target industry delimited by *, a target category delimited by < and >,
                and many summaries from articles related to this industry delimited by triple backticks.

                Target industry: *{target_industry}*

                Target category: <{target_category}>

                Restrict your output in 100 words.

                {Summary}
        """,  # noqa: E501
    },
}
