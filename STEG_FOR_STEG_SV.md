# 📝 Steg-för-steg: Så här skapar du din ChatKit-widget

## 🎯 Översikt

Detta projekt är redan konfigurerat med all nödvändig kod! Du behöver bara:
1. Skaffa dina API-nycklar från OpenAI
2. Konfigurera en `.env`-fil
3. Starta servrarna
4. Testa widgeten

---

## ✅ Steg 1: Skaffa dina API-nycklar

### 1.1 OpenAI API-nyckel
1. Gå till: https://platform.openai.com/api-keys
2. Logga in på ditt OpenAI-konto
3. Klicka på "Create new secret key"
4. Kopiera nyckeln (den börjar med `sk-`)
5. **VIKTIGT:** Spara den säkert - du kan bara se den en gång!

### 1.2 ChatKit Workflow ID
1. Gå till: https://platform.openai.com/agent-builder
2. Klicka på "Create new workflow" eller använd en befintlig
3. Konfigurera din agent (lägg till instruktioner, verktyg, etc.)
4. Efter att du sparat workflow:et, kopiera **Workflow ID**
   - Det börjar med `wf_`
   - Exempel: `wf_68df4b13b3588190a09d19288d4610ec0df388c3983f58d1`

---

## ✅ Steg 2: Skapa `.env`-filen

1. Öppna projektets rotmapp i en textredigerare
2. Skapa en ny fil som heter `.env` (med punkt framför)
3. Lägg till följande innehåll:

```env
OPENAI_API_KEY=sk-din-riktiga-api-nyckel-här
CHATKIT_WORKFLOW_ID=wf_ditt-riktiga-workflow-id-här
FRONTEND_URL=http://localhost:3000
```

4. Ersätt värdena med dina riktiga nycklar
5. Spara filen

**⚠️ VIKTIGT:** 
- Lägg INTE `.env`-filen i git (den är redan ignorerad)
- Dela INTE din API-nyckel med någon

---

## ✅ Steg 3: Installera beroenden

### Backend (Python)
Öppna en terminal och kör:

```bash
cd backend
source venv/bin/activate  # Aktivera virtual environment
pip install -r requirements.txt
```

Om du inte har ett virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend (Node.js)
Öppna en **ny** terminal och kör:

```bash
cd frontend
npm install
```

---

## ✅ Steg 4: Starta servrarna

Du behöver köra både backend och frontend **samtidigt** i separata terminaler.

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python server.py
```

Du bör se:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Du bör se:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

---

## ✅ Steg 5: Testa widgeten

1. Öppna din webbläsare
2. Gå till: `http://localhost:3000`
3. Du bör se en grön chat-bubbla i nedre högra hörnet 💬
4. Klicka på bubblan för att öppna chatten
5. Skriv ett meddelande och testa att chatta!

---

## 🚨 Felsökning

### Problem: Backend startar inte
**Lösning:**
- Kontrollera att `.env`-filen finns i projektets rotmapp
- Kontrollera att `OPENAI_API_KEY` och `CHATKIT_WORKFLOW_ID` är korrekt ifyllda
- Kontrollera att du har aktiverat virtual environment: `source venv/bin/activate`

### Problem: Frontend startar inte
**Lösning:**
- Kontrollera att Node.js är installerat: `node --version` (ska vara 18+)
- Ta bort `node_modules` och kör `npm install` igen:
  ```bash
  rm -rf node_modules
  npm install
  ```

### Problem: Widgeten visas inte
**Lösning:**
- Öppna webbläsarens konsol (F12 → Console)
- Leta efter röda felmeddelanden
- Kontrollera att backend körs på port 8000
- Kontrollera att frontend körs på port 3000

### Problem: "Failed to create session"
**Lösning:**
- Kontrollera att din API-nyckel är korrekt i `.env`
- Kontrollera att ditt Workflow ID är korrekt (ska börja med `wf_`)
- Kontrollera backend-terminalen för detaljerade felmeddelanden
- Kontrollera att din API-nyckel har rätt behörigheter

---

## 📋 Checklista

Innan du kontaktar mig för hjälp, kontrollera:

- [ ] Jag har skapat en `.env`-fil i projektets rotmapp
- [ ] Jag har lagt till min `OPENAI_API_KEY` i `.env`
- [ ] Jag har lagt till mitt `CHATKIT_WORKFLOW_ID` i `.env`
- [ ] Jag har installerat Python-beroenden (`pip install -r requirements.txt`)
- [ ] Jag har installerat Node.js-beroenden (`npm install`)
- [ ] Backend-servern körs utan fel på port 8000
- [ ] Frontend-servern körs utan fel på port 3000
- [ ] Jag har testat att öppna `http://localhost:3000` i webbläsaren

---

## 🎉 Nästa steg

När allt fungerar kan vi:
- ✨ Anpassa widgetens utseende (färger, storlek, position)
- 🔧 Lägga till fler funktioner
- 🌐 Integrera på din riktiga hemsida
- 🚀 Konfigurera för produktion

---

## 💬 Behöver du hjälp?

Om du fastnar, skicka mig:
1. **Ditt Workflow ID** (om du har det)
2. **Felmeddelanden** du ser (från konsolen eller terminalen)
3. **Vad du har testat** hittills

**Jag kan hjälpa dig med:**
- Att skapa en Agent Workflow om du inte har en
- Att felsöka tekniska problem
- Att anpassa widgetens utseende
- Att integrera på din hemsida

