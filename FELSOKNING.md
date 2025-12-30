# Felsökning: Chatten öppnas inte

## Steg 1: Kontrollera att backend körs

Öppna en ny terminal och kör:
```bash
curl http://localhost:8000/health
```

Du bör se:
```json
{"status":"ok","workflow_id_set":true,"api_key_set":true}
```

**Om det inte fungerar:**
- Starta backend: `cd backend && python server.py`
- Kontrollera att `.env`-filen finns och har rätt värden

## Steg 2: Kontrollera webbläsarens konsol

1. Öppna webbläsarens Developer Tools (F12 eller Cmd+Option+I)
2. Gå till **Console**-fliken
3. Klicka på chat-knappen
4. Se vilka meddelanden som visas

**Vad du letar efter:**
- `Fetching new client secret from backend...` - betyder att frontend försöker kontakta backend
- `Client secret received successfully` - betyder att det fungerade!
- Felmeddelanden i rött - dessa berättar vad som är fel

## Steg 3: Kontrollera Network-fliken

1. I Developer Tools, gå till **Network**-fliken
2. Klicka på chat-knappen
3. Leta efter en request till `/api/chatkit/session`
4. Klicka på den requesten
5. Gå till **Response**-fliken

**Vad du bör se:**
```json
{"client_secret":"secret_..."}
```

**Om du ser ett fel:**
- Status 500 = Backend-problem, kolla backend-terminalen
- Status 404 = Backend körs inte eller proxy fungerar inte
- Status 502/503 = Backend är nere

## Steg 4: Kontrollera backend-terminalen

I terminalen där backend körs bör du se:
```
Creating ChatKit session with workflow_id: wf_..., user: ...
Session created successfully: sess_...
```

**Om du ser fel:**
- "OPENAI_API_KEY environment variable is not set" → Lägg till den i `.env`
- "CHATKIT_WORKFLOW_ID environment variable is not set" → Lägg till den i `.env`
- Andra fel → Läs felmeddelandet noggrant

## Vanliga problem

### Problem: Inget händer när jag klickar på knappen
**Lösning:**
1. Öppna Console i Developer Tools
2. Se om det finns några JavaScript-fel
3. Kontrollera att React-appen laddades korrekt

### Problem: Chatten öppnas men är tom
**Lösning:**
1. Kolla Console för felmeddelanden
2. Kolla Network-fliken för att se om `/api/chatkit/session` fungerade
3. Se om ChatKit-scriptet laddades (Network-fliken, sök efter "chatkit.js")

### Problem: "Failed to create session: 500"
**Lösning:**
1. Kolla backend-terminalen för felmeddelanden
2. Verifiera att `.env`-filen har rätt värden
3. Kontrollera att OpenAI API-nyckeln är giltig

### Problem: "Kunde inte ansluta till chatten"
**Lösning:**
1. Kontrollera att backend körs på port 8000
2. Testa: `curl http://localhost:8000/health`
3. Om det inte fungerar, starta backend igen




