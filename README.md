# Clinical Pharmacist Performance Assessment Tool

A standardized, mobile-friendly web application for assessing the clinical performance of acute care hospital pharmacists. Grounded in nationally recognized standards from ASHP, ACCP, and the JCPP Pharmacists' Patient Care Process (PPCP).

---

## Standards Alignment

| Standard / Framework | Source |
|---|---|
| ASHP Accreditation Standard for Residency Programs (2024) — R1, R2, R3, R4 | [ASHP](https://www.ashp.org/professional-development/residency-information) |
| ACCP Clinical Pharmacist Competencies (2019) — all 6 domains | [JACCP](https://pubmed.ncbi.nlm.nih.gov/28464300/) |
| JCPP Pharmacists' Patient Care Process (PPCP) | [JCPP](https://jcpp.net/patient-care-process/) |
| ASHP Practice Advancement Initiative (PAI) 2030 | [ASHP PAI](https://www.ashp.org/pharmacy-practice/pai) |

### Assessment Domains

| Domain | ASHP Standard | ACCP Competency |
|---|---|---|
| 1. Pharmacists' Patient Care Process (PPCP) | R1 (Patient Care) | Direct Patient Care |
| 2. Drug Therapy Management & Clinical Knowledge | R1 (Patient Care) | Pharmacotherapy Knowledge |
| 3. Communication, Documentation & Collaboration | R1 (Patient Care) | Communication |
| 4. Systems-Based Practice, Quality & Safety | R2 (Advancing Practice) | Systems-Based Care |
| 5. Professional Development, Leadership & Education | R3 (Leadership) + R4 (Education) | Professionalism + CPD |

### EPA Rating Scale

| Level | Label | Description |
|---|---|---|
| 1 | Needs Significant Development | Significant supervision required |
| 2 | Developing (Below Expectations) | Direct supervision required |
| 3 | Progressing (Approaching Expectations) | Indirect supervision |
| 4 | Meets Expectations (Practice-Ready) | Independent practice — expected standard |
| 5 | Exemplary (Exceeds Expectations) | Role model / peer resource |

---

## Features

- 23 assessment items across 5 ASHP/ACCP-aligned domains
- EPA 1-5 rating scale with behavioral anchors for each item
- Mobile-friendly interface optimized for phones and tablets for on-unit use
- Downloadable PDF report in professional, accreditation-ready format
- CSV export compatible with Smartsheet, Excel, and other tools
- Assessor attestation built-in objectivity safeguard
- About page with complete standards references and methodology
- Confidentiality framing marked as peer review protected

---

## Setup & Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/kdumas31/clinical-pharmacist-assessment.git
cd clinical-pharmacist-assessment

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at http://localhost:8501 in your browser.

---

## Deployment to Streamlit Cloud (Free)

1. Go to https://share.streamlit.io
2. Click New app and connect your GitHub repo
3. Set Main file path: app.py
4. Click Deploy

---

## References

1. ASHP. Accreditation Standard for PGY1 Pharmacy Residency Programs. 2024.
2. ASHP. PGY1 Harmonized Competency Areas, Goals, and Objectives. BOD Approved 2024.
3. Engle JP, et al. ACCP Clinical Pharmacist Competencies. JACCP. 2019;2(6):550-556.
4. JCPP. Pharmacists' Patient Care Process. 2014.
5. ASHP. Practice Advancement Initiative 2030.
