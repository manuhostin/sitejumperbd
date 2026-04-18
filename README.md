# SiteJumper

Um projeto Django.

## Configuração

1. Crie um ambiente virtual: `python -m venv .venv`
2. Ative o ambiente: `.venv\Scripts\activate` (Windows)
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute as migrações: `python manage.py migrate`
5. Rode o servidor: `python manage.py runserver`

## Deploy (Render + Vercel)

- Copie `.env.example` para `.env` e ajuste os valores.
- Gere `SECRET_KEY` aleatória (ex.: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`).
- No Render, configure: `DATABASE_URL`, `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG=False`, `CORS_ALLOWED_ORIGINS`.
- No frontend (Vercel), configure `VITE_API_URL` (veja `frontend.vercel.env.example`).
