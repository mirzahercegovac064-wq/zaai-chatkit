# 🔒 Fixa GitHub Secret Scanning-fel

GitHub blockerar din push eftersom API-nycklar finns i dina commits. Här är hur du fixar det:

## ⚠️ Problem

GitHub har upptäckt att du försöker pusha filer med API-nycklar:
- `.env`
- `ENV_INNEHALL.txt`
- `backend/.env`

## ✅ Lösning: Ta bort secrets från git

### Steg 1: Ta bort filerna från git (men behåll dem lokalt)

Kör detta i Terminal:

```bash
cd /Users/mirzahercegovac/zaai-chatkit

# Ta bort filerna från git tracking
git rm --cached .env
git rm --cached ENV_INNEHALL.txt
git rm --cached backend/.env

# Kontrollera att .gitignore finns och innehåller .env
```

### Steg 2: Se till att .gitignore ignorerar dessa filer

Kontrollera att `.gitignore` innehåller:

```
.env
.env.local
.env.*.local
ENV_INNEHALL.txt
```

Om `.gitignore` inte finns eller saknar dessa rader, skapa/uppdatera den.

### Steg 3: Gör en ny commit

```bash
git add .gitignore
git commit -m "Remove API keys from git tracking"
```

### Steg 4: Pusha igen

```bash
git push -u origin main
```

---

## 🔄 Alternativ: Om du redan har pushat (och behöver rensa historiken)

Om du redan har pushat secrets tidigare, behöver du rensa git-historiken:

### Varning: Detta ändrar git-historiken!

```bash
# Ta bort filerna från alla commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env ENV_INNEHALL.txt backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (VIKTIGT: Detta skriver över historiken!)
git push origin --force --all
```

**⚠️ Varning:** Force push skriver över historiken. Använd bara om du är säker!

---

## ✅ Efter att du fixat det

1. Filerna finns fortfarande lokalt på din dator
2. De kommer INTE att pushas till GitHub
3. Du kan pusha koden utan problem

---

## 🎯 Snabbaste lösningen

Kör dessa kommandon i Terminal:

```bash
cd /Users/mirzahercegovac/zaai-chatkit

# Ta bort från git
git rm --cached .env ENV_INNEHALL.txt backend/.env

# Se till att .gitignore ignorerar dem
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.*.local" >> .gitignore
echo "ENV_INNEHALL.txt" >> .gitignore

# Commit ändringarna
git add .gitignore
git commit -m "Remove API keys from repository"

# Pusha igen
git push -u origin main
```

---

## 💡 Tips för framtiden

- **ALDRIG** committa `.env`-filer
- Använd alltid `.gitignore` för secrets
- Använd environment variables i Render istället för filer

