# Building a CV Chatbot with Django and Claude

## Why a chatbot for a CV?

Recruiters skim CVs in seconds. What if they could just ask questions instead? That's the idea behind cavai — a conversational interface powered by Claude that knows everything about my background.

## The stack

- **Django** for the backend — simple, batteries-included, perfect for a quick deploy
- **Claude Sonnet** via the Anthropic API — handles the conversation with my CV as context
- **Vercel** for hosting — free tier, zero config, just push and deploy
- **Markdown** for content — the CV and blog posts are plain `.md` files, converted to HTML on the fly

## How it works

The CV is loaded as a markdown file at server start. When a user sends a message, it's appended to a conversation history along with the CV content as system context. Claude responds based only on what's in the CV — no hallucinations about skills I don't have.

## Keeping it lean

No database for content. No CMS. No build step. Just markdown files in a templates folder, a few Django views, and the Anthropic SDK. The whole thing is under 500 lines of Python.

## What's next

- More blog posts about projects and experiments
- Maybe a voice interface?
- Exploring local models as an alternative to API calls

## Conclusion

Sometimes the best portfolio is one that talks back. If you're reading this, try asking the chatbot something — it might surprise you.
