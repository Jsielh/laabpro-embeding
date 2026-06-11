# LaabPro Backend - FastAPI + LangChain
## Instalación

```bash
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```
## Ejecutar

```bash
python run.py
```

API disponible en: http://localhost:8000

##  Endpoints

- `GET /` - Info de la API
- `GET /health` - Health check
- `POST /api/chat/message` - Enviar mensaje al agente

### Ejemplo Request:
```json
{
  "message": "Hola, ¿cómo puedo inscribirme?",
  "language": "es",
  "user_email": "user@example.com"
}
```
### Ejemplo Response:
```json
{
  "message": "¡Hola! Para inscribirte...",
  "timestamp": "2026-02-25T18:30:00",
  "language": "es"
}
```
