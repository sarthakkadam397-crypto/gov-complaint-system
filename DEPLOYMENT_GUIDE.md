# 🚀 Step-by-Step Guide: How to Make the Software Live Using GitHub

This guide explains how to host and deploy the **All-in-One Government Complaint Management System** online so that anyone can access it 24/7 from their mobile phone or laptop.

---

## 💡 Important Understanding: Two Live Deployment Options

| Feature | Option 1: GitHub Pages (Instant) | Option 2: GitHub + Render (Full-Stack) |
| :--- | :--- | :--- |
| **Hosting Platform** | **GitHub Pages** directly | **GitHub** linked to **Render.com** |
| **Setup Time** | 2 minutes (Easiest) | 5 minutes |
| **Cost** | 100% Free forever | 100% Free forever |
| **Backend Engine** | Client-Side Web Engine (`localStorage`) | Full Python Backend (`Flask` + `SQLite3`) |
| **Live URL Format** | `https://your-username.github.io/gov-complaint-system/` | `https://gov-complaint-system.onrender.com` |
| **Best For** | Academic viva, client demo, instant portfolio link | Full production with database persistence |

---

## 📦 STEP 1: Create a GitHub Repository (Required for Both)

1. Open your web browser and go to [GitHub.com](https://github.com/).
2. Log in (or click **Sign up** to create a free account if you don't have one).
3. In the top-right corner, click the **`+`** icon and select **"New repository"**.
4. Configure the repository:
   - **Repository name**: `gov-complaint-system` (or any name you like)
   - **Description**: `All-in-One Government Complaint Management System`
   - **Visibility**: Select **Public**
   - **Initialize repository**: Leave **all boxes unchecked** (do *not* add README, .gitignore, or license, because we already have them prepared).
5. Click the green **"Create repository"** button.

---

## 📤 STEP 2: Upload Your Project Files to GitHub

Since Git is not installed locally on your PC, you can upload the files directly via your web browser:

1. On your newly created GitHub repository page, click the link that says:  
   👉 **`uploading an existing file`**  
   *(found under the "Quick setup" section)*.
2. Open **File Explorer** on your Windows PC and navigate to:  
   `C:\Users\Abhishek\.gemini\antigravity\scratch\gov_complaint_system`
3. Select and drag all files and folders into the GitHub upload area in your browser:
   - `static/` (folder with `css/`, `js/`, `index.html`, `register.html`, `track.html`, `admin.html`, `transparency.html`)
   - `uploads/`
   - `app.py`
   - `app_flask.py`
   - `config.py`
   - `database.py`
   - `seed_data.py`
   - `test_system.py`
   - `Procfile`
   - `render.yaml`
   - `requirements.txt`
   - `start.bat`
   - `README.md`
   - `SYSTEM_ARCHITECTURE.md`
   - `index.html` *(root redirection page)*
4. Scroll down to **"Commit changes"**:
   - Commit message: `Initial commit: All-in-One Government Complaint Management System`
5. Click the green **"Commit changes"** button.  
   *(GitHub will take a few seconds to process and display all your project files).*

---

## 🌐 OPTION 1: Make It Live Instantly on GitHub Pages (2 Minutes)

Our frontend includes a built-in client-side data engine. When hosted on GitHub Pages, all features—including lodging grievances, receiving `GOV-2026-XXXXX` tracking IDs, visual 5-stage timeline updates, officer logins, and department forwarding—run smoothly right in the browser!

### How to Enable GitHub Pages:
1. On your GitHub repository page, click on the **Settings** tab (gear icon at the top menu).
2. On the left sidebar under the *Code and automation* section, click **Pages**.
3. Under **"Build and deployment"**:
   - **Source**: Select **`Deploy from a branch`**
   - **Branch**: Select **`main`** (or `master`)
   - **Folder**: Leave as **`/ (root)`**
4. Click **Save**.
5. Refresh the page after 1 to 2 minutes. You will see a green box:  
   🎉 **"Your site is live at https://<your-username>.github.io/gov-complaint-system/"**

Click that link—your application is now live on the global internet!

---

## ☁️ OPTION 2: Make It Live on Render with Full Python Backend (Free 24/7)

If you want the real Python backend, REST API, and SQLite database running in the cloud:

1. Open [Render.com](https://render.com/) and click **"Get Started"** or **"Log in"**.
2. Select **"Continue with GitHub"** to sign in with your GitHub account.
3. On the Render Dashboard, click the blue **"New +"** button and select **"Web Service"**.
4. Select **"Build and deploy from a Git repository"** and click **Next**.
5. Connect your GitHub repository (`gov-complaint-system`) and click **Connect**.
6. Fill in the settings:
   - **Name**: `gov-complaint-system`
   - **Region**: Choose the closest region (e.g., Singapore or Frankfurt)
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python seed_data.py
     ```
   - **Start Command**:
     ```bash
     gunicorn app_flask:app --bind 0.0.0.0:$PORT
     ```
   - **Instance Type**: Select **Free** ($0 / month)
7. Click **"Create Web Service"**.
8. Render will now automatically install dependencies, seed the database, and start your live server.
9. Within 2 minutes, your live URL will appear at the top:  
   👉 `https://gov-complaint-system.onrender.com`

---

## 🧪 Testing Your Live Site

Once your site is live (via GitHub Pages or Render):

1. **Citizen Portal**: Open the homepage, navigate through the 11 complaint categories, and check the emergency toll-free numbers.
2. **File a Grievance**: Go to **Register Complaint**, fill in details, upload an image or document, and submit. You will instantly receive an official `GOV-2026-XXXXX` tracking ID.
3. **Track Grievance**: Go to **Track Grievance**, paste your ID or type `GOV-2026-10492` to watch the 5-stage progress timeline stepper.
4. **Officer Login**: Go to **Officer Portal**, click any 1-click evaluation button (e.g., *Super Admin (IAS)* or *Cybercrime Dy. SP*), and update grievance statuses or forward complaints to other departments.
5. **Transparency Board**: Check live public statistics, department resolution percentages, and citizen satisfaction ratings.
