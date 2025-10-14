![python version](https://shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20-blue) ![code quality](badges/quality.svg) ![Version](https://img.shields.io/badge/version-0.1.5--alpha-blue) ![License](https://img.shields.io/badge/license-MIT-green)

# ElabLite

**ElabLite** is a metadata generator tool for instrumental acquisition batches designed for use with electronic laboratory notebooks (ELN), specifically tailored for elabFTW instances. It simplifies the process of creating, managing, and exporting scientific experiment metadata through an intuitive desktop app offline.

## 🎯 Features

### Core Features
- 📝 **Template-based Metadata Creation**: Upload or select existing templates (JSON, CSV, ELN formats)
- 🔬 **Scientific Technique Management**: Pre-configured technical analysis codes (3D imaging, spectroscopy, chromatography, etc.)
- 📊 **Dataframe Editor**: Manage multiple analyses with spreadsheet-like interface
- 💾 **Auto-save System**: Automatic saving with manual save options
- 📦 **Batch Export**: Generate CSV files and ZIP archives for multiple experiments`
- 🏷️ **Comprehensive Metadata**: Support for titles, dates, authors, ratings, tags, and custom fields

### Supported File Formats`
- **Input**: JSON, CSV, ELN, ELABLITE
- **Output**: ELABLITE (custom format), CSV, ZIP archives

### Technical Analysis Support
Built-in support for 50+ analytical techniques including:
- Imaging: 3D, RGB, UV, IR, X-ray
- Spectroscopy: FTIR, Raman, XRF, Mass Spec
- Microscopy: SEM, Optical, Multiphoton
- Chromatography: GC-MS, LC-MS, CE-MS
- And many more...

## 🚀 Installation (User)

- **Platform**: Windows

You can download the latest version (.exe) of ElabLite [here](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/releases).

You can find an user guide [here](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/docs/user-guide.md).

## ⚙️ Installation (Development)

### 📋 Prerequisites

- Python 3.10 or higher
- pip package manager

### 1. Clone the Repository

```bash
git clone https://github.com/CRC-Centre-Recherche-Conservation/ElabLite.git
cd ElabLite
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🏃 Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### 📦 Packaging

This project uses [stlite@desktop](https://github.com/whitphx/stlite/blob/main/packages/desktop/README.md) to package the Streamlit application into an executable, standalone format.
The commands below install dependencies, generate the necessary files, and test the application locally before creating the final package.


```bash
npm install

npm run dump

npm run serve # To test locally

npm npm run app:dist
```

## 📖 Quick Start Guide

### Creating a New Experiment

1. **Select/Upload Template**
   - Navigate to "New Experiment" in the sidebar
   - Either upload a new template or select an existing one
   
2. **Fill Base Metadata** (Step 1)
   - Enter experiment title, date, and author
   - Select analytical technique
   - Add commentary, tags, and rating
   - Save your experiment

3. **Complete Experiment Metadata** (Step 2)
   - Fill in technique-specific metadata fields
   - All required fields are marked with *
   
4. **Manage Files Metadata** (Step 3)
   - Add rows for multiple analyses
   - Fill in IdentifierAnalysis and Object/Sample
   - Edit cells directly in the spreadsheet

5. **Export** (Step 4)
   - Save final version
   - Download .elablite file for archiving

### Loading an Existing Experiment

1. Navigate to "Load Experiment"
2. Import or select a saved .elablite file
3. Continue editing from where you left off

### Completing with Files

1. Go to "Select Experiment" → "Complete Experiment(s)"
2. Upload your .elablite preset
3. Upload associated data files
4. Map files to metadata rows
5. Generate filenames and download ZIP archive

## 📁 Project Structure

```
ElabLite/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── __version__.py             # Version information
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── models/
│   ├── forms.py               # Metadata form models
│   ├── technical.py           # Technical analysis definitions
│   └── validator.py           # Input validators
├── pages/
│   ├── 1-select_template.py   # Template selection page
│   ├── 1-load_template.py     # Load existing experiment
│   ├── 2-metadata_forms.py    # Main metadata editor
│   ├── 3-metadata_preset.py   # Preset selection
│   └── 4-metadata_management.py # File management
├── utils/
│   ├── manager.py             # File and data management
│   ├── menu.py                # Sidebar menu
│   ├── parser.py              # Template parsers
│   ├── save_manager.py        # Save operations
│   └── stepper.py             # Workflow stepper UI
└── static/
    └── icons/                 # Application icons
```

## 🔧 Configuration

### Streamlit Configuration

Edit `.streamlit/config.toml` to customize:

```toml
[client]
showSidebarNavigation = false

[server]
maxUploadSize = 100  # Maximum upload size in MB
```

## 💡 Key Concepts

### ELABLITE Format

ELABLITE is a custom serialized format that stores:
- Base metadata (title, date, author, etc.)
- Form data (technique-specific metadata)
- Template metadata structure
- Dataframe of analyses

### Metadata Fields

**Required Fields:**
- Title
- Date
- Author
- Technique

**Optional Fields:**
- Commentary
- Tags
- Rating (0-5 stars)
- Project information

### Number Fields with Units

Number fields support unit selection. Data is stored as:
```
value||unit
```
Example: `25.5||°C`

## 🔐 Data Storage

- **Temporary Storage**: Files stored in system temp directory (`tmp/templates/`)
- **Auto-save**: Experiments saved to `tmp/templates/presets/`
- **Retention**: Last 10 files kept automatically
- **Download**: Manual export for permanent archiving

## 🐛 Troubleshooting

### Common Issues

**Template not loading:**
- Check file format (JSON, CSV, ELN, ELABLITE) -> You need to export model from your instance elabFTW
- Check file permissions
- Verify file is not corrupted

**Files not uploading:**
- Check file size (max 100MB per file)
- Verify file permissions

**Save not working:**
- Ensure all required fields are filled
- Check disk space availability

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Developed for the Centre de Recherche et de Conservation (CRC) - Equipex Biblissima+
- Built with [Streamlit](https://streamlit.io/)
- Designed for use with [elabFTW](https://www.elabftw.net/)

## 📞 Support

- 🐛 [Report a Bug](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/issues/new?assignees=rayondemiel&labels=bug&projects=CRC-Centre-Recherche-Conservation%2F3&template=BUG-REPORT.yml&title=%5BBug%5D%3A+)
- 📖 [Documentation](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/docs/)
