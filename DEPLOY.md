# Deploy Django (Render) + Vue (Vercel)

## 1) Backend no Render
1. No Render, crie o serviço usando o `render.yaml` deste repositório.
   - Antes do primeiro deploy, substitua os placeholders `<your-frontend>` e `<your-backend>` pelos domínios reais.
2. Crie um projeto no Supabase e copie a connection string PostgreSQL do modo **Session** (use exatamente os valores do painel do Supabase).
   - O modo Session mantém conexão estável para o Django (evita limitações de pooling por transação em operações longas).
3. No serviço do Render, adicione a variável `DATABASE_URL` com a connection string do Supabase.
4. No deploy, o Render executa automaticamente:
   - `pip install -r requirements.txt`
   - `python manage.py migrate`
   - `python manage.py collectstatic --noinput`
   - `gunicorn sitejumper.wsgi:application`

## 2) Variáveis de ambiente do backend
Use como base o arquivo `.env.example`:
- `DEBUG=False`
- `SECRET_KEY=<valor seguro>`
- `DATABASE_URL=<connectionString PostgreSQL do Supabase (Session)>`
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
4. Valide localmente com `.env` contendo o `DATABASE_URL` do Supabase e execute `python manage.py migrate`.
