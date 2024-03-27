import json

import openai
from dotenv import load_dotenv

from function.functions_list import functions
from function.handle_image import handle_image
from function.search_youtube import search_youtube
from instructions.system_instructions import LLM_INSTRUCTIONS

load_dotenv()
client = openai
MODEL = "gpt-4-1106-preview"


def execute_function(function_name, tool_call):
    available_functions = {
        "search_youtube": search_youtube,
        "handle_image": handle_image,
    }
    if not function_name:
        return f"function {function_name} not available for calling"
    if function_name == "search_youtube":
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            query=function_args.get("query"),
        )
    if function_name == "handle_image":
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            url=function_args.get("url"),
            query=function_args.get("query"),
        )
    return function_response


def _extracted_from_chatbot_(messages, response_message, tool_calls):
    tool_messages = messages.copy()
    # Initialise another array for tool content
    tool_messages.append(response_message)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        print("Calling function: ", function_name)
        function_response = execute_function(function_name, tool_call)
        tool_messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(function_response),
            }
        )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=tool_messages,
        )
        final_response = second_response.choices[0].message.content
    chat_message = final_response

    messages.append({"role": "assistant", "content": chat_message})


def init_chat():
    return [
        {"role": "system", "content": LLM_INSTRUCTIONS},
    ]


def chatbot(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=functions,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    if tool_calls := response_message.tool_calls:
        _extracted_from_chatbot_(messages, response_message, tool_calls)
    else:
        chat_message = response_message.content
        messages.append({"role": "assistant", "content": chat_message})
    return messages


if __name__ == "__main__":
    messages = init_chat()
    while True:
        prompt = str(input("Enter your message (or 'quit' to exit): "))
        if prompt.lower() == "quit":
            break
        query = {"role": "user", "content": prompt}
        messages.append(query)
        messages = chatbot(messages)
        # print(messages)
        for message in messages:
            if message["role"] != "system":
                print(f"{message['role']}: \"{message['content']}\"")
    print("done")
