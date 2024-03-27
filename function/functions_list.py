functions = [
    {
        "type": "function",
        "function": {
            "name": "search_youtube",
            "description": "Search YouTube for relevant videos for user query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": """The query for which we have to find relevant videos. Modify query in such a way that we can find related videos to user query.
                        Example:
                        ""
                        User: "Please describe the concept of transformers using the following image as a reference: ![Transformers YOLO](https://miro.medium.com/v2/resize:fit:863/0*jKqypwGzmDv7KDUZ.png)"
                        query: "Describe the concept of transformers using the inmage as a reference"
                        ""
                        """,
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "handle_image",
            "description": "Call GPT-4-Vision API to undersand image based queries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": """The query relevant to image""",
                    },
                    "url": {
                        "type": "string",
                        "description": """The URL of the image to be sent to GPT-4-Vision. Extract the raw URL from the user message.
                        Example:
                        ""
                        User: "Please describe the concept of transformers using the following image as a reference: ![Transformers YOLO](https://miro.medium.com/v2/resize:fit:863/0*jKqypwGzmDv7KDUZ.png)"
                        url: "https://miro.medium.com/v2/resize:fit:863/0*jKqypwGzmDv7KDUZ.png"
                        ""
                        """,
                    },
                },
                "required": ["query", "url"],
            },
        },
    },
]
