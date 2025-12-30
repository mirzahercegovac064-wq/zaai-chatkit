# 🚀 Snabbguide: Lägg till ChatKit-widget på din Framer-hemsida

## ⚡ 3 enkla steg

### Steg 1: Lägg till ChatKit-scriptet

1. I Framer: **Settings** → **Site Settings** → **General** → **Custom Code**
2. I **Code to inject in `<head>`**, klistra in:

```html
<meta http-equiv="Cross-Origin-Embedder-Policy" content="credentialless" />
<script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>
```

3. Klicka **Save**

---

### Steg 2: Lägg till Dependencies

1. I **Site Settings** → **General** → scrolla ner till **Dependencies**
2. Lägg till: `@openai/chatkit-react`
3. Klicka **Save**

---

### Steg 3: Skapa Custom Code-komponenten

1. På din sida: **Insert** → **Code** → **Custom Code**
2. I **Properties** → **Edit Code**
3. **Radera allt** och klistra in koden från `framer/ChatWidget.jsx`
4. Klicka **Save**
5. I **Properties**: Sätt **Position** till **Fixed**, **Bottom**: `20px`, **Right**: `20px`

---

## ✅ Klart!

Öppna **Preview** och testa widgeten. Du bör se en grön chat-bubbla i nedre högra hörnet! 💬

---

## 📝 Viktigt

- Din backend-URL är redan konfigurerad i komponenten: `https://zaai-chatkit.onrender.com`
- Backend är redan uppdaterad för att tillåta Framer-domäner
- Om du behöver ändra något, redigera `framer/ChatWidget.jsx` och klistra in igen

---

## 🆘 Hjälp?

Se `FRAMER_IMPLEMENTATION_STEG.md` för detaljerad guide och felsökning.

