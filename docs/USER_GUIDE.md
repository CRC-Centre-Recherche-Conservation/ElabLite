# ElabLite - Guide Utilisateur

## Table des Matières

1. [Introduction](#introduction)
2. [Premiers Pas](#premiers-pas)
3. [Workflows Principaux](#workflows-principaux)
4. [Guide des Fonctionnalités](#guide-des-fonctionnalités)
5. [Exemples Pratiques](#exemples-pratiques)
6. [FAQ](#faq)
7. [Bonnes Pratiques](#bonnes-pratiques)

---

## Introduction

### Qu'est-ce qu'ElabLite ?

ElabLite est une application web qui facilite la création et la gestion de métadonnées pour vos expériences scientifiques. Elle est particulièrement conçue pour s'intégrer avec les cahiers de laboratoire électroniques (ELN) comme elabFTW.

### À qui s'adresse ElabLite ?

- Chercheurs et techniciens de laboratoire
- Gestionnaires de données scientifiques
- Conservateurs et restaurateurs
- Analystes instrumentaux

### Avantages Clés

✅ **Gain de temps**: Créez des métadonnées structurées rapidement  
✅ **Standardisation**: Utilisez des templates réutilisables  
✅ **Traçabilité**: Sauvegarde automatique et historique  
✅ **Export facilité**: Génération de fichiers prêts pour elabFTW  
✅ **Gestion de masse**: Traitement de multiples analyses simultanément  

---

## Premiers Pas

### Installation et Lancement

1. **Télécharger ElabLite**
   ```bash
   git clone https://github.com/CRC-Centre-Recherche-Conservation/ElabLite.git
   cd ElabLite
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   streamlit run app.py
   ```

4. **Accéder à l'interface**
   - Votre navigateur s'ouvre automatiquement
   - URL: `http://localhost:8501`

### Interface Utilisateur

L'interface se compose de :

```
┌─────────────────────────────────────────────┐
│  Barre de navigation latérale (Sidebar)     │
│  - Menu principal                           │
│  - Options de navigation                    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Zone de contenu principale                 │
│  - Formulaires                              │
│  - Tableaux de données                      │
│  - Boutons d'action                         │
└─────────────────────────────────────────────┘
```

---

## Workflows Principaux

### Workflow 1: Créer une Nouvelle Expérience

**Objectif**: Créer une expérience avec métadonnées à partir d'un template

```
Template Selection → Base Metadata → Experiment Metadata → Files → Export
     (Page 1)           (Step 1)         (Step 2)         (Step 3)  (Step 4)
```

#### Page 1: Sélection du Template

1. Dans le menu latéral, cliquez sur **"• New Experiment"**

2. Choisissez une option:
   - **Upload Template**: Importer un nouveau fichier (JSON, CSV, ELN)
   - **Select existing template**: Utiliser un template déjà chargé

3. **Exemple de template JSON**:
   ```json
   {
     "metadata": "{
       \"extra_fields\": {
         \"temperature\": {
           \"type\": \"number\",
           \"value\": 20,
           \"unit\": \"°C\",
           \"units\": [\"°C\", \"K\", \"°F\"],
           \"description\": \"Temperature of analysis\",
           \"required\": true
         },
         \"method\": {
           \"type\": \"select\",
           \"value\": \"Method A\",
           \"options\": [\"Method A\", \"Method B\", \"Method C\"],
           \"required\": true
         }
       }
     }"
   }
   ```

4. Cliquez sur **"Validate"**

#### Step 1: Métadonnées de Base

**Barre de progression**: Vous êtes à l'étape 1/4

**Champs obligatoires** (marqués *):

- **Title**: Titre descriptif de l'expérience
  - Exemple: `XRF Analysis - Medieval Manuscript`

- **Date**: Date de réalisation
  - Utilisez le sélecteur de date

- **Author**: Nom de l'expérimentateur
  - Exemple: `Dr. Marie Dupont`

- **Technique**: Code de la technique analytique
  - Sélectionnez dans la liste déroulante (ex: XRF, FTIR, etc.)
  - Bouton **[+]**: Ajouter une nouvelle technique si nécessaire

**Champs optionnels**:

- **Project Config** (⚙️): Informations sur le projet
  - Project (longname): Nom complet du projet
  - Project (shortname): Acronyme (utilisé dans les noms de fichiers)
  - Project (URI): URL du projet

- **Commentary**: Notes et observations
  
- **Tags**: Mots-clés (max 8)
  - Exemple: `manuscript`, `pigment`, `blue`, `medieval`

- **Rating**: Évaluation de l'expérience (0-5 étoiles)

**Sauvegarde**:

Une fois les champs obligatoires remplis:

1. Section "💾 Save your experiment before continuing" apparaît

2. Options:
   - **💾 Update Current Save**: Mettre à jour le fichier actuel
   - **💾 Save As New**: Créer un nouveau fichier de sauvegarde

3. Entrez un nom de fichier descriptif
   - Exemple: `XRF_manuscript_2025`

4. Le fichier est sauvegardé en `.elablite`

**Navigation**: Cliquez sur **"Next ⏭️"** pour continuer

#### Step 2: Métadonnées de l'Expérience

**Barre de progression**: Vous êtes à l'étape 2/4

**Bouton Save persistant**: En haut de page, disponible à tout moment

Cette étape affiche les champs définis dans votre template:

**Exemple de champs**:

- Champs texte: Entrez des informations textuelles
- Champs numériques: Valeur + unité
  ```
  [25.5] [°C ▼]
  ```
- Listes déroulantes: Sélectionnez une option
- Cases à cocher: Cochez si applicable
- Dates: Utilisez le sélecteur
- Emails: Format validé automatiquement
- URLs: Format validé automatiquement

**Sauvegarde automatique**: L'indicateur en haut affiche "💾 Last saved Xs ago"

**Navigation**: 
- **"⏮️ Previous"**: Retour à l'étape 1
- **"Next ⏭️"**: Continuer (activé si tous les champs requis sont remplis)

#### Step 3: Éditeur de Fichiers

**Barre de progression**: Vous êtes à l'étape 3/4

**Objectif**: Gérer les métadonnées pour plusieurs analyses

**Interface**:

Le tableau affiche automatiquement:

| IdentifierAnalysis | Object/Sample | LocalisationAnalysis | [vos champs] |
|--------------------|---------------|----------------------|--------------|
| XRF0001            | Ms59f01v      | RedPigment           | 25.5°C       |

**Colonnes clés**:

1. **IdentifierAnalysis**: Identifiant unique de l'analyse
   - Format suggéré: `XRF0001`, `FTIR_0042`
   - Utilisé dans le nom de fichier final

2. **Object/Sample**: Identifiant de l'objet/échantillon
   - Format suggéré: `Ms59f01v`, `MNHN-X314`
   - Pas d'espaces (utilisez - ou CamelCase)

3. **LocalisationAnalysis**: Localisation de l'analyse
   - Exemple: `RedPigment`, `UpperLeft`, `Zone3`

**Actions disponibles**:

- **Add row** ➕: Ajoute une ligne pré-remplie avec les métadonnées de l'étape 2
- **Apply** ✅: Applique et sauvegarde les modifications
- Édition directe des cellules
- Suppression de lignes (bouton [×])
- Ajout de colonnes (bouton [+] en haut à droite)

**Workflow typique**:

1. Cliquez sur **"Add row"** pour chaque analyse
2. Remplissez `IdentifierAnalysis` et `Object/Sample`
3. Modifiez les autres champs si nécessaire
4. Cliquez sur **"Apply"** pour sauvegarder

**Navigation**: Cliquez sur **"Next ⏭️"**

#### Step 4: Export Final

**Barre de progression**: Vous êtes à l'étape 4/4 ✅

**Section 1: Save Working File**

Dernière sauvegarde avant export:

```
[💾 Save]  📁 Current: XRF_manuscript_2025.elablite
```

**Section 2: Download for Archive**

Télécharger une copie pour:
- Archivage permanent
- Partage avec collaborateurs
- Sauvegarde externe

```
[XRF_manuscript_2025          ] [📥 Download .elablite]
```

**Section 3: Recent Saves**

Liste des 10 dernières sauvegardes:

```
📋 Recent Saves
  📄 XRF_manuscript_2025.elablite (current) - 2025-10-14 15:30:00
  📄 FTIR_analysis_2025.elablite - 2025-10-13 10:45:00
  ...
```

---

### Workflow 2: Charger une Expérience Existante

**Objectif**: Reprendre le travail sur une expérience sauvegardée

```
Load Template → Continue Editing → Save → Export
   (Page 1)         (Steps 1-4)
```

#### Étapes:

1. Menu latéral → **"• Load Experiment"**

2. Choisissez:
   - **Import save**: Téléverser un fichier `.elablite`
   - **Load existing save**: Sélectionner dans la liste

3. Le fichier se charge avec toutes vos données
   - Métadonnées de base
   - Formulaire d'expérience
   - Tableau de fichiers

4. Modifiez ce que vous souhaitez

5. Sauvegardez vos changements

---

### Workflow 3: Compléter avec Fichiers de Données

**Objectif**: Mapper des fichiers de données à vos métadonnées et générer un ZIP pour elabFTW

```
Select Preset → Upload Files → Map Files → Generate Export
   (Page 3)        (Step 3)      (Step 3)      (Step 4)
```

#### Page 3: Sélection du Preset

1. Menu latéral → **"Select Experiment"**

2. Options:
   - **Upload experiment**: Importer un `.elablite`
   - **Select existing experiment**: Choisir dans la liste

3. Cliquez sur **"Validate"**

#### Step 1 & 2: Révision

Ces étapes affichent vos métadonnées en lecture seule pour vérification.

#### Step 3: Gestion des Fichiers

**Upload de fichiers**:

1. Cliquez sur **"Browse files"** ou glissez-déposez

2. Formats acceptés: Tous types de fichiers

3. Les fichiers sont associés automatiquement:
   - Le système cherche `IdentifierAnalysis` et `Object/Sample` dans les noms de fichiers
   - Exemple: `XRF0001_Ms59f01v_spectrum.txt` → ligne correspondante

**Tableau de mapping**:

| Filename | IdentifierAnalysis | Object/Sample | ... |
|----------|-------------------|---------------|-----|
| XRF0001_Ms59f01v_spectrum.txt | XRF0001 | Ms59f01v | ... |
| XRF0002_Ms59f02r_spectrum.txt | XRF0002 | Ms59f02r | ... |

**Mapping manuel**:

Si un fichier n'est pas trouvé automatiquement:
1. Cliquez dans la cellule `Filename`
2. Tapez ou collez le nom du fichier

#### Step 4: Téléchargement

**Préparation des noms de fichiers**:

1. **Sélectionnez les colonnes** à inclure dans les noms de fichiers:
   ```
   [☑] IdentifierAnalysis
   [☑] Object/Sample
   [☑] LocalisationAnalysis
   ```

2. **Cliquez sur "Validation filename"**

3. Exemple de résultat:
   ```
   Original: spectrum.txt
   Nouveau:  20251014_XRF_PROJECT_XRF0001_Ms59f01v_RedPigment.txt
   ```

   Format: `DATE_TECHNIQUE_PROJECT_SELECTED_COLUMNS.extension`

**Option de groupement**:

- **☐ Grouping analysis ?**: DÉCOCHÉ
  - Crée une expérience elabFTW par ligne
  - Recommandé: analyses indépendantes

- **☑ Grouping analysis ?**: COCHÉ
  - Toutes les analyses dans UNE expérience
  - Recommandé: série d'analyses liées

**Génération finale**:

1. Cliquez sur **"Generate files"**

2. Le système crée:
   ```
   Generating CSV...      ████████████ 
   Renaming files...      ████████████
   Zipping...             ████████████
   Process complete!
   ```

3. **Téléchargez le ZIP**:
   ```
   [Download Zip]  →  20251014_experiences.zip
   ```

**Contenu du ZIP**:

```
20251014_experiences.zip
├── experiences.csv          # Métadonnées pour elabFTW
├── logs_process.csv         # Traçabilité des opérations
└── data/                    # Fichiers renommés
    ├── 20251014_XRF_PROJECT_XRF0001_Ms59f01v.txt
    ├── 20251014_XRF_PROJECT_XRF0002_Ms59f02r.txt
    └── DATAFILE.txt         # Liste des fichiers (si groupé)
```

---

## Guide des Fonctionnalités

### Système de Sauvegarde

#### Auto-Save

- **Activation**: Automatique dès la première sauvegarde
- **Fréquence**: À chaque modification importante
- **Indicateur**: "💾 Last saved Xs ago"
- **Localisation**: `tmp/templates/presets/`

#### Save / Save As

**Save** (💾):
- Met à jour le fichier actuel
- Raccourci rapide
- Disponible partout dans l'application

**Save As** (💾):
- Crée un nouveau fichier
- Permet de renommer
- Utile pour les variantes

**Format ELABLITE**:
```python
{
  '@context': 'http://example.org/elablite/v1.0/',
  'metadata_base': {...},        # Métadonnées de base
  'form_data': {...},            # Formulaire d'expérience
  'template_metadata': {...},    # Structure du template
  'dataframe_metadata': [...]    # Tableau d'analyses
}
```

### Gestion des Templates

#### Formats Supportés

**JSON**:
```json
{
  "metadata": "{\"extra_fields\": {...}}"
}
```

**CSV**:
```csv
field_name,field_type,value,required
temperature,number,20,true
method,select,Method A,true
```

**ELABLITE**:
Format natif d'ElabLite (binaire sérialisé)

#### Structure d'un Template

```json
{
  "extra_fields": {
    "field_name": {
      "type": "text|number|select|date|checkbox|email|url|...",
      "value": "default_value",
      "description": "Help text",
      "required": true|false,
      "position": 1,
      "group_id": 0,
      
      // Pour 'select':
      "options": ["Option A", "Option B"],
      "allow_multi_values": false,
      
      // Pour 'number':
      "unit": "°C",
      "units": ["°C", "K", "°F"]
    }
  }
}
```

#### Types de Champs Disponibles

| Type | Description | Exemple |
|------|-------------|---------|
| `text` | Texte libre | "Sample description" |
| `number` | Nombre + unité | 25.5 °C |
| `select` | Liste déroulante | "Method A" |
| `date` | Sélecteur de date | 2025-10-14 |
| `datetime_local` | Date et heure | 2025-10-14 15:30 |
| `checkbox` | Case à cocher | ☑ |
| `email` | Email (validé) | user@lab.com |
| `url` | URL (validée) | https://lab.com |
| `time` | Heure | 15:30:00 |
| `radio` | Boutons radio | ◉ Option A ○ Option B |

### Techniques Analytiques

#### Techniques Pré-configurées (50+)

**Imagerie**:
- `3D`: Imagerie 3D
- `VIS`: Photographie RGB
- `IR`: Photographie infrarouge
- `RX`: Radiographie X
- `TOMO`: Tomographie X

**Spectroscopie**:
- `XRF`: Fluorescence X
- `IRTF`: FTIR
- `RAMAN`: Raman
- `REFL`: Réflectance
- `TRANS`: Transmittance

**Microscopie**:
- `MO`: Microscopie optique
- `MEB`: MEB/SEM
- `MPM`: Multiphoton

**Chromatographie**:
- `GC-MS`: Chromatographie gazeuse-MS
- `LC-MS`: Chromatographie liquide-MS
- `CE-MS`: Électrophorèse capillaire-MS

#### Ajouter une Technique

1. Cliquez sur le bouton **[+]** à côté du sélecteur de technique

2. Remplissez le formulaire:
   ```
   Code:          XRD
   English Name:  X-ray Diffraction
   French Name:   Diffraction des rayons X
   ```

3. Cliquez sur **"Add Technique"**

4. La technique est disponible immédiatement

### Éditeur de Dataframe

#### Opérations de Base

**Ajouter une ligne**:
- Bouton **"Add row"**: Ajoute une ligne pré-remplie
- Bouton **[+]** du tableau: Ajoute une ligne vide

**Modifier une cellule**:
- Double-cliquez ou cliquez simplement
- Tapez la nouvelle valeur
- Appuyez sur Entrée ou cliquez ailleurs

**Supprimer une ligne**:
- Cliquez sur **[×]** à gauche de la ligne

**Réorganiser les colonnes**:
- Glissez-déposez les en-têtes de colonnes

#### Opérations Avancées

**Copier-Coller**:
- Sélectionnez des cellules
- Ctrl+C / Ctrl+V fonctionne
- Utile pour dupliquer des lignes similaires

**Tri**:
- Cliquez sur l'en-tête de colonne
- Les données se trient automatiquement

**Recherche**:
- Utilisez Ctrl+F dans votre navigateur

### Validation des Données

#### Validation Automatique

**Emails**:
```
✅ user@lab.com
❌ user@lab       → Toast: "Invalid email"
```

**URLs**:
```
✅ https://lab.com
❌ lab.com        → Toast: "Invalid URL"
```

**Champs Requis**:
- Marqués avec *
- Bouton "Next" désactivé si incomplet

#### Indicateurs Visuels

- ✅ Champ valide et rempli
- ❌ Erreur de validation
- ⚠️ Avertissement
- 🎉 Succès d'une opération

---

## Exemples Pratiques

### Exemple 1: Analyse XRF sur Manuscrit

**Contexte**: Série d'analyses XRF sur un manuscrit médiéval

**Template**:
```json
{
  "extra_fields": {
    "voltage": {
      "type": "number",
      "value": 40,
      "unit": "kV",
      "units": ["kV"],
      "required": true
    },
    "current": {
      "type": "number",
      "value": 100,
      "unit": "µA",
      "units": ["µA", "mA"],
      "required": true
    },
    "acquisition_time": {
      "type": "number",
      "value": 60,
      "unit": "s",
      "units": ["s", "min"],
      "required": true
    },
    "filter": {
      "type": "select",
      "value": "Al 200µm",
      "options": ["No filter", "Al 200µm", "Al 500µm"],
      "required": false
    }
  }
}
```

**Step 1 - Base**:
```
Title: XRF Analysis - Avranches Ms 59
Date: 2025-10-14
Author: Dr. Smith
Technique: XRF
Tags: manuscript, medieval, pigment, blue
Rating: 4 stars
```

**Step 2 - Metadata**:
```
Voltage: 40 kV
Current: 100 µA
Acquisition time: 60 s
Filter: Al 200µm
```

**Step 3 - Files**:

| IdentifierAnalysis | Object/Sample | LocalisationAnalysis | voltage | current | acquisition_time | filter |
|--------------------|---------------|----------------------|---------|---------|------------------|--------|
| XRF0001 | Ms59f01v | BluePigment | 40 kV | 100 µA | 60 s | Al 200µm |
| XRF0002 | Ms59f01v | RedPigment | 40 kV | 100 µA | 60 s | Al 200µm |
| XRF0003 | Ms59f02r | GoldLeaf | 40 kV | 100 µA | 120 s | No filter |

**Step 4 - Export**:
- Save as: `XRF_Avranches_Ms59_2025.elablite`
- Download for archiving

---

### Exemple 2: Série FTIR avec Fichiers

**Contexte**: Analyses FTIR sur échantillons de peinture + export avec fichiers

**Workflow complet**:

1. **Créer l'expérience** (Pages 1-2, Steps 1-4)
   - Template avec champs FTIR
   - Métadonnées de base
   - 10 analyses dans le tableau
   - Save as: `FTIR_paintings_batch1.elablite`

2. **Compléter avec fichiers** (Page 3-4)
   - Load: `FTIR_paintings_batch1.elablite`
   - Upload 10 fichiers de spectre (`.txt`)
   - Mapping automatique réussi ✅
   - Sélection colonnes: `IdentifierAnalysis`, `Object/Sample`
   - Validation filename
   - Generate files
   - Download ZIP

**Résultat**:

```
20251014_experiences.zip (2.3 MB)
├── experiences.csv (10 lignes)
├── logs_process.csv
└── FTIR_paintings_batch1/
    ├── 20251014_FTIR_PROJ_FTIR001_Paint01.txt
    ├── 20251014_FTIR_PROJ_FTIR002_Paint02.txt
    ├── ...
    └── 20251014_FTIR_PROJ_FTIR010_Paint10.txt
```

**Import dans elabFTW**:
1. Extraire le ZIP
2. Importer `experiences.csv`
3. Les fichiers sont liés automatiquement

---

### Exemple 3: Template Réutilisable

**Objectif**: Créer un template pour des analyses récurrentes

**Création du Template JSON**:

```json
{
  "metadata": "{
    \"extra_fields\": {
      \"instrument\": {
        \"type\": \"select\",
        \"value\": \"Bruker Alpha\",
        \"options\": [\"Bruker Alpha\", \"Nicolet iS50\", \"Perkin Elmer\"],
        \"required\": true,
        \"position\": 1
      },
      \"resolution\": {
        \"type\": \"select\",
        \"value\": \"4\",
        \"options\": [\"2\", \"4\", \"8\", \"16\"],
        \"description\": \"Spectral resolution in cm-1\",
        \"required\": true,
        \"position\": 2
      },
      \"scans\": {
        \"type\": \"number\",
        \"value\": 32,
        \"description\": \"Number of scans\",
        \"required\": true,
        \"position\": 3
      },
      \"range_start\": {
        \"type\": \"number\",
        \"value\": 400,
        \"unit\": \"cm-1\",
        \"units\": [\"cm-1\"],
        \"description\": \"Start of spectral range\",
        \"required\": true,
        \"position\": 4,
        \"group_id\": 1
      },
      \"range_end\": {
        \"type\": \"number\",
        \"value\": 4000,
        \"unit\": \"cm-1\",
        \"units\": [\"cm-1\"],
        \"description\": \"End of spectral range\",
        \"required\": true,
        \"position\": 5,
        \"group_id\": 1
      },
      \"atr_crystal\": {
        \"type\": \"select\",
        \"value\": \"Diamond\",
        \"options\": [\"Diamond\", \"ZnSe\", \"Ge\"],
        \"required\": false,
        \"position\": 6,
        \"group_id\": 2
      },
      \"pressure\": {
        \"type\": \"select\",
        \"value\": \"Medium\",
        \"options\": [\"Light\", \"Medium\", \"Heavy\"],
        \"description\": \"ATR pressure\",
        \"required\": false,
        \"position\": 7,
        \"group_id\": 2
      },
      \"notes\": {
        \"type\": \"text\",
        \"value\": \"\",
        \"description\": \"Additional observations\",
        \"required\": false,
        \"position\": 8
      }
    }
  }"
}
```

**Utilisation**:
1. Sauvegarder comme `FTIR_ATR_template.json`
2. Upload dans ElabLite
3. Le template apparaît dans "Select existing template"
4. Réutilisable pour toutes les analyses FTIR-ATR

---

## FAQ

### Questions Générales

**Q: Mes données sont-elles sécurisées ?**  
R: Les données sont stockées localement sur votre machine dans le dossier temporaire du système. Aucune donnée n'est envoyée à un serveur externe.

**Q: Puis-je utiliser ElabLite sans connexion Internet ?**  
R: Oui, une fois installé, ElabLite fonctionne entièrement en local.

**Q: Combien de fichiers puis-je traiter en une fois ?**  
R: La limite est de 100 MB par fichier. Vous pouvez uploader autant de fichiers que nécessaire (limité par la mémoire de votre machine).

### Formats et Templates

**Q: Quel format de template dois-je utiliser ?**  
R: JSON est recommandé pour sa flexibilité. ELABLITE pour sauvegarder des expériences complètes.

**Q: Puis-je modifier un template existant ?**  
R: Oui, modifiez le fichier JSON et rechargez-le, ou sauvegardez une variante avec "Save As".

**Q: Comment gérer des champs avec des listes de valeurs multiples ?**  
R: Utilisez `"allow_multi_values": true` dans votre template pour les champs `select`.

### Sauvegarde et Export

**Q: Quelle est la différence entre Save et Download ?**  
R: 
- **Save**: Sauvegarde dans le dossier temporaire pour continuer le travail
- **Download**: Télécharge une copie pour archivage permanent

**Q: Où sont stockés mes fichiers sauvegardés ?**  
R: Dans `tmp/templates/presets/` sur votre système. Utilisez Download pour une copie permanente.

**Q: Combien de temps les fichiers sont-ils conservés ?**  
R: Les 10 fichiers les plus récents sont conservés. Les anciens sont automatiquement supprimés.

**Q: Puis-je récupérer un fichier supprimé ?**  
R: Non, d'où l'importance d'utiliser Download pour l'archivage.

### Gestion des Fichiers

**Q: Les fichiers uploadés sont-ils stockés ?**  
R: Non, ils sont en mémoire temporaire. Ils sont perdus si vous changez de page ou rechargez.

**Q: Comment gérer des fichiers avec des noms similaires ?**  
R: Utilisez les colonnes IdentifierAnalysis et Object/Sample de manière unique pour différencier.

**Q: Que faire si le mapping automatique échoue ?**  
R: Remplissez manuellement la colonne Filename dans le tableau.

### Techniques et Métadonnées

**Q: Ma technique n'est pas dans la liste**  
R: Cliquez sur [+] pour ajouter une nouvelle technique. Elle sera disponible immédiatement.

**Q: Puis-je avoir des métadonnées différentes par ligne ?**  
R: Non dans le workflow "Complete Experiment". Utilisez "New Experiment" avec un tableau pour des variations.

**Q: Comment gérer des unités personnalisées ?**  
R: Modifiez le template JSON pour ajouter vos unités dans la liste `"units"`.

### Erreurs Courantes

**Q: "Please fill all required fields"**  
R: Vérifiez que tous les champs marqués * sont remplis dans Step 1.

**Q: "Invalid email" / "Invalid URL"**  
R: Vérifiez le format. Email: `user@domain.com`, URL: `https://site.com`

**Q: "Filename validation failed"**  
R: Assurez-vous que toutes les lignes ont un fichier dans la colonne Filename.

**Q: Le bouton "Next" est désactivé**  
R: Un ou plusieurs champs requis ne sont pas remplis. Regardez les champs marqués *.

---

## Bonnes Pratiques

### Organisation des Données

#### Nommage des Identifiants

**IdentifierAnalysis**:
```
✅ FTIR0001, XRF_0042, MS-2025-001
❌ FTIR 1, analyse#1, test
```

**Object/Sample**:
```
✅ Ms59f01v, MNHN-Z314, Sample_A01
❌ manuscript page 1, échantillon A, test 01
```

**Conventions recommandées**:
- Pas d'espaces
- Tirets (-) pour séparer les parties
- Underscores (_) pour les sous-parties
- Majuscules pour les acronymes
- Numérotation avec zéros de tête (001, 002)

#### Structure de Projet

**Créer des templates par type d'analyse**:
```
templates/
  ├── FTIR_ATR_standard.json
  ├── XRF_portable_outdoor.json
  ├── GC-MS_organic.json
  └── Microscopy_optical.json
```

**Organiser les sauvegardes**:
```
experiments/
  ├── 2025/
  │   ├── 01_January/
  │   │   ├── project_alpha_ftir.elablite
  │   │   └── project_beta_xrf.elablite
  │   └── 02_February/
  └── 2024/
```

### Workflow Efficace

#### Préparation

1. **Créer un template réutilisable** pour vos analyses récurrentes
2. **Définir vos conventions de nommage** en équipe
3. **Préparer vos fichiers de données** avec des noms cohérents

#### Exécution

1. **Session de création**:
   - Créer l'expérience avec métadonnées (Steps 1-2)
   - Sauvegarder régulièrement
   - Compléter le tableau (Step 3)
   - Exporter (Step 4)

2. **Session de complétion** (séparée ou ultérieure):
   - Charger l'expérience sauvegardée
   - Uploader les fichiers de données
   - Vérifier le mapping
   - Générer le ZIP

#### Archivage

1. **Télécharger systématiquement**:
   - Le fichier `.elablite` pour l'archivage
   - Le ZIP généré pour elabFTW

2. **Organiser les archives**:
   ```
   archives/
     ├── elablite_files/
     │   └── 2025-10-14_project_alpha.elablite
     └── exports/
         └── 20251014_experiences.zip
   ```

3. **Backups réguliers** sur un stockage sécurisé

### Collaboration

#### Partage de Templates

1. Créer un repository d'équipe:
   ```
   lab_templates/
     ├── README.md
     ├── FTIR/
     ├── XRF/
     └── Microscopy/
   ```

2. Versionner les templates (Git recommandé)

3. Documenter chaque template:
   ```markdown
   # FTIR ATR Template
   
   ## Usage
   For all ATR-FTIR analyses on solid samples
   
   ## Required fields
   - Instrument
   - Resolution
   - Scans
   
   ## Optional fields
   - ATR crystal
   - Pressure
   ```

#### Conventions d'Équipe

Document partagé avec:
- Codes des techniques utilisées
- Format des identifiants
- Abréviations standard
- Workflow approuvé

### Optimisation

#### Performance

**Pour de gros tableaux (>100 lignes)**:
- Utilisez "Apply" régulièrement pour sauvegarder
- Évitez trop de modifications simultanées
- Travaillez par sections

**Pour de nombreux fichiers**:
- Groupez les uploads par lot
- Vérifiez le mapping par sections
- Utilisez des noms de fichiers descriptifs

#### Réutilisabilité

**Créer des variantes de templates**:
```
FTIR_ATR_standard.json
FTIR_ATR_liquids.json
FTIR_ATR_films.json
```

**Sauvegardes "Clean"**:
- Créez une version "template" sans données spécifiques
- Utilisez "Save As" pour les variantes

### Qualité des Données

#### Validation

**Avant de passer au Step suivant**:
- ✅ Tous les champs requis remplis
- ✅ Unités correctes et cohérentes
- ✅ Identifiants uniques et formatés
- ✅ Commentaires/notes ajoutés si nécessaire

**Avant export final**:
- ✅ Mapping de fichiers vérifié
- ✅ Noms de fichiers validés
- ✅ Pas de duplicata dans le tableau
- ✅ Métadonnées cohérentes entre les lignes

#### Traçabilité

**Utiliser les champs disponibles**:
- **Commentary**: Notes sur le contexte
- **Tags**: Mots-clés pour retrouver
- **Rating**: Qualité de l'expérience
- **Project info**: Liens vers projets

**Logs automatiques**:
Le fichier `logs_process.csv` dans le ZIP contient:
- Toutes les métadonnées avant transformation
- Traçabilité des modifications
- À conserver pour audit

---

## Dépannage

### Problèmes de Démarrage

**L'application ne démarre pas**:
```bash
# Vérifier l'installation
pip list | grep streamlit

# Réinstaller si nécessaire
pip install -r requirements.txt --force-reinstall
```

**Port déjà utilisé**:
```bash
# Utiliser un autre port
streamlit run app.py --server.port 8502
```

### Problèmes de Chargement

**Template ne se charge pas**:
1. Vérifiez le format du fichier (JSON valide)
2. Testez avec un template simple
3. Regardez les erreurs dans la console

**Fichier ELABLITE corrompu**:
- Retentez le téléchargement
- Vérifiez que le fichier n'est pas vide
- Utilisez une sauvegarde antérieure

### Problèmes de Sauvegarde

**Sauvegarde échoue**:
1. Vérifiez l'espace disque disponible
2. Vérifiez les permissions du dossier `tmp/`
3. Essayez "Save As" avec un nouveau nom

**Fichier introuvable**:
- Vérifiez dans `tmp/templates/presets/`
- Utilisez "Download" pour une copie permanente

### Problèmes de Performance

**Application lente**:
1. Réduisez la taille du tableau
2. Fermez les autres onglets du navigateur
3. Redémarrez l'application

**Navigateur plante**:
- Réduisez le nombre de fichiers uploadés
- Utilisez un navigateur moderne (Chrome, Firefox)
- Augmentez la mémoire allouée si possible

---

## Ressources Additionnelles

### Documentation Technique

- **GitHub**: https://github.com/CRC-Centre-Recherche-Conservation/ElabLite
- **Streamlit Docs**: https://docs.streamlit.io/
- **elabFTW**: https://www.elabftw.net/

### Support

- **Bug Reports**: [Issue Tracker](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/discussions)

### Contribuer

Vous pouvez contribuer en:
- Signalant des bugs
- Proposant des améliorations
- Partageant vos templates
- Traduisant la documentation

---

**Version du guide**: 1.0 (2025-10-14)  
**Compatible avec**: ElabLite v0.1.5-alpha