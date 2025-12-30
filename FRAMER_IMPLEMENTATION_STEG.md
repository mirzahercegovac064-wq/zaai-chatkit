# 🎯 Steg-för-steg: Implementera ChatKit-widget på din Framer-hemsida

Din backend är redan deployad på: `https://zaai-chatkit.onrender.com`

## ✅ Steg 1: Lägg till ChatKit-scriptet i Framer

1. Öppna ditt Framer-projekt
2. Gå till **Settings** (kugghjulet uppe till höger) → **Site Settings**
3. Välj fliken **General** → scrolla ner till **Custom Code**
4. I rutan **Code to inject in `<head>`**, klistra in:

```html
<meta http-equiv="Cross-Origin-Embedder-Policy" content="credentialless" />
<script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  async
></script>
```

5. Klicka **Save** eller **Publish**

---

## ✅ Steg 2: Installera ChatKit React-paketet (om det behövs)

Framer stöder npm-paket via Custom Code. Om du får fel om att `@openai/chatkit-react` saknas:

1. I Framer, gå till **Settings** → **Site Settings** → **General**
2. Scrolla ner till **Dependencies**
3. Lägg till: `@openai/chatkit-react`
4. Klicka **Save**

---

## ✅ Steg 3: Skapa Custom Code-komponenten

1. I Framer, gå till sidan där du vill ha widgeten
2. Klicka på **Insert** (eller tryck `I`)
3. Välj **Code** → **Custom Code**
4. En ny komponent visas på sidan

5. I **Properties**-panelen (höger sida), klicka på **Edit Code**

6. **Radera all befintlig kod** och klistra in koden från `framer/ChatWidget.jsx`

7. Klicka **Save**

---

## ✅ Steg 4: Positionera widgeten

1. Välj Custom Code-komponenten på sidan
2. I **Properties**-panelen:
   - **Position**: Välj **Fixed**
   - **Bottom**: `20px`
   - **Right**: `20px`
   - **Width**: `Auto` eller lämna tomt
   - **Height**: `Auto` eller lämna tomt
   - **Z-index**: `1000` (för att ligga över annat innehåll)

---

## ✅ Steg 5: Testa widgeten

1. Klicka **Preview** (eller tryck `P`) för att se din sida
2. Du bör se en grön chat-bubbla i nedre högra hörnet 💬
3. Klicka på bubblan för att öppna chatten
4. Testa att skicka ett meddelande

---

## 🔧 Felsökning

### Widgeten visas inte

1. **Kontrollera att scriptet är laddat:**
   - Öppna Developer Tools (F12 eller Cmd+Option+I)
   - Gå till **Network**-fliken
   - Ladda om sidan
   - Leta efter `chatkit.js` - den ska laddas utan fel

2. **Kontrollera Console för fel:**
   - I Developer Tools, gå till **Console**-fliken
   - Leta efter röda felmeddelanden
   - Skicka mig felmeddelandena om du behöver hjälp

### CORS-fel

Om du ser fel om CORS (Cross-Origin Resource Sharing):
- Backend är redan konfigurerad för Framer-domäner
- Om du fortfarande får fel, kontrollera att din Framer-URL matchar mönstret `*.framer.website` eller `*.framer.app`

### Backend kan inte nås

1. Testa att backend är online:
   - Öppna: `https://zaai-chatkit.onrender.com/health`
   - Du bör se: `{"status":"ok",...}`

2. Testa session-endpoint:
   - Öppna Developer Tools → **Network**
   - Försök öppna chatten
   - Leta efter en request till `/api/chatkit/session`
   - Kontrollera svaret

---

## 🎨 Anpassa widgeten

### Ändra färger

I Custom Code-komponenten, leta efter `styles`-objektet och ändra:

```javascript
background: 'radial-gradient(circle at 0 0, #10a37f, #0c8b68)', // Knappens färg
background: 'linear-gradient(135deg, #0f172a, #020617)', // Header-färg
```

### Ändra position

I **Properties**-panelen för komponenten:
- **Bottom**: Avstånd från botten (t.ex. `20px`)
- **Right**: Avstånd från höger (t.ex. `20px`)

### Ändra storlek

I `styles.widgetContainer`:
```javascript
width: '380px',  // Bredd
height: '600px', // Höjd
```

### Ändra titel

I komponenten, leta efter:
```javascript
<div style={styles.widgetTitle}>
  ZAAI Assistant  // Ändra denna text
</div>
```

---

## 📱 Responsiv design

Widgeten är redan responsiv och anpassar sig automatiskt på mobil. Om du vill justera:

I `styles.widgetContainer`, lägg till media queries eller använd CSS-variabler.

---

## ✅ Checklista

Innan du publicerar, kontrollera:

- [ ] ChatKit-scriptet är lagt till i Site Settings
- [ ] Custom Code-komponenten är skapad och placerad
- [ ] Widgeten fungerar i Preview
- [ ] Backend svarar korrekt (testa `/health`)
- [ ] Inga fel i Console
- [ ] Widgeten fungerar på mobil (testa i Preview med mobilvy)

---

## 🚀 Publicera

När allt fungerar:

1. Klicka **Publish** i Framer
2. Widgeten kommer automatiskt att fungera på din publicerade sida!

---

## 💬 Behöver du hjälp?

Om du fastnar:
1. Kontrollera Developer Tools → Console för felmeddelanden
2. Testa backend: `https://zaai-chatkit.onrender.com/health`
3. Skicka mig felmeddelanden eller skärmdumpar så hjälper jag dig!

