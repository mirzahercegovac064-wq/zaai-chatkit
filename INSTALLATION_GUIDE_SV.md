# Guide: Så här skapar du din ChatKit-widget

Detta är en steg-för-steg guide för att sätta upp din ChatKit-widget på din hemsida.

## 📋 Vad som redan finns i projektet

Projektet har redan:
- ✅ Backend-server (FastAPI) som skapar ChatKit-sessioner
- ✅ Frontend-komponent (React) med ChatWidget
- ✅ Alla nödvändiga beroenden och konfigurationer
- ✅ ChatKit-script inkluderat i HTML

## 🎯 Vad DU behöver göra

### Steg 1: Skaffa dina API-nycklar och Workflow ID

Du behöver två saker från OpenAI:

#### 1.1 OpenAI API-nyckel
1. Gå till [OpenAI Platform](https://platform.openai.com/api-keys)
2. Logga in på ditt konto
3. Skapa en ny API-nyckel eller använd en befintlig
4. Kopiera nyckeln (den börjar med `sk-`)

#### 1.2 ChatKit Workflow ID
1. Gå till [Agent Builder](https://platform.openai.com/agent-builder)
2. Skapa en ny agent workflow (eller använd en befintlig)
3. Efter att du skapat workflow:et, kopiera **Workflow ID** (det börjar med `wf_`)
4. Detta ID används för att koppla din widget till din agent

### Steg 2: Konfigurera miljövariabler

1. Skapa en `.env`-fil i projektets rotmapp (samma nivå som `README.md`)
2. Lägg till följande innehåll i filen:

```env
OPENAI_API_KEY=sk-din-api-nyckel-här
CHATKIT_WORKFLOW_ID=wf_ditt-workflow-id-här
FRONTEND_URL=http://localhost:3000
```

**Viktigt:** 
- Ersätt `sk-din-api-nyckel-här` med din riktiga API-nyckel
- Ersätt `wf_ditt-workflow-id-här` med ditt riktiga Workflow ID
- Lägg INTE filen i git (den är redan i `.gitignore`)

### Steg 3: Installera beroenden

#### Backend (Python)
```bash
cd backend
python3 -m venv venv  # Om du inte redan har ett virtual environment
source venv/bin/activate  # På macOS/Linux
# På Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend (Node.js)
```bash
cd frontend
npm install
```

### Steg 4: Starta servrarna

Du behöver köra både backend och frontend samtidigt.

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Om inte redan aktiverat
python server.py
```
Backend körs på: `http://localhost:8000`

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
Frontend körs på: `http://localhost:3000`

### Steg 5: Testa widgeten

1. Öppna din webbläsare och gå till `http://localhost:3000`
2. Du bör se en chat-bubbla i nedre högra hörnet
3. Klicka på bubblan för att öppna chatten
4. Testa att skicka ett meddelande

## 🔧 Vad JAG behöver från dig för att slutföra implementationen

För att säkerställa att allt fungerar perfekt, behöver jag följande information:

### 1. Har du redan skapat en Agent Workflow?
- [ ] Ja, jag har ett Workflow ID
- [ ] Nej, jag behöver hjälp att skapa en

**Om ja:** Skicka mig ditt Workflow ID (det börjar med `wf_`)

**Om nej:** Jag kan guida dig genom processen, eller så kan du följa [denna guide](https://platform.openai.com/docs/guides/agent-builder)

### 2. Har du en OpenAI API-nyckel?
- [ ] Ja, jag har en API-nyckel
- [ ] Nej, jag behöver skapa en

**Om ja:** Se till att den har rätt behörigheter för ChatKit

**Om nej:** Du kan skapa en på [OpenAI Platform](https://platform.openai.com/api-keys)

### 3. Var ska widgeten integreras?
- [ ] På en befintlig hemsida (vilken URL?)
- [ ] I detta projekt (localhost för nu)
- [ ] Annat (beskriv)

### 4. Anpassningar du vill ha?
- [ ] Anpassad färg/stil på widgeten
- [ ] Anpassad position (nu är den i nedre högra hörnet)
- [ ] Anpassad storlek
- [ ] Annat (beskriv)

## 🚨 Felsökning

### Widgeten visas inte
- Kontrollera att backend-servern körs (`http://localhost:8000`)
- Kontrollera att frontend-servern körs (`http://localhost:3000`)
- Öppna webbläsarens konsol (F12) och leta efter felmeddelanden
- Kontrollera att `.env`-filen finns och innehåller rätt värden

### "Failed to create session" fel
- Kontrollera att `OPENAI_API_KEY` är korrekt i `.env`
- Kontrollera att `CHATKIT_WORKFLOW_ID` är korrekt i `.env`
- Kontrollera att API-nyckeln har rätt behörigheter
- Kontrollera backend-loggarna för mer detaljerad felinformation

### CORS-fel
- Kontrollera att `FRONTEND_URL` i `.env` matchar din frontend-URL
- Om du använder en annan port, uppdatera `FRONTEND_URL` i `.env`

## 📚 Ytterligare resurser

- [ChatKit Dokumentation](https://platform.openai.com/docs/guides/chatkit)
- [Agent Builder Guide](https://platform.openai.com/docs/guides/agent-builder)
- [ChatKit React SDK](https://github.com/openai/chatkit-js)
- [ChatKit Python SDK](https://github.com/openai/chatkit-python)

## ✅ Checklista innan du börjar

Innan du kontaktar mig för hjälp, kontrollera att du har:

- [ ] Skapat en `.env`-fil i projektets rotmapp
- [ ] Lagt till din `OPENAI_API_KEY` i `.env`
- [ ] Lagt till ditt `CHATKIT_WORKFLOW_ID` i `.env`
- [ ] Installerat alla Python-beroenden (`pip install -r requirements.txt`)
- [ ] Installerat alla Node.js-beroenden (`npm install`)
- [ ] Startat backend-servern och den körs utan fel
- [ ] Startat frontend-servern och den körs utan fel
- [ ] Testat att öppna `http://localhost:3000` i webbläsaren

## 🎉 Nästa steg

När allt fungerar lokalt kan vi:
1. Anpassa widgetens utseende och beteende
2. Integrera widgeten på din riktiga hemsida
3. Konfigurera för produktion
4. Lägga till fler funktioner (t.ex. anpassade widgets, teman, etc.)

---

**Har du frågor eller behöver hjälp?** Skicka mig:
1. Ditt Workflow ID (om du har det)
2. Eventuella felmeddelanden du ser
3. Beskrivning av vad du vill uppnå

