# Konkreta steg för att fixa ChatKit

## Steg 1: Skapa .env-fil

Skapa en fil som heter `.env` i projektets rotmapp (`/Users/mirzahercegovac/zaai-chatkit/.env`)

Innehåll i filen:
```
OPENAI_API_KEY=din_riktiga_api_nyckel_här
CHATKIT_WORKFLOW_ID=wf_ditt_riktiga_workflow_id_här
```

**Viktigt:**
- `OPENAI_API_KEY` ska börja med `sk-`
- `CHATKIT_WORKFLOW_ID` ska börja med `wf_`
- Inga citattecken runt värdena

## Steg 2: Starta backend

Öppna en terminal och kör:

```bash
cd /Users/mirzahercegovac/zaai-chatkit/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

Backend startar på: http://localhost:8000

**Kontrollera att det fungerar:**
- Öppna http://localhost:8000/health i webbläsaren
- Du bör se: `{"status":"ok","workflow_id_set":true,"api_key_set":true}`

## Steg 3: Starta frontend

Öppna en NY terminal (låt backend köra) och kör:

```bash
cd /Users/mirzahercegovac/zaai-chatkit/frontend
npm install
npm run dev
```

Frontend startar på: http://localhost:3000 (eller 5173)

## Steg 4: Testa

1. Öppna http://localhost:3000 i webbläsaren
2. Du bör se en grön chat-knapp nere till höger
3. Klicka på knappen
4. Chatten ska öppnas

## Om det inte fungerar

### Problem: Backend ger fel när den startar
- Kontrollera att `.env`-filen finns i rätt mapp
- Kontrollera att värdena i `.env` är korrekta (inga citattecken)

### Problem: Chatten öppnas inte
1. Öppna Developer Tools i webbläsaren (F12 eller Cmd+Option+I)
2. Gå till Console-fliken
3. Se vilka felmeddelanden som visas
4. Gå till Network-fliken och leta efter `/api/chatkit/session`
5. Klicka på den requesten och se vad den returnerar

### Problem: Backend säger "workflow_id_set: false"
- Dubbelkolla att `CHATKIT_WORKFLOW_ID` är satt i `.env`-filen
- Dubbelkolla att det börjar med `wf_`
- Starta om backend efter att ha ändrat `.env`




