from dataclasses import dataclass
import streamlit as st

@dataclass
class TechniqueOption:
    code: str
    french_name: str
    english_name: str

    @staticmethod
    def add_technique(code, french_name, english_name):
        new_technique = TechniqueOption(code, french_name, english_name)
        TECHNIQUES[code] = new_technique
        return new_technique

    @staticmethod
    @st.experimental_dialog("Add a technical analysis")
    def open_add_technique_modal():
        st.write("You can add a new technical code if it does not exist.")
        with st.form("add_technique_form"):
            code = st.text_input("Code")
            english_name = st.text_input("English Name")
            french_name = st.text_input("French Name")
            submitted = st.form_submit_button("Add Technique")
            if submitted:
                if code and english_name:
                    new_technique = TechniqueOption.add_technique(code, french_name, english_name)
                    st.session_state["add_technique"] = new_technique
                    st.rerun()
                else:
                    st.error("Please fill in all fields")


TECHNIQUES = {
    "3D": TechniqueOption("3D", "Imagerie 3D", "3D Imaging"),
    "3D-LG": TechniqueOption("3D-LG", "Imagerie 3D – Lasergrammétrie", "3D Imaging – Laser Scanning"),
    "3D-LS": TechniqueOption("3D-LS", "Imagerie 3D – Lumière structurée", "3D Imaging – Structured Light"),
    "3D-PG": TechniqueOption("3D-PG", "Imagerie 3D – Photogrammétrie", "3D Imaging – Photogrammetry"),
    "3D-VG": TechniqueOption("3D-VG", "Imagerie 3D – Vidéogrammétrie", "3D Imaging – Videogrammetry"),
    "BINO": TechniqueOption("BINO", "Imagerie par loupe binoculaire", "Binocular Magnifier Imaging"),
    "CE": TechniqueOption("CE", "Electrophorèse capillaire", "Capillary Electrophoresis"),
    "CE-MS": TechniqueOption("CE-MS", "Electrophorèse capillaire couplée à la spectrométrie de masse", "Capillary Electrophoresis coupled with Mass Spectrometry"),
    "COLOR": TechniqueOption("COLOR", "Colorimétrie | spectro-colorimétrie", "Colorimetry | spectrocolorimetry"),
    "CR": TechniqueOption("CR", "Compte-rendu", "Report"),
    "DSC": TechniqueOption("DSC", "Calorimétrie différentielle à balayage", "Differential Scanning Calorimetry"),
    "DVS": TechniqueOption("DVS", "Sorption dynamique de vapeur", "Dynamic Vapor Sorption"),
    "FORS": TechniqueOption("FORS", "Fiber optical reflectance spectroscopy", "Fiber Optical Reflectance Spectroscopy"),
    "GC-MS": TechniqueOption("GC-MS", "Chromatographie en phase gazeuse couplée à la spectrométrie de masse", "Gas Chromatography-Mass Spectrometry"),
    "GC-2D-MS": TechniqueOption("GC-2D-MS", "Chromatographie en phase gazeuse à 2 dimensions couplée à la spectrométrie de masse", "Two-Dimensional Gas Chromatography-Mass Spectrometry"),
    "IR": TechniqueOption("IR", "Photographie infrarouge", "Infrared Photography"),
    "IRFC": TechniqueOption("IRFC", "Image fausse couleur avec photographie infrarouge", "False Color Image with Infrared Photography"),
    "IRTF": TechniqueOption("IRTF", "Spectroscopie infrarouge à transformée de Fourier", "Fourier Transform Infrared Spectroscopy"),
    "IRTF-ATR": TechniqueOption("IRTF-ATR", "Spectroscopie infrarouge à transformée de Fourier - mode réflectance", "Fourier Transform Infrared Spectroscopy – reflectance"),
    "LC-MS": TechniqueOption("LC-MS", "Chromatographie en phase liquide couplée à la spectrométrie de masse", "Liquid Chromatography-Mass Spectrometry"),
    "MALDI-MS": TechniqueOption("MALDI-MS", "Spectromètre de masse couplée à une source d'ionisation laser assistée par une matrice", "Matrix-Assisted Laser Desorption/Ionization Mass Spectrometry"),
    "MEB": TechniqueOption("MEB", "Microscopie électronique à balayage", "Scanning Electron Microscopy"),
    "MECA": TechniqueOption("MECA", "Essais mécaniques", "Mechanical Testing"),
    "MFT": TechniqueOption("MFT", "Microfading tester", "Microfading Tester"),
    "MO": TechniqueOption("MO", "Microscopie optique", "Optical Microscopy"),
    "MPM": TechniqueOption("MPM", "Multiphoton microscopy", "Multiphoton Microscopy"),
    "pH": TechniqueOption("pH", "Tests de pH", "pH Testing"),
    "PTR-MS": TechniqueOption("PTR-MS", "Spectrométrie de masse par transfert de charge protonique", "Proton-Transfer-Reaction Mass Spectrometry"),
    "RAMAN": TechniqueOption("RAMAN", "Spectroscopie Raman", "Raman Spectroscopy"),
    "REFL": TechniqueOption("REFL", "Spectrophotométrie de réflectance", "Reflectance Spectrophotometry"),
    "RIR": TechniqueOption("RIR", "Réflectographie infrarouge", "Infrared Reflectography"),
    "RIS": TechniqueOption("RIS", "Imagerie de réflectance hyperspectrale", "Hyperspectral Reflectance Imaging"),
    "RIS-SWIR": TechniqueOption("RIS-SWIR", "Imagerie de réflectance hyperspectrale – domaine infrarouge", "Hyperspectral Reflectance Imaging – Short-Wave Infrared domain"),
    "RIS-VNIR": TechniqueOption("RIS-VNIR", "Imagerie de réflectance hyperspectrale – domaine visible", "Hyperspectral Reflectance Imaging –Visible and Near-Infrared domain"),
    "RTI": TechniqueOption("RTI", "Reflectance Transformation Imaging", "Reflectance Transformation Imaging"),
    "RX": TechniqueOption("RX", "Radiographies X", "X-ray Radiography"),
    "SEC": TechniqueOption("SEC", "Chromatographie d'exclusion stérique", "Size-Exclusion Chromatography"),
    "TOMO": TechniqueOption("TOMO", "Tomographie X", "X-ray Tomography"),
    "TRANS": TechniqueOption("TRANS", "Spectrophotométrie de transmittance", "Transmittance Spectrophotometry"),
    "UVF": TechniqueOption("UVF", "Photographie de fluorescence UV", "UV Fluorescence Photography"),
    "UVFC": TechniqueOption("UVFC", "Image fausse couleur avec photographie UVR", "False Color Image with UV Reflectance Photography"),
    "UVR": TechniqueOption("UVR", "Photographie de réflectance UV", "UV Reflectance Photography"),
    "VIS": TechniqueOption("VIS", "Photographie RGB", "RGB Photography"),
    "VIS-LD": TechniqueOption("VIS-LD", "Photographie RGB – Lumière directe", "RGB Photography – Direct Light"),
    "VIS-LR": TechniqueOption("VIS-LR", "Photographie RGB – Lumière rasante", "RGB Photography – Raking Light"),
    "VIS-LT": TechniqueOption("VIS-LT", "Photographie RGB – Lumière transmise", "RGB Photography – Transmitted Light"),
    "VIS-MP": TechniqueOption("VIS-MP", "Photographie RGB – Macrophotographie", "RGB Photography – Macrophotography"),
    "VIS-OL": TechniqueOption("VIS-OL", "Photographie RGB – Open light", "RGB Photography – Open Light"),
    "XRD": TechniqueOption("XRD", "Diffraction des rayons X", "X-ray Diffraction"),
    "XRF": TechniqueOption("XRF", "Spectroscopie de fluorescence des rayons X", "X-ray Fluorescence Spectroscopy"),
}