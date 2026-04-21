# 📋 PRE-DEMO CHECKLIST - RUN THIS BEFORE DEMO DAY

## ✅ SYSTEM REQUIREMENTS (Check in advance!)

- [ ] **OS**: Windows 10/11
- [ ] **Python**: 3.8+ installed (`python --version`)
- [ ] **Node.js**: 18+ installed (`node --version`)
- [ ] **Git**: Initialized and connected to GitHub
- [ ] **Docker**: Version 20+ installed (`docker --version`)
- [ ] **Docker Compose**: Version 2+ installed (`docker-compose --version`)
- [ ] **RAM**: 8GB+ available
- [ ] **Disk Space**: 5GB+ free
- [ ] **Internet Connection**: Stable and working

---

## 📦 DEPENDENCIES CHECK

### Backend Dependencies
```bash
cd dpdp-backend
# Check if venv exists
ls venv

# If not, create:
python -m venv venv

# Activate
venv\Scripts\activate

# Install/verify packages
pip install -r requirements.txt

# Verify key packages
python -c "import fastapi, sentence_transformers, torch, sqlalchemy"
# Should print nothing (no errors = success)
```

**Key Packages to Verify:**
- [ ] FastAPI (`pip show fastapi`)
- [ ] Sentence Transformers (`pip show sentence-transformers`)
- [ ] SQLAlchemy (`pip show sqlalchemy`)
- [ ] ReportLab (`pip show reportlab`)
- [ ] BeautifulSoup4 (`pip show beautifulsoup4`)

---

### Frontend Dependencies
```bash
cd dpdp-frontend
# Check if node_modules exists
ls node_modules

# If not, install:
npm install

# Verify key packages
npm list react tailwindcss vite
```

**Key Packages to Verify:**
- [ ] React (`npm list react`)
- [ ] Vite (`npm list vite`)
- [ ] Tailwind CSS (`npm list tailwindcss`)
- [ ] Axios (`npm list axios`)

---

## 🔧 CONFIGURATION CHECK

### Backend Config Files

**File 1: `.env`**
```bash
# Should contain:
MODEL_NAME=all-MiniLM-L6-v2
SIMILARITY_THRESHOLD=35
DATABASE_URL=sqlite:///./dpdp_compliance.db
```
- [ ] `.env` exists and properly configured

**File 2: `dpdp-backend/core/config.py`**
- [ ] Settings class reads from `.env`
- [ ] Defaults are reasonable

**File 3: `dpdp-backend/database/db.py`**
- [ ] Database URL configured
- [ ] SQLite path exists

### Frontend Config Files

**File 1: `vite.config.js`**
- [ ] Vite configuration exists
- [ ] React plugin configured

**File 2: `tailwind.config.js`**
- [ ] Tailwind configured
- [ ] Content paths correct

**File 3: `dpdp-frontend/src/services/api.js`**
- [ ] API base URL set to `http://localhost:8000`
- [ ] Axios configured

---

## 🚀 PRE-DEMO STARTUP TEST

Run this test 2 hours before demo!

### Test 1: Backend Startup (5 minutes)
```bash
cd dpdp-backend
venv\Scripts\activate
python -m uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

**Success Criteria:**
- [ ] No errors in terminal
- [ ] Server running on port 8000
- [ ] Can access `http://localhost:8000/docs`

**If Error:**
```bash
# Try this:
pip install --upgrade fastapi uvicorn
python -m uvicorn main:app --reload
```

---

### Test 2: Frontend Startup (5 minutes)
```bash
cd dpdp-frontend
npm run dev
```

**Expected Output:**
```
  VITE v8.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

**Success Criteria:**
- [ ] No errors in terminal
- [ ] Server running on port 5173
- [ ] Can access `http://localhost:5173` in browser

**If Port Error:**
```bash
# Find and kill process on 5173:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Try again:
npm run dev
```

---

### Test 3: Full System Test (10 minutes)

**Keep both running (in separate terminals)**

1. Open browser: `http://localhost:5173`
2. Check Frontend loads:
   - [ ] Page loads without errors
   - [ ] Navigation menu visible
   - [ ] Dashboard page accessible

3. Open new tab: `http://localhost:8000/docs`
4. Check Backend API:
   - [ ] Swagger UI loads
   - [ ] All endpoints visible
   - [ ] Try `/` GET endpoint (should return "DPDP Compliance API Running")

5. **Upload Test** (if you have a test file):
   - [ ] Go to `http://localhost:5173` Upload page
   - [ ] Upload a small policy text file
   - [ ] Wait for analysis
   - [ ] [ ] Results appear correctly

---

## 🐳 DOCKER TEST (Optional but Recommended)

### Test Docker Build
```bash
docker-compose build
```

**Expected Output:**
```
[+] Building 2.5s (45/45) FINISHED
 => => naming to dpdp-compliance-checker-backend:latest
 => => naming to dpdp-compliance-checker-frontend:latest
```

- [ ] Build completes without errors
- [ ] Two images created

### Test Docker Run
```bash
docker-compose up
```

**Expected Output:**
```
backend | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend | ➜  Local:   http://127.0.0.1:5173/
```

- [ ] Both containers start
- [ ] No port conflicts
- [ ] Both accessible in browser

---

## 📡 GIT VERIFICATION

```bash
# Check git status
git status

# Check recent commits
git log --oneline -5

# Check remote
git remote -v
```

**Success Criteria:**
- [ ] `.git` directory exists
- [ ] Remote pointing to GitHub
- [ ] At least 1 commit in history
- [ ] Clean working directory (no uncommitted changes)

---

## 🔐 NGROK SETUP (For Extra Mile Demo)

### Installation
```bash
# Download from: https://ngrok.com/download
# Or install via Chocolatey:
choco install ngrok
```

### Test ngrok
```bash
# Ensure backend is running on port 8000
ngrok http 8000
```

**Expected Output:**
```
Session Status                online
Forwarding                    https://xxxxx-yy.ngrok.io -> http://localhost:8000
Web Interface                 http://127.0.0.1:4040
```

**Success Criteria:**
- [ ] HTTPS URL generated
- [ ] URL is public and accessible
- [ ] Can access `https://xxxxx-yy.ngrok.io/docs`

---

## 📝 DEMO FILES READY

### Check Documentation
- [ ] `README.md` exists and readable
- [ ] `DEMO_SCRIPT.md` exists with exact commands
- [ ] Jenkinsfile exists and contains pipeline

### Prepare Sample Data
- [ ] Sample privacy policy text file ready
- [ ] Alternative: Website URL with privacy policy ready
- [ ] Backup URL: https://www.termsfeed.com/standard-terms-and-conditions/ (or similar)

---

## 🎬 DEMO ENVIRONMENT SETUP

### Browser Tabs (Open 3 tabs in advance)
- [ ] Tab 1: `http://localhost:5173` (Frontend - Ready)
- [ ] Tab 2: `http://localhost:8000/docs` (Backend Docs - Ready)
- [ ] Tab 3: GitHub Repository (backup info)

### Terminal Setup (Open 2 terminals)
- [ ] Terminal 1: Ready for backend
- [ ] Terminal 2: Ready for frontend

### Backup Terminals
- [ ] Terminal 3: Ready for Docker commands
- [ ] Terminal 4: Ready for ngrok commands

---

## ⚠️ COMMON ISSUES & QUICK FIXES

| Issue | Fix |
|-------|-----|
| Port 8000 in use | `netstat -ano \| findstr :8000` then `taskkill /PID <PID> /F` |
| Port 5173 in use | `netstat -ano \| findstr :5173` then `taskkill /PID <PID> /F` |
| Python package error | `pip install --force-reinstall -r requirements.txt` |
| npm error | `npm install` and `npm cache clean --force` |
| Docker error | `docker-compose down -v && docker-compose up --build` |
| Sentence Transformers slow | Model downloads on first run (5-10 min) - be patient |
| API 404 error | Check the base URL in `api.js` matches backend port |

---

## 📊 DEMO TIMING

- **Total Demo Duration**: 10-12 minutes
- **Intro**: 0:30
- **System Startup**: 1:00
- **Functionality**: 3:00
- **Git**: 1:00
- **Docker**: 2:00
- **Jenkins**: 1:00
- **ngrok**: 1:30
- **Buffer**: 1:00

---

## 🎯 FINAL CHECKLIST (30 minutes before demo)

- [ ] Both backend and frontend started and working
- [ ] Browser tabs ready with correct URLs
- [ ] Sample policy file ready for upload
- [ ] Git history visible
- [ ] Docker command ready to run
- [ ] Jenkins visible (if available)
- [ ] ngrok ready to launch
- [ ] All terminals visible/accessible
- [ ] Volume set appropriately
- [ ] Internet stable
- [ ] No notifications enabled (disable Slack, Teams, etc.)
- [ ] Full screen ready for presentation
- [ ] README.md visible
- [ ] DEMO_SCRIPT.md available for reference

---

## 🚨 EMERGENCY RECOVERY

### If Backend crashes during demo:
```bash
cd dpdp-backend
python -m uvicorn main:app --reload
```

### If Frontend crashes during demo:
```bash
cd dpdp-frontend
npm run dev
```

### If Docker fails:
```bash
docker-compose down
docker-compose up --build
```

### If port conflicts:
```bash
# Reset all:
netstat -ano | findstr :8000 && taskkill /PID <PID> /F
netstat -ano | findstr :5173 && taskkill /PID <PID> /F
docker-compose down
```

---

## 💡 TIPS FOR SUCCESS

1. **Test thoroughly** before demo day
2. **Have backups** of all commands in a notes file
3. **Keep terminals visible** - don't minimize them
4. **Speak clearly** and explain what you're showing
5. **Go slowly** - viewers need time to understand
6. **Be confident** - you know this project!
7. **Have internet ready** - ngrok needs connectivity
8. **Disable screensaver** - lock settings during demo
9. **Close unnecessary apps** - for better performance
10. **Practice this script** 2-3 times before demo

---

## 📞 LAST MINUTE HELP

If something goes wrong during demo:

1. **Stay calm** ✅
2. **Have a backup plan** (skip to next section) ✅
3. **Reference the README** for documentation ✅
4. **Show Git history** instead (always works) ✅
5. **Explain architecture** while troubleshooting ✅

---

**🔥 YOU'RE READY! NOW GO ACE THAT DEMO! 🔥**

*Document Created: April 21, 2026*
*Last Updated: Before Demo*
