# Casos de prueba — Creación de tickets Zoho Desk

## Prerrequisitos

- Backend corriendo en `http://localhost:8000`
- Variables de entorno configuradas en `backend/.env`:
  - `ZOHO_MCP_SERVER_URL`
  - `ZOHO_DESK_ORG_ID`
  - `ZOHO_DESK_DEPARTMENT_ID`
- Conexión activa al servidor MCP de Zoho
- Chroma Cloud con documentos indexados para los locales `es`, `en`, `pt`

## Endpoint

```
POST /ask
Content-Type: application/json

{
  "query": "...",
  "locale": "es|en|pt",
  "session_id": "uuid"
}
```

## Cómo ejecutar las pruebas

```bash
cd backend
venv\Scripts\activate
python scripts/test_locales.py
```

---

## Caso 1 — [es] Ticket explícito con detalles

| Campo | Valor |
|-------|-------|
| **Locale** | `es` |
| **Query** | `"Tengo un problema con la plataforma, no puedo subir archivos. Mi correo es juan@test.com"` |
| **Tipo** | Reporte de problema |

**Resultado esperado:**
1. El agente identifica que es un reporte de problema
2. Si faltan datos (apellido, título), pregunta al usuario
3. Si tiene todos los datos, llama a `ZohoDesk_createTicket`
4. Devuelve confirmación con ID del ticket

---

## Caso 2 — [en] Ticket explícito con detalles

| Campo | Valor |
|-------|-------|
| **Locale** | `en` |
| **Query** | `"I have an issue, I can't upload files. My email is john@test.com"` |
| **Tipo** | Problem report |

**Resultado esperado:**
1. Agent identifies the problem report
2. If details are missing (last name, title), asks the user
3. If all data is present, calls `ZohoDesk_createTicket`
4. Returns confirmation with ticket ID

---

## Caso 3 — [pt] Ticket explícito com detalhes

| Campo | Valor |
|-------|-------|
| **Locale** | `pt` |
| **Query** | `"Tenho um problema, não consigo fazer upload. Meu email é joao@test.com"` |
| **Tipo** | Relato de problema |

**Resultado esperado:**
1. Agente identifica o relato de problema
2. Se faltarem dados (sobrenome, título), pergunta ao usuário
3. Se tiver todos os dados, chama `ZohoDesk_createTicket`
4. Retorna confirmação com ID do ticket

---

## Caso 4 — [es] Consulta general (no debe crear ticket)

| Campo | Valor |
|-------|-------|
| **Locale** | `es` |
| **Query** | `"¿Qué es LaabPro?"` |
| **Tipo** | Pregunta informativa |

**Resultado esperado:**
1. El agente usa la herramienta RAG (`retrieve_context`)
2. Responde basado en los documentos recuperados
3. NO llama a `ZohoDesk_createTicket`

---

## Caso 5 — [en] General query (should not create ticket)

| Campo | Valor |
|-------|-------|
| **Locale** | `en` |
| **Query** | `"What is LaabPro?"` |
| **Tipo** | Informational question |

**Resultado esperado:**
1. Uses `retrieve_context` tool
2. Answers based on retrieved documents
3. Does NOT call `ZohoDesk_createTicket`

---

## Caso 6 — [pt] Consulta geral (não deve criar ticket)

| Campo | Valor |
|-------|-------|
| **Locale** | `pt` |
| **Query** | `"O que é LaabPro?"` |
| **Tipo** | Pergunta informativa |

**Resultado esperado:**
1. Usa ferramenta `retrieve_context`
2. Responde com base nos documentos recuperados
3. NÃO chama `ZohoDesk_createTicket`

---

## Caso 7 — [es] Ticket sin detalles (debe pedir más info)

| Campo | Valor |
|-------|-------|
| **Locale** | `es` |
| **Query** | `"Ayuda"` |
| **Tipo** | Solicitud vaga |

**Resultado esperado:**
1. El agente NO crea el ticket inmediatamente
2. Pregunta al usuario por los detalles del problema (descripción, título, contacto)
3. Solo después de recibir la información completa, crea el ticket

---

## Caso 8 — [en] Vague request (should ask for details)

| Campo | Valor |
|-------|-------|
| **Locale** | `en` |
| **Query** | `"Help"` |
| **Tipo** | Vague request |

**Resultado esperado:**
1. Agent does NOT create the ticket immediately
2. Asks the user for problem details (description, title, contact)
3. Only after receiving complete information, calls `ZohoDesk_createTicket`

---

## Caso 9 — [pt] Pedido vago (deve pedir detalhes)

| Campo | Valor |
|-------|-------|
| **Locale** | `pt` |
| **Query** | `"Ajuda"` |
| **Tipo** | Solicitação vaga |

**Resultado esperado:**
1. Agente NÃO cria o ticket imediatamente
2. Pergunta ao usuário pelos detalhes do problema (descrição, título, contato)
3. Só após receber informações completas, chama `ZohoDesk_createTicket`

---

## Resumen

| # | Locale | Query | Comportamiento esperado |
|---|--------|-------|------------------------|
| 1 | `es` | "Tengo un problema... no puedo subir archivos..." | Crear ticket |
| 2 | `en` | "I have an issue... I can't upload files..." | Create ticket |
| 3 | `pt` | "Tenho um problema... não consigo fazer upload..." | Criar ticket |
| 4 | `es` | "¿Qué es LaabPro?" | Solo RAG |
| 5 | `en` | "What is LaabPro?" | RAG only |
| 6 | `pt` | "O que é LaabPro?" | Apenas RAG |
| 7 | `es` | "Ayuda" | Pedir detalles |
| 8 | `en` | "Help" | Ask for details |
| 9 | `pt` | "Ajuda" | Pedir detalhes |

## Notas

- Los casos 1-3 dependen de la conexión MCP con Zoho Desk. Si el MCP no está disponible, fallarán con error 500.
- Los casos 4-6 dependen de que haya documentos indexados en Chroma Cloud para cada locale.
- Los casos 7-9 prueban la lógica del agente para no crear tickets sin información suficiente.
