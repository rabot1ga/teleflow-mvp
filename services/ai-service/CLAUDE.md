# AI Service — AI Context

## Responsibility
LLM operations: rewrite, summarize, classify, translate, generate tags.

## Database: None

## Operations
- rewrite: Рерайт текста
- summarize: Краткое изложение
- classify: Категоризация
- translate: Перевод
- generate_tags: Генерация тегов
- moderate: Проверка на спам

## Providers
- OpenAI (gpt-4o-mini, gpt-4o)
- Anthropic (claude-sonnet-4-20250514)
- Ollama (llama3, mistral)

## Celery Tasks
- `rewrite_text(text, prompt)`
- `summarize_text(text, max_words)`
- `classify_text(text, categories)`
