# Migração do banco do Render para Supabase

Este projeto Django já lê `DATABASE_URL` via variável de ambiente (django-environ).  
Para migrar, basta apontar essa variável para o PostgreSQL do Supabase.

## 1) Criar projeto no Supabase

1. Acesse [https://supabase.com](https://supabase.com) e faça login.
2. Clique em **New project**.
3. Defina:
   - **Organization**
   - **Project name**
   - **Database password** (guarde esta senha)
   - **Region** (escolha a mais próxima do Render)
4. Aguarde o projeto ficar pronto.

## 2) Obter a connection string do PostgreSQL

1. No painel do Supabase, abra **Project Settings** → **Database**.
2. Em **Connection string**, selecione o formato URI/SQLAlchemy/psql (qualquer URI PostgreSQL completa serve).
3. Use o host no formato:
   - `db.<project-ref>.supabase.co`
4. Exemplo de `DATABASE_URL`:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.<your-project-ref>.supabase.co:5432/postgres?sslmode=require
```

> Se a senha tiver caracteres especiais, use URL encoding.

## 3) Configurar no Render

1. Abra seu serviço backend no Render.
2. Vá em **Environment**.
3. Crie/edite a variável:
   - `DATABASE_URL=<sua-uri-do-supabase>`
4. Salve e faça **Manual Deploy** (ou aguarde o próximo deploy).

## 4) Migrar dados existentes (se houver)

Se você já tinha dados no banco antigo do Render:

1. Exporte o banco antigo:

```bash
pg_dump "<DATABASE_URL_ANTIGA_RENDER>" > backup_render.sql
```

2. Importe no Supabase:

```bash
psql "<DATABASE_URL_SUPABASE>" < backup_render.sql
```

3. Garanta que as migrações Django estão aplicadas:

```bash
python manage.py migrate
```

## 5) Testar conexão

1. No ambiente local, configure `DATABASE_URL` no `.env` com a URI do Supabase.
2. Rode:

```bash
python manage.py migrate
python manage.py runserver
```

3. Valide:
   - Endpoints da API respondendo normalmente
   - Operações de leitura/escrita funcionando
4. No Render, confira os logs após deploy para garantir que não houve erro de conexão ao PostgreSQL.
