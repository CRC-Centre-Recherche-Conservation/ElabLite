# ElabLite - Quick Installation Guide (Dev)

## 🚀 Get Started in 5 Minutes

### Option 1: Quick Start (Recommended)

```bash
# 1. Download ElabLite
git clone https://github.com/CRC-Centre-Recherche-Conservation/ElabLite.git
cd ElabLite

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```

That's it! Your browser will open automatically at `http://localhost:8501`

### Option 2: Using Virtual Environment (Best Practice)

**On macOS/Linux:**
```bash
# 1. Clone repository
git clone https://github.com/CRC-Centre-Recherche-Conservation/ElabLite.git
cd ElabLite

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
streamlit run app.py
```

**On Windows:**
```bash
# 1. Clone repository
git clone https://github.com/CRC-Centre-Recherche-Conservation/ElabLite.git
cd ElabLite

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
streamlit run app.py
```

## 📦 What Gets Installed?

The `requirements.txt` includes:
- **streamlit** (≥1.36.0) - Web framework
- **python-dateutil** - Date handling
- **validators** (≥0.28.1) - Input validation
- **streamlit-tags** (≥1.2.8) - Tag input widget
- **st-star-rating** (≥0.0.6) - Star rating widget
- **dill** (≥0.3.8) - Serialization

Total size: ~50 MB

## ✅ System Requirements

- **Python**: 3.10 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 512 MB minimum (1 GB recommended)
- **Disk Space**: 100 MB for installation + your data

## 🔍 Verify Installation

After running `streamlit run app.py`, you should see:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The application homepage should display:
- ElabLite logo
- "Welcome to ElabLite" message
- Sidebar with navigation menu

## ❗ Troubleshooting

### "Command not found: streamlit"

Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### "Port 8501 already in use"

Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### "ModuleNotFoundError"

Install missing dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Python Version Issues

Check your Python version:
```bash
python --version  # Should be 3.10 or higher
```

If needed, specify Python 3:
```bash
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

## 🎯 First Steps After Installation

1. **Create your first experiment**
   - Click "• New Experiment" in the sidebar
   - Upload or select a template
   
2. **Explore example templates**
   - Check the `templates/` folder (if available)
   - Or create your own JSON template

3. **Read the documentation**
   - `USER_GUIDE.md` - Comprehensive user guide
   - `README.md` - Project overview
   - In-app help tooltips

## 🔄 Updating ElabLite

To get the latest version:

```bash
cd ElabLite
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🆘 Getting Help

- **Documentation**: See `USER_GUIDE.md`
- **Issues**: [GitHub Issues](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/discussions)

## 🎉 You're Ready!

Start creating structured metadata for your scientific experiments!

---

**Need more details?** Check out:
- 📖 [Full README](README.md)
- 📚 [User Guide](USER_GUIDE.md)
- 🤝 [Contributing Guide](CONTRIBUTING.md)