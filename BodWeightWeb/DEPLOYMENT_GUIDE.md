# Streamlit App Deployment Guide

## Method 1: Streamlit Community Cloud (RECOMMENDED - FREE)

### Prerequisites
- GitHub account
- Your Streamlit app code
- Your CSV data file

### Step 1: Prepare Your Files

1. **Create a requirements.txt file** in the same directory as your app:
   ```
   streamlit
   pandas
   plotly
   ```

2. **Update the file path** in your app to use a relative path:
   
   Change this line in `BodyWeightStreamlit_app.py`:
   ```python
   file_path = r"C:\Users\Eric_Rash\OneDrive - Baylor University\AppliedPerformancProjects\CodingProjects\PythonScripts\New Repo\BodyWeightMaster.csv"
   ```
   
   To this:
   ```python
   file_path = "BodyWeightMaster.csv"
   ```

3. **Your project structure should look like:**
   ```
   your-project-folder/
   ├── BodyWeightStreamlit_app.py
   ├── BodyWeightMaster.csv
   └── requirements.txt
   ```

### Step 2: Create a GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the "+" icon in the top right → "New repository"
3. Name your repository (e.g., "bodyweight-dashboard")
4. Choose "Public" (required for free Streamlit deployment)
5. Click "Create repository"

### Step 3: Upload Your Files to GitHub

**Option A: Using GitHub Web Interface (Easiest)**
1. On your new repository page, click "uploading an existing file"
2. Drag and drop these files:
   - `BodyWeightStreamlit_app.py`
   - `BodyWeightMaster.csv`
   - `requirements.txt`
3. Click "Commit changes"

**Option B: Using Git Command Line**
```bash
cd your-project-folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 4: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in" and use your GitHub account
3. Click "New app"
4. Fill in the deployment form:
   - **Repository:** Select your repository (e.g., `your-username/bodyweight-dashboard`)
   - **Branch:** `main`
   - **Main file path:** `BodyWeightStreamlit_app.py`
   - **App URL:** Choose a custom URL (optional)
5. Click "Deploy!"

### Step 5: Wait for Deployment

- The app will take 2-5 minutes to deploy
- You'll see a build log showing the progress
- Once complete, you'll get a public URL like: `https://your-app-name.streamlit.app`

### Step 6: Share Your App

- Your app is now live!
- Share the URL with anyone
- The app will automatically update when you push changes to GitHub

---

## Method 2: Alternative Deployment Options

### A. Heroku (Free tier discontinued, but still available with paid plan)

1. Create a `Procfile`:
   ```
   web: streamlit run BodyWeightStreamlit_app.py --server.port=$PORT
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy using Heroku CLI

### B. Azure App Service

1. Create an Azure account
2. Use Azure CLI or Azure Portal
3. Create a Web App
4. Deploy using Git or Azure DevOps

### C. AWS EC2

1. Launch an EC2 instance
2. Install Python and dependencies
3. Run Streamlit with:
   ```bash
   streamlit run BodyWeightStreamlit_app.py --server.port=8501 --server.address=0.0.0.0
   ```

### D. Google Cloud Run

1. Create a `Dockerfile`
2. Build and push to Google Container Registry
3. Deploy to Cloud Run

### E. Local Network Deployment

To share on your local network:
```bash
streamlit run BodyWeightStreamlit_app.py --server.address=0.0.0.0 --server.port=8501
```
Access via `http://YOUR_LOCAL_IP:8501`

---

## Troubleshooting

### Issue: "File not found" error
**Solution:** Make sure your CSV file is in the same directory and you're using a relative path

### Issue: Missing dependencies
**Solution:** Ensure your `requirements.txt` includes all necessary packages

### Issue: App won't deploy on Streamlit Cloud
**Solution:** 
- Repository must be public
- Check that all files are committed to GitHub
- Verify file paths are relative, not absolute

### Issue: CSV file is too large
**Solution:** 
- GitHub has a 100MB file limit
- Consider using Git LFS for large files
- Or store data in Google Sheets/Database and read remotely

---

## Best Practices

1. **Use Environment Variables** for sensitive data:
   ```python
   import os
   file_path = os.getenv('DATA_PATH', 'BodyWeightMaster.csv')
   ```

2. **Add a .gitignore file:**
   ```
   __pycache__/
   *.pyc
   .env
   .streamlit/secrets.toml
   ```

3. **Use Streamlit Secrets** for sensitive configuration:
   - Add secrets in Streamlit Cloud dashboard
   - Access via `st.secrets`

4. **Monitor Usage:**
   - Streamlit Community Cloud has resource limits
   - Check your app analytics in the dashboard

---

## Next Steps

1. Customize your app URL
2. Add authentication if needed (using `streamlit-authenticator`)
3. Set up automatic GitHub Actions for testing
4. Add error handling and loading states
5. Consider upgrading to Streamlit for Teams for private apps

---

## Quick Reference Links

- [Streamlit Community Cloud](https://share.streamlit.io)
- [Streamlit Docs](https://docs.streamlit.io)
- [Deployment Tutorial](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [GitHub](https://github.com)
