# LaabPro - Guía Rápida
cd backend
# Crear entorno virtual
python -m venv venv
# Activar (Windows)
venv\Scripts\activate
# Instalar
pip install -r requirements.txt
##  Configurar tu API Key
Edita `backend/.env`:
- Para **GPT**: Agrega tu `OPENAI_API_KEY=sk-...`
##  Ejecutar Todo

### Terminal 1 - Backend:
```bash
cd backend
venv\Scripts\activate
python run.py
```
 Backend en: http://localhost:8000


### Terminal 2 - Frontend:
```bash
cd frontend
pnpm dev
```

 Frontend en: http://localhost:5173

