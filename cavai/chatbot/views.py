from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os
import markdown
from pathlib import Path

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

try:
    os.environ['OPENAI_API_KEY']
except KeyError:
    raise KeyError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Load CV content once for context in chat prompts.
cv_path = Path(settings.BASE_DIR) / 'templates' / 'cv.md'
try:
    cv_text = cv_path.read_text(encoding='utf-8')
except FileNotFoundError:
    cv_text = ""

messages = [
    {
        "role": "system",
        "content": """
You are an assistant that answers questions about Diogo based on his curriculum vitae. He wants a job in research or data science. Give very concise answers and emphasize his strengths.

If asked for a download link give this: https://docs.google.com/document/d/1hdZrJUtET7AWqVCBfx6AnU3ar01d869yQSnnnipfDhY/

If the user introduces job details, job description or job role, compare it to Diogo's CV and confirm if he is a good fit or not with brief reasoning.

Minimize word count in all responses.

You are only allowed to answer questions about Diogo or his CV. If asked anything else, respond with "I can only answer questions about Diogo or his CV."
"""
    },
    {
        'role': 'user',
        'content': f"Here is Diogo's CV (in Markdown):\n\n{cv_text}",
    },
]

def ask_chatgpt(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200,
        n=1,
    )
    assistant_output = completion.choices[0].message.content
    return assistant_output

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
    global messages
    if request.method == 'POST':
        user_input = request.POST.get('message')
        messages.append({"role": "user", "content": user_input})
        assistant_output = ask_chatgpt(messages)
        messages.append({"role": "assistant", "content": assistant_output})
        return JsonResponse({'message': user_input, 'response': assistant_output})
    return render(request, 'chatbot.html')

def cv_view(request):
    try:
        with open(os.path.join(settings.BASE_DIR, 'templates/cv.md'), 'r') as f:
            cv_content = f.read()
        cv_html = markdown.markdown(cv_content)
    except FileNotFoundError:
        cv_html = "<p>CV file not found.</p>"

    return render(request, 'cv.html', {'cv_html': cv_html})

def vibe_coding_view(request):
    return render(request, 'vibe_coding.html')
