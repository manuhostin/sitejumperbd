# Deploy Django (Render) + Vue (Vercel)

## 1) Backend no Render
1. No Render, crie o serviço usando o `render.yaml` deste repositório.
2. O Render criará:
   - Web service Django
   - Banco PostgreSQL
3. No deploy, o Render executa automaticamente:
   - `pip install -r requirements.txt`
   - `python manage.py migrate`
   - `python manage.py collectstatic --noinput`
   - `gunicorn sitejumper.wsgi:application`

## 2) Variáveis de ambiente do backend
Use como base o arquivo `.env.example`:
- `DEBUG=False`
- `SECRET_KEY=<valor seguro>`
- `DATABASE_URL=<connectionString PostgreSQL do Render>`
- `ALLOWED_HOSTS=<seu-backend.onrender.com,...>`
- `CORS_ALLOWED_ORIGINS=https://<seu-front>.vercel.app`

O backend também aceita automaticamente origens `https://*.vercel.app` via regex CORS.

## 3) Frontend no Vercel
No projeto Vue no Vercel, configure:
- `VITE_API_URL=https://<seu-backend>.onrender.com`

## 4) Teste integração
1. Faça deploy backend no Render.
2. Faça deploy frontend no Vercel.
3. Valide chamadas da API no navegador (Network tab) e confirme resposta do backend remoto.
