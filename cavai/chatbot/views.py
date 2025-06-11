from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import time
import re
import os

# client = OpenAI(api_key=settings.OPENAI_API_KEY)
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
messages = [{"role": "system", "content": "You are a helpful assistant."}]

# assistant = client.beta.assistants.retrieve(settings.OPENAI_ASSISTANT_ID)
assistant = client.beta.assistants.retrieve(os.environ.get('OPENAI_ASSISTANT_ID'))
thread = client.beta.threads.create()

def clean_string(input_string):
    result = ""
    inside_parentheses = 0

    for char in input_string:
        if char == '【':
            inside_parentheses += 1
        elif char == '】':
            inside_parentheses -= 1
        elif inside_parentheses == 0:
            result += char

    return result

def ask_chatgpt(messages):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=100,
    n=1,
    )
    assistant_output = completion.choices[0].message.content
    return assistant_output

def ask_assistant(user_input):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    )
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        ).status

        if run_status == "completed":
            break

        time.sleep(1)  
        
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
    assistant_output = messages.data[0].content[0].text.value
    return clean_string(assistant_output)

# def chatbot(request):
#     global messages
#     if request.method == 'POST':
#         user_input = request.POST.get('message')
#         messages.append({"role": "user", "content": user_input})
#         assistant_output = ask_chatgpt(messages)
#         messages.append({"role": "assistant", "content": assistant_output})
#         return JsonResponse({'message':user_input, 'response': assistant_output})
#     return render(request, 'chatbot.html')

def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        # comment out the following line for debugging
        assistant_output = ask_assistant(user_input)
        # assistant_output = user_input
        return JsonResponse({'message':user_input, 'response': assistant_output})
    return render(request, 'chatbot.html')