# ChatKit Widget Integration för Framer

Denna guide visar hur du integrerar ChatKit-widgeten på din Framer-hemsida.

## Metod 1: Custom Code Component (Rekommenderat)

Framer stöder React-komponenter via Custom Code. Detta är den enklaste metoden.

### Steg 1: Lägg till Custom Code-komponenten i Framer

1. Öppna ditt Framer-projekt
2. Gå till **Insert** → **Code** → **Custom Code**
3. Klistra in koden från `framer/ChatWidget.jsx` (se nedan)

### Steg 2: Lägg till script-taggar i Site Settings

1. Gå till **Site Settings** → **General** → **Custom Code**
2. I **Code to inject in `<head>`**, lägg till:

```html
<meta http-equiv="Cross-Origin-Embedder-Policy" content="credentialless" />
<script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  async
></script>
```

### Steg 3: Konfigurera API-endpoint

I Custom Code-komponenten, uppdatera `API_ENDPOINT` till din backend-URL:

```javascript
const API_ENDPOINT = 'https://din-backend-url.com/api/chatkit/session'
```

**Viktigt:** Din backend måste tillåta CORS-requests från din Framer-domän.

### Steg 4: Positionera widgeten

1. Välj Custom Code-komponenten
2. I **Properties**, sätt:
   - **Width**: Auto eller önskad bredd
   - **Height**: Auto eller önskad höjd
   - **Position**: Fixed (för att hålla den i hörnet)

## Metod 2: Via Embed Component (Enklare, men mindre flexibel)

Om du vill ha en ännu enklare lösning kan du använda en HTML-embed.

### Steg 1: Skapa en HTML-fil

Skapa en fil med widgeten och hosta den separat, sedan bädda in via iframe.

### Steg 2: Lägg till Embed-komponenten

1. Gå till **Insert** → **Media** → **Embed**
2. Lägg in URL:en till din widget

## Metod 3: Standalone Script (Rekommenderat för produktion)

För en produktionslösning kan du skapa en standalone-version som läses in via ett script.

### Implementering

Se `framer/standalone-widget.js` för en fristående version som kan läggas in via script-tag.

## Backend-konfiguration

Din backend måste:

1. **CORS-inställningar**: Tillåt requests från din Framer-domän
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://din-site.framer.website", "https://*.framer.website"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **API-endpoint**: Ha en endpoint på `/api/chatkit/session` som returnerar `client_secret`

3. **Environment variables**: 
   - `OPENAI_API_KEY`
   - `CHATKIT_WORKFLOW_ID`

## Felsökning

### Widgeten visas inte

1. Kontrollera att ChatKit-scriptet laddas (Network-fliken i DevTools)
2. Kontrollera Console för JavaScript-fel
3. Verifiera att Custom Code-komponenten är korrekt konfigurerad

### CORS-fel

1. Kontrollera att backend tillåter din Framer-domän
2. Testa med `curl` att backend svarar korrekt:
   ```bash
   curl -X POST https://din-backend-url.com/api/chatkit/session \
     -H "Content-Type: application/json"
   ```

### Backend kan inte nås

1. Kontrollera att backend är online
2. Verifiera att API_ENDPOINT är korrekt i Custom Code
3. Testa att öppna endpoint:en direkt i webbläsaren

## Exempel-kod

Se `framer/ChatWidget.jsx` för en komplett React-komponent som är optimerad för Framer.



