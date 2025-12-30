# 🚀 Deploya uppdaterad backend till Render

## Alternativ 1: Via GitHub (Rekommenderat)

### Steg 1: Skapa git-repo lokalt

I Terminal, kör:

```bash
cd /Users/mirzahercegovac/zaai-chatkit
git init
git add .
git commit -m "Initial commit with ChatKit integration"
```

### Steg 2: Skapa GitHub-repo

1. Gå till [GitHub.com](https://github.com) och logga in
2. Klicka **New repository** (eller **+** → **New repository**)
3. Ge den ett namn (t.ex. `zaai-chatkit`)
4. **Viktigt:** Välj **Private** (så att din API-nyckel inte exponeras)
5. Klicka **Create repository**

### Steg 3: Koppla lokalt repo till GitHub

GitHub visar instruktioner, men kör detta i Terminal:

```bash
cd /Users/mirzahercegovac/zaai-chatkit
git remote add origin https://github.com/DITT-ANVÄNDARNAMN/zaai-chatkit.git
git branch -M main
git push -u origin main
```

(Ersätt `DITT-ANVÄNDARNAMN` med ditt GitHub-användarnamn)

### Steg 4: Koppla GitHub till Render

1. Gå till din Render-dashboard: https://dashboard.render.com
2. Välj din backend-service (t.ex. `zaai-chatkit`)
3. Gå till **Settings** → **Build & Deploy**
4. Under **Repository**, klicka **Connect GitHub**
5. Välj ditt repository (`zaai-chatkit`)
6. Render kommer automatiskt att deploya när du pushar till GitHub

### Steg 5: Pusha uppdateringen

När GitHub är kopplat till Render, kör:

```bash
cd /Users/mirzahercegovac/zaai-chatkit
git add backend/server.py
git commit -m "Update CORS for Framer domains"
git push
```

Render kommer automatiskt att deploya uppdateringen! 🎉

---

## Alternativ 2: Uppdatera direkt i Render (Snabbare)

Om du inte vill använda GitHub just nu:

### Steg 1: Öppna Render Dashboard

1. Gå till: https://dashboard.render.com
2. Välj din backend-service (`zaai-chatkit`)

### Steg 2: Redigera filen

1. Klicka på **Shell** (eller **Logs** → **Shell**)
2. Eller använd Render's **Web Editor** om det finns

### Steg 3: Uppdatera server.py

1. Öppna `backend/server.py`
2. Hitta CORS-sektionen (runt rad 16-30)
3. Ersätt med den nya koden:

```python
# Enable CORS for frontend
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
# Allow Framer domains and local development
# For production, we allow all origins to support Framer's dynamic domains
allowed_origins = [
    frontend_url,
    "http://localhost:3000",
    "http://localhost:5173",
]

# In production, allow all origins for Framer compatibility
# This allows any Framer domain (*.framer.website, *.framer.app) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (safe for public API endpoints)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

4. Spara filen
5. Render kommer automatiskt att deploya om

---

## ✅ Verifiera att det fungerar

Efter deploy, testa:

1. Öppna: `https://zaai-chatkit.onrender.com/health`
2. Du bör se: `{"status":"ok",...}`

3. Testa CORS genom att öppna Developer Tools i webbläsaren och köra:
```javascript
fetch('https://zaai-chatkit.onrender.com/api/chatkit/session', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
}).then(r => r.json()).then(console.log)
```

Om det fungerar utan CORS-fel, är allt klart! ✅

---

## 🎯 Rekommendation

Jag rekommenderar **Alternativ 1 (GitHub)** eftersom:
- ✅ Enklare att uppdatera i framtiden
- ✅ Versionshantering av din kod
- ✅ Automatisk deploy vid varje push
- ✅ Backup av din kod

Men om du vill ha det snabbt nu, använd **Alternativ 2**!

