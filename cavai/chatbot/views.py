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
You are CV Assistant. Answer only using the provided CV content for Diogo. Audience is hiring managers for research or data science roles.

Style and constraints:
- Be concise and factual. Prefer one to three short sentences.
- When asked for a summary, use one crisp sentence.
- Use plain text with line breaks and hyphen bullets; no tables or code blocks.
- If asked for the CV or a download link, reply: "Check his CV at https://diogodebastos.vercel.app/cv ".
"""
    },
    {
        'role': 'user',
        'content': f"Context: Diogo's CV in Markdown below. Use only this as your source.\n\n{cv_text}",
    },
]
#- If job details/description are provided, assess fit with this exact multiline format:
#   Fit: <Strong/Moderate/Weak> — <one short reason>
#   Strengths:\n- <bullet 1>\n- <bullet 2>\n- <bullet 3>
#   Gaps:\n- <bullet 1>\n- <bullet 2>
# - If information is not in the CV, say: "Not in CV".
# - Refuse out-of-scope questions with: "I can only answer questions about Diogo or his CV."

def ask_chatgpt(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=250,
        # temperature=0.2,
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
        # Keep history compact: system + CV + last 8 exchanges
        if len(messages) > 2:
            base = messages[:2]
            tail = messages[2:][-16:]  # user+assistant pairs
            messages[:] = base + tail
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
