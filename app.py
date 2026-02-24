"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         CLINICAL PHARMACIST PERFORMANCE ASSESSMENT TOOL                     ║
║  Grounded in ASHP Accreditation Standards, ACCP Competency Framework,       ║
║  and the JCPP Pharmacists' Patient Care Process (PPCP)                       ║
║  Version 1.0  |  For use by Clinical Pharmacy Managers & Peer Pharmacists   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from io import BytesIO
import base64
import json
import math

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clinical Pharmacist Assessment",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={"About": "Clinical Pharmacist Performance Assessment Tool v1.0"}
)

# ─── MOBILE-FRIENDLY CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Layout ── */
  .main .block-container { max-width: 900px; padding: 1rem 1.5rem 3rem; }
  @media (max-width: 768px) {
    .main .block-container { padding: 0.5rem 0.75rem 2rem; }
  }

  /* ── App header ── */
  .app-header {
    background: linear-gradient(135deg, #0d2b4e 0%, #1a4a7a 100%);
    color: white; padding: 18px 22px; border-radius: 10px;
    margin-bottom: 20px;
  }
  .app-header h1 { margin: 0; font-size: 1.5rem; color: white; }
  .app-header p  { margin: 4px 0 0; font-size: 0.85rem; opacity: 0.85; }

  /* ── Domain header ── */
  .domain-header {
    background: linear-gradient(135deg, #1a4a7a 0%, #2563a8 100%);
    color: white; padding: 12px 18px; border-radius: 8px;
    margin: 24px 0 12px; font-size: 1rem; font-weight: 700;
  }
  .domain-desc {
    background: #f0f7ff; border-left: 4px solid #2563a8;
    padding: 10px 14px; border-radius: 0 6px 6px 0;
    font-size: 0.83rem; color: #444; margin-bottom: 14px;
  }

  /* ── Item card ── */
  .item-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-left: 4px solid #2563a8; padding: 12px 16px;
    border-radius: 0 8px 8px 0; margin: 10px 0 4px;
    font-size: 0.93rem; line-height: 1.5; color: #1e293b;
  }

  /* ── EPA legend ── */
  .epa-box {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 8px; padding: 12px 16px; margin: 10px 0;
    font-size: 0.82rem; color: #1e3a5f;
  }
  .epa-row { display: flex; align-items: center; margin: 4px 0; gap: 8px; }
  .epa-dot {
    width: 12px; height: 12px; border-radius: 50%;
    flex-shrink: 0; display: inline-block;
  }

  /* ── Scores & badges ── */
  .score-card {
    border-radius: 10px; padding: 14px 18px; margin: 8px 0;
    border: 1px solid rgba(0,0,0,0.08);
  }
  .score-card-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; }
  .score-card-value { font-size: 1.8rem; font-weight: 800; line-height: 1; }
  .score-card-label { font-size: 0.78rem; opacity: 0.85; margin-top: 4px; }

  .overall-box {
    background: linear-gradient(135deg, #0d2b4e, #1a4a7a);
    color: white; border-radius: 12px; padding: 20px;
    text-align: center; margin: 16px 0;
  }
  .overall-box .big-score { font-size: 3rem; font-weight: 900; line-height: 1; }
  .overall-box .cat       { font-size: 1.05rem; font-weight: 600; margin-top: 6px; }
  .overall-box .sub       { font-size: 0.82rem; opacity: 0.8; margin-top: 4px; }

  /* ── Section title ── */
  .section-title {
    font-size: 1.2rem; font-weight: 700; color: #0d2b4e;
    border-bottom: 2px solid #2563a8; padding-bottom: 6px;
    margin: 28px 0 14px;
  }

  /* ── Anchor hints ── */
  .anchor-hint {
    font-size: 0.75rem; color: #64748b;
    display: flex; gap: 16px; margin-top: 2px;
  }
  .anchor-hint span { flex: 1; }

  /* ── Buttons ── */
  .stButton > button {
    width: 100%; padding: 12px; font-size: 1rem;
    border-radius: 8px; font-weight: 600;
  }

  /* ── Radio bigger touch targets ── */
  .stRadio [data-baseweb="radio"] { margin-bottom: 6px; padding: 2px 0; }
  .stRadio label { font-size: 0.92rem !important; }

  /* ── Attribution footer ── */
  .attr { font-size: 0.72rem; color: #94a3b8; text-align: center; margin-top: 30px; }

  /* ── Info callout ── */
  .callout {
    background: #fefce8; border: 1px solid #fde047;
    border-radius: 8px; padding: 10px 14px; font-size: 0.85rem;
    color: #713f12; margin: 10px 0;
  }
  .callout-blue {
    background: #eff6ff; border: 1px solid #93c5fd;
    border-radius: 8px; padding: 10px 14px; font-size: 0.85rem;
    color: #1e3a5f; margin: 10px 0;
  }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# ASSESSMENT FRAMEWORK
# Based on: ASHP Accreditation Standard (2024), ACCP Clinical Pharmacist
# Competencies, JCPP Pharmacists' Patient Care Process (PPCP), and
# ASHP PGY1 Required Competency Areas (R1–R4).
# ═════════════════════════════════════════════════════════════════════════════

DOMAINS = [
    {
        "id": "ppcp",
        "title": "Domain 1 — Pharmacists' Patient Care Process (PPCP)",
        "short": "Patient Care Process",
        "description": (
            "The JCPP Pharmacists' Patient Care Process is the standard patient care framework endorsed by ASHP, ACCP, "
            "APhA, ASHP, and all major pharmacy organizations. Mastery of the PPCP aligns with ASHP Accreditation "
            "Standard R1 (Patient Care) and ACCP's Direct Patient Care competency domain."
        ),
        "color": "#1a4a7a",
        "items": [
            {
                "id": "ppcp_1",
                "text": "COLLECT: Systematically obtains accurate and complete medication histories, relevant labs/vitals/clinical notes, and patient-specific data needed for assessment",
                "low": "Misses critical data; requires guidance to complete medication reconciliation",
                "high": "Comprehensively synthesizes all relevant data; proactively identifies discrepancies",
            },
            {
                "id": "ppcp_2",
                "text": "ASSESS: Accurately identifies, prioritizes, and communicates drug therapy problems and patient care needs using clinical reasoning",
                "low": "Misses significant drug therapy problems; limited clinical reasoning",
                "high": "Identifies complex, nuanced DTPs; integrates multiple data sources into sound clinical judgments",
            },
            {
                "id": "ppcp_3",
                "text": "PLAN: Develops individualized, evidence-based, patient-centered pharmacotherapy plans aligned with current clinical guidelines",
                "low": "Plans lack evidence basis or are not patient-specific; guideline non-concordant",
                "high": "Develops comprehensive individualized plans; applies guidelines contextually; considers full range of options",
            },
            {
                "id": "ppcp_4",
                "text": "IMPLEMENT: Effectively communicates and implements the care plan with the healthcare team, patient, and caregivers in a timely manner",
                "low": "Difficulty implementing plans; communication gaps with team or patients",
                "high": "Seamlessly implements plans; proactive and clear communication; ensures team and patient buy-in",
            },
            {
                "id": "ppcp_5",
                "text": "FOLLOW-UP/MONITOR: Establishes appropriate monitoring parameters for efficacy and safety, follows up consistently, and adjusts plans based on clinical response",
                "low": "Monitoring incomplete or inconsistent; does not reliably follow up on clinical concerns",
                "high": "Establishes comprehensive individualized monitoring; consistently follows through; optimizes therapy based on outcomes",
            },
        ],
    },
    {
        "id": "dtm",
        "title": "Domain 2 — Drug Therapy Management & Clinical Knowledge",
        "short": "Drug Therapy & Knowledge",
        "description": (
            "Reflects ACCP's Pharmacotherapy Knowledge competency domain and ASHP practice standards for "
            "acute care clinical pharmacists. Includes clinical pharmacology, PK/PD, antimicrobial stewardship, "
            "and evidence-based medicine as required under ASHP R1 objectives."
        ),
        "color": "#155e75",
        "items": [
            {
                "id": "dtm_1",
                "text": "Demonstrates current, accurate pharmacotherapy knowledge for common and complex conditions encountered on the unit (disease states, mechanisms, therapeutics)",
                "low": "Knowledge gaps significantly impact recommendation quality",
                "high": "Expert-level knowledge; serves as unit resource for complex and unusual clinical questions",
            },
            {
                "id": "dtm_2",
                "text": "Applies pharmacokinetic/pharmacodynamic principles to individualize drug dosing (renal/hepatic adjustment, TDM, special populations: obesity, ECMO, CRRT, etc.)",
                "low": "PK/PD applications inaccurate or missed; requires guidance for adjustments",
                "high": "Expert PK/PD application across all patient populations including complex cases",
            },
            {
                "id": "dtm_3",
                "text": "Proactively identifies and manages drug-drug interactions, adverse drug events, and medication safety concerns; prevents harm",
                "low": "Misses significant interactions or ADEs; reactive rather than proactive",
                "high": "Proactively identifies complex interactions and safety issues; implements effective mitigation strategies",
            },
            {
                "id": "dtm_4",
                "text": "Applies antimicrobial stewardship principles (de-escalation, IV-to-PO conversion, indication review, appropriate duration, culture-guided therapy)",
                "low": "Limited stewardship engagement; rarely initiates stewardship interventions",
                "high": "Champions stewardship on the unit; consistently applies all principles; proactively educates team",
            },
            {
                "id": "dtm_5",
                "text": "Retrieves, critically evaluates, and appropriately applies drug information and clinical evidence to patient care decisions (EBM skills)",
                "low": "Drug information skills limited; applies evidence uncritically or inaccurately",
                "high": "Expert evidence appraisal; synthesizes conflicting literature to guide individualized clinical decisions",
            },
        ],
    },
    {
        "id": "comm",
        "title": "Domain 3 — Communication, Documentation & Interprofessional Collaboration",
        "short": "Communication & Collaboration",
        "description": (
            "Aligns with ACCP's Communication competency domain and ASHP Accreditation Standard R1 objectives "
            "for interprofessional collaboration, patient counseling, and clinical documentation. "
            "Reflects Joint Commission patient education and documentation standards."
        ),
        "color": "#065f46",
        "items": [
            {
                "id": "comm_1",
                "text": "Provides clear, concise, clinically relevant verbal recommendations to physicians, APPs, nurses, and other healthcare team members",
                "low": "Recommendations unclear or difficult to act upon; communication barriers with team",
                "high": "Consistently delivers actionable, respected recommendations; adapts style to audience effectively",
            },
            {
                "id": "comm_2",
                "text": "Documents clinical interventions, SOAP notes, and recommendations accurately, completely, and in a timely manner per institutional standards",
                "low": "Documentation incomplete, inaccurate, or untimely; misses significant interventions",
                "high": "Documentation thorough, precise, and timely; writing is clinically useful to the entire care team",
            },
            {
                "id": "comm_3",
                "text": "Provides effective, tailored patient and caregiver education (medication counseling, discharge education, adherence counseling, health literacy assessment)",
                "low": "Patient education missed, unclear, or not tailored to health literacy level",
                "high": "Excellent patient educator; assesses comprehension; addresses barriers to adherence proactively",
            },
            {
                "id": "comm_4",
                "text": "Actively contributes meaningful pharmacotherapy input during interprofessional rounds and functions as a valued, integrated team member",
                "low": "Limited rounds participation; pharmacy perspective underrepresented; passive team role",
                "high": "Key rounds contributor; proactively raises pharmacotherapy concerns; widely valued by team",
            },
            {
                "id": "comm_5",
                "text": "Maintains professional, respectful communication with patients, families, and team members including in challenging, high-stress, or conflict situations",
                "low": "Communication in difficult situations needs improvement; may create or escalate conflict",
                "high": "Exceptional professional communication in all situations; models respectful de-escalation",
            },
        ],
    },
    {
        "id": "sys",
        "title": "Domain 4 — Systems-Based Practice, Quality & Patient Safety",
        "short": "Systems, Quality & Safety",
        "description": (
            "Aligns with ASHP Accreditation Standard R2 (Advancing Practice and Improving Patient Care), "
            "ACCP's Systems-Based Care and Population Health domain, and Joint Commission National "
            "Patient Safety Goals. Includes QI participation, medication safety, and policy compliance."
        ),
        "color": "#7c2d12",
        "items": [
            {
                "id": "sys_1",
                "text": "Identifies, reports, and acts on medication errors, near-misses, and adverse drug events; actively promotes a culture of medication safety",
                "low": "Rarely identifies or seports safety events; limited engagement with safety culture",
                "high": "Proactively identifies safety concerns; consistently reports events; drives safety culture improvements",
            },
            {
                "id": "sys_2",
                "text": "Participates in quality improvement projects, P&T/formulary activities, medication use evaluations, or other practice improvement initiatives",
                "low": "Minimal QI involvement; not engaged in practice improvement activities",
                "high": "Active QI leader/participant; initiates improvements; meaningfully contributes to P&T and formulary decisions",
            },
            {
                "id": "sys_3",
                "text": "Demonstrates current knowledge of institutional drug use policies, formulary restrictions, prior authorization processes, and regulatory requirements",
                "low": "Limited policy awareness; frequently requires guidance on formulary and regulatory matters",
                "high": "Expert in institutional policies; proactively applies, interprets, and educates others; identifies gaps",
            },
            {
                "id": "sys_4",
                "text": "Effectively manages time, workload, and clinical responsibilities; appropriately prioritizes patient care tasks including high-acuity situations",
                "low": "Struggles with prioritization; workload management issues affect care quality; tasks incomplete",
                "high": "Excellent time management; efficiently handles high-acuity workload; consistently meets all responsibilities",
            },
        ],
    },
    {
        "id": "prof",
        "title": "Domain 5 — Professional Development, Leadership & Education",
        "short": "Leadership & Development",
        "description": (
            "Aligns with ASHP Accreditation Standards R3 (Leadership and Management) and R4 (Teaching, "
            "Education, and Dissemination of Knowledge), and ACCP's Professionalism and Continuing "
            "Professional Development domains. Reflects ASHP PAI 2030 practice advancement standards."
        ),
        "color": "#4a1d96",
        "items": [
            {
                "id": "prof_1",
                "text": "Demonstrates professional accountability, ethical practice, and consistent adherence to standards of pharmacy practice and institutional policies",
                "low": "Professional accountability concerns; inconsistent adherence to practice standards",
                "high": "Exemplary professional standards; highly accountable; advocates for patients and the profession",
            },
            {
                "id": "prof_2",
                "text": "Engages in self-directed, continuous professional development; proactively identifies and addresses own knowledge and skill gaps",
                "low": "Limited self-directed learning; does not proactively address knowledge gaps",
                "high": "Highly motivated self-learner; continuously improves; proactively seeks and addresses gaps",
            },
            {
                "id": "prof_3",
                "text": "Preceptors, mentors, or educates pharmacy students, residents, and/or interprofessional learners (if applicable to role)",
                "low": "Limited teaching engagement; not effectively contributing to learner development",
                "high": "Outstanding preceptor/educator; positively impacts learner development; sought as teaching resource",
                "optional": True,
            },
            {
                "id": "prof_4",
                "text": "Demonstrates leadership: takes initiative, adapts to change, advocates for patients and the profession, and fosters collaborative improvement",
                "low": "Limited leadership initiative; primarily reactive; does not advocate for improvements",
                "high": "Strong leader; consistently demonstrates initiative; champions patient care and practice advancement",
            },
        ],
    },
]

# ─── EPA SCALE ────────────────────────────────────────────────────────────────
# Adapted from ASHP Residency Entrustable Professional Activities (EPA) framework
# and ACGME/ASHP competency milestone progression for practicing pharmacists.

EPA_SCALE = {
    1: {
        "label": "1 — Needs Significant Development",
        "short": "Needs Significant Development",
        "desc": "Does not yet demonstrate expected competency. Requires significant supervision, direction, and guidance. Patient safety may be a concern without close oversight.",
        "color": "#dc2626",
        "bg": "#fef2f2",
    },
    2: {
        "label": "2 — Developing (Below Expectations)",
        "short": "Developing",
        "desc": "Demonstrates basic/emerging competency. Requires direct supervision and frequent guidance. Performance is below expectations for a practice-ready pharmacist.",
        "color": "#ea580c",
        "bg": "#fff7ed",
    },
    3: {
        "label": "3 — Progressing (Approaching Expectations)",
        "short": "Progressing",
        "desc": "Demonstrates developing-to-expected competency. Able to perform with indirect supervision available. Approaches expectations; minor gaps remain.",
        "color": "#ca8a04",
        "bg": "#fefce8",
    },
    4: {
        "label": "4 — Meets Expectations (Practice-Ready)",
        "short": "Meets Expectations",
        "desc": "Demonstrates expected competency for a practice-ready acute care clinical pharmacist. Practices independently and consistently. Meets all performance standards.",
        "color": "#16a34a",
        "bg": "#f0fdf4",
    },
    5: {
        "label": "5 — Exemplary (Exceeds Expectations)",
        "short": "Exemplary",
        "desc": "Demonstrates exemplary competency well above expectations. Serves as a role model, peer resource, and mentor. Advances practice on the unit.",
        "color": "#2563eb",
        "bg": "#eff6ff",
    },
}

RATING_OPTIONS = {
    "N/A — Not observed / Not applicable to role": 0,
    "1 — Needs Significant Development": 1,
    "2 — Developing (Below Expectations)": 2,
    "3 — Progressing (Approaching Expectations)": 3,
    "4 — Meets Expectations (Practice-Ready)": 4,
    "5 — Exemplary (Exceeds Expectations)": 5,
}

UNIT_OPTIONS = [
    "Medical/Surgical ICU (MICU/SICU)",
    "Cardiac ICU (CICU/CVICU)",
    "Neurological/Neurosurgical ICU",
    "Pediatric ICU (PICU)",
    "Neonatal ICU (NICU)",
    "Surgical/Trauma ICU",
    "General Internal Medicine",
    "Cardiology / Cardiac Step-Down",
    "Hematology / Oncology",
    "Bone Marrow Transplant",
    "Solid Organ Transplant",
    "Infectious Disease",
    "Pulmonology / Respiratory",
    "Nephrology",
    "Neurology / Stroke",
    "General Surgery",
    "Orthopedics / Trauma",
    "Emergency Medicine",
    "Other (specify in comments)",
]

ASSESSMENT_TYPES = [
    "Routine Peer Performance Review",
    "Annual Performance Evaluation",
    "ASHP Residency Preceptor Assessment",
    "Competency Validation / Credentialing",
    "Post-Probationary Review",
    "Focused Performance Improvement Review",
    "Learner Observation (Student/Resident Preceptor Quality)",
    "Other",
]

FOLLOW_UP_OPTIONS = [
    "No follow-up required — performance meets or exceeds expectations",
    "3 months — minor development areas identified",
    "6 months — moderate development areas, targeted plan in place",
    "12 months — routine annual review cycle",
     "30–60 days — significant concerns, close follow-up needed",
    "Refer to formal performance improvement process",
]

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

def score_color(score):
    if score is None: return "#94a3b8"
    if score < 1.75: return "#dc2626"
    if score < 2.75: return "#ea580c"
    if score < 3.5:  return "#ca8a04"
    if score < 4.5:  return "#16a34a"
    return "#2563eb"

def score_bg(score):
    if score is None: return "#f8fafc"
    if score < 1.75: return "#fef2f2"
    if score < 2.75: return "#fff7ed"
    if score < 3.5:  return "#fefce8"
    if score < 4.5:  return "#f0fdf4"
    return "#eff6ff"

def perf_category(score):
    if score is None: return "Insufficient Data"
    if score < 1.75: return "Needs Significant Development"
    if score < 2.75: return "Developing — Below Expectations"
    if score < 3.5:  return "Progressing - Approaching Expectations"
    if score < 4.5:  return "Meets Expectations — Practice-Ready"
    return "Exemplary — Exceeds Expectations"

def calc_domain_avg(ratings_dict):
    vals = [v for v in ratings_dict.values() if v and v > 0]
    return round(sum(vals) / len(vals), 2) if vals else None

def calc_overall_avg(all_ratings):
    vals = [v for v in all_ratings.values() if v and v > 0]
    return round(sum(vals) / len(vals), 2) if vals else None

# ─── PDF GENERATION ──────────────────────────────────────────────────────────

def generate_pdf_report(info, ratings, narratives):
    """
    Generate a professional PDF assessment report using reportlab.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, KeepTogether,
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    except ImportError:
        return None

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    # Custom styles
    title_style = ParagraphStyle(
        "Title2",
        parent=styles["Title"],
        fontSize=15,
        textColor=colors.HexColor("#0d2b4e"),
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    sub_style = ParagraphStyle(
        "Sub",
        parent=styles["Normal"],
        fontSize=8.5,
        textColor=colors.HexColor("#475569"),
        spaceAfter=2,
        alignment=TAD_CENTER,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=11,
        textColor=colors.HexColor("#0d2b4e"),
        spaceBefore=14,
        spaceAfter=4,
        borderPad=2,
    )
    h3 = ParagraphStyle(
        "H3",
        parent=styles["Heading3"],
        fontSize=9.5,
        textColor=colors.HexColor("#1a4a7a"),
        spaceBefore=8,
        spaceAfter=3,
    )
    body = ParagraphStyle(
        "Body2",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4,
        leading=13,
    )
    small = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=7.5,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=2,
        leading=11,
    )
    label_bold = ParagraphStyle(
        "LabelBold",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#0d2b4e"),
        fontName="Helvetica-Bold",
    )
    narrative_style = ParagraphStyle(
        "Narrative",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#1e293b"),
        backColor=colors.HexColor("#f8fafc"),
        borderPad=6,
        leading=13,
        spaceAfter=6,
    )

    story = []

    # ── Header Banner ──────────────────────────────────────────────────────
    header_data = [[
        Paragraph(
            "<b>CLINICAL PHARMACIST PERFORMANCE ASSESSMENT</b><br/>"
            "<font size=8 color='#93c5fd'>Acute Care Hospital — Peer/Manager Review</font>",
            ParagraphStyle("HeaderBanner", fontName="Helvetica-Bold", fontSize=13,
                           textColor=colors.white, leading=18, alignment=TA_CENTER)
        )
    ]]
    header_tbl = Table(header_data, colWidths=[7 * inch])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0d2b4e")),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 16),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Grounded in ASHP Accreditation Standards (2024), ACCP Clinical Pharmacist Competencies, "
        "and the JCPP Pharmacists' Patient Care Process (PPCP)", sub_style
    ))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#bfdbfe")))
    story.append(Spacer(1, 10))

    # ── Assessment Info Table ─────────────────────────────────────────────
    story.append(Paragraph("ASSESSMENT INFORMATION", h2))

    def info_row(label, value):
        return [
            Paragraph(label, label_bold),
            Paragraph(str(value) if value else "—", body),
        ]

    info_data = [
        info_row("Pharmacist Being Assessed:", info.get("pharmacist_name", "")),
        info_row("Pharmacist Credentials:", info.get("pharmacist_credentials", "")),
        info_row("Clinical Unit / Service:", info.get("unit", "")),
        info_row("Assessor Name & Credentials:", info.get("assessor_name", "") + ((" " + info.get("assessor_credentials", "")) if info.get("assessor_credentials") else "")),
        info_row("Assessor Role:", info.get("assessor_role", "")),
        info_row("Assessment Type:", info.get("assessment_type", "")),
        info_row("Assessment Date:", str(info.get("assessment_date", ""))),
        info_row("Observation Period:", f"{info.get('obs_start', '')} to {info.get('obs_end', '')}"),
        info_row("Assessment Context / Notes:", info.get("context_notes", "")),
    ]
    info_tbl = Table(info_data, colWidths=[2.2 * inch, 4.8 * inch])
    info_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 12))

    # ── Overall Score ─────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#bfdbfe")))
    story.append(Spacer(1, 8))
    story.append(Paragraph("OVERALL PERFORMANCE SUMMARY", h2))

    all_vals = [v for v in ratings.values() if v and v > 0]
    overall = round(sum(all_vals) / len(all_vals), 2) if all_vals else None
    category = perf_category(overall)
    n_rated = len(all_vals)
    total_items = sum(len(d["items"]) for d in DOMAINS)

    oc = colors.HexColor(score_color(overall)) if overall else colors.HexColor("#94a3b8")

    overall_data = [[
        Paragraph(
            f"<b>{overall if overall else 'N/A'}</b><br/>"
            f"<font size=9>out of 5.0</font>",
            ParagraphStyle("OScore", fontName="Helvetica-Bold", fontSize=22,
                           textColor=oc, alignment=TA_CENTER, leading=26)
        ),
        Paragraph(
            f"<b>{category}</b><br/>"
            f"<font size=8 color='#475569'>{n_rated} of {total_items} items rated  •  "
            f"{len(all_vals)} scored observations</font>",
            ParagraphStyle("OCat", fontName="Helvetica-Bold", fontSize=11,
                           textColor=colors.HexColor("#0d2b4e"), leading=16)
        ),
    ]]
    otbl = Table(overall_data, colWidths=[1.5 * inch, 5.5 * inch])
    otbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0f7ff")),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("VALIGN",   (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [6]),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#bfdbfe")),
    ]))
    story.append(otbl)
    story.append(Spacer(1, 12))

    # ── Domain Score Summary Table ────────────────────────────────────────
    story.append(Paragraph("DOMAIN SCORES SUMMARY", h2))

    domain_hdr = [
        Paragraph("<b>Domain</b>", label_bold),
        Paragraph("<b>Avg Score</b>", label_bold),
        Paragraph("<b>Performance Category</b>", label_bold),
        Paragraph("<b>Items Rated</b>", label_bold),
    ]
    domain_rows = [domain_hdr]
    for dom in DOMAINS:
        item_ids = [it["id"] for it in dom["items"]]
        dom_ratings = {k: ratings.get(k) for k in item_ids}
        avg = calc_domain_avg(dom_ratings)
        n = len([v for v in dom_ratings.values() if v and v > 0])
        sc = colors.HexColor(score_color(avg)) if avg else colors.HexColor("#94a3b8")
        domain_rows.append([
            Paragraph(dom["short"], body),
            Paragraph(f"<b><font color='{score_color(avg)}'>{avg if avg else '—'}</font></b>",
                      ParagraphStyle("DS", fontSize=10, fontName="Helvetica-Bold")),
            Paragraph(perf_category(avg), small),
            Paragraph(f"{n} / {len(dom['items'])}", body),
        ])
    dtbl = Table(domain_rows, colWidths=[2.5 * inch, 1.0 * inch, 2.7 * inch, 0.8 * inch])
    dtbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), colors.HexColor("#0d2b4e")),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(dtbl)
    story.append(Spacer(1, 14))

    # ── Detailed Ratings by Domain ────────────────────────────────────────
    story.append(Paragraph("DETAILED ASSESSMENT RATINGS", h2))
    story.append(Paragraph(
        "Rating Scale: 1 = Needs Significant Development  |  2 = Developing  |  "
        "3 = Progressing  |  4 = Meets Expectations  |  5 = Exemplary  |  N/A = Not Observed",
        small
    ))
    story.append(Spacer(1, 6))

    for dom in DOMAINS:
        dom_block = []
        dom_block.append(Paragraph(dom["title"], h3))

        detail_hdr = [
            Paragraph("<b>Assessment Item</b>", ParagraphStyle("DH", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white)),
            Paragraph("<b>Rating</b>", ParagraphStyle("DH2", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white, alignment=TA_CENTER)),
            Paragraph("<b>Performance Category</b>", ParagraphStyle("DH3", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white)),
        ]
        det_rows = [detail_hdr]
        for item in dom["items"]:
            rating = ratings.get(item["id"])
            optional_tag = " <font color='#94a3b8'>[Optional]</font>" if item.get("optional") else ""
            if rating and rating > 0:
                r_label = EPA_SCALE[rating]["short"]
                r_color = score_color(rating)
            else:
                r_label = "N/A"
                r_color = "#94a3b8"
            det_rows.append([
                Paragraph(item["text"] + optional_tag,
                          ParagraphStyle("It", fontSize=8, leading=11, textColor=colors.HexColor("#1e293b"))),
                Paragraph(
                    f"<b><font color='{r_color}'>{rating if (rating and rating > 0) else 'N/A'}</font></b>",
                    ParagraphStyle("Rt", fontSize=10, fontName="Helvetica-Bold", alignment=TA_CENTER)
                ),
                Paragraph(r_label if rating else "Not Observed",
                          ParagraphStyle("Cat", fontSize=8, textColor=colors.HexColor(r_color))),
            ])

        det_tbl = Table(det_rows, colWidths=[3.9 * inch, 0.7 * inch, 2.4 * inch])
        det_tbl.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (-1, 0), colors.HexColor("#1a4a7a")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 7),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        dom_block.append(det_tbl)
        dom_block.append(Spacer(1, 8))
        story.append(KeepTogether(dom_block))

    # ── Narrative Sections ────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#bfdbfe")))
    story.append(Spacer(1, 8))
    story.append(Paragraph("NARRATIVE ASSESSMENT", h2))

    def narrative_block(title, content):
        blk = []
        blk.append(Paragraph(title, h3))
        if content and content.strip():
            blk.append(Paragraph(content.replace("\n", "<br/>"), narrative_style))
        else:
            blk.append(Paragraph("<i>No comments provided.</i>",
                                  ParagraphStyle("NC", fontSize=8.5, textColor=colors.HexColor("#94a3b8"), fontName="Helvetica-Oblique")))
        blk.append(Spacer(1, 6))
        return blk

    story += narrative_block("Clinical Strengths", narratives.get("strengths", ""))
    story += narrative_block("Areas for Development", narratives.get("development", ""))
    story += narrative_block("Action Plan / Goals", narratives.get("goals", ""))
    story += narrative_block("Overall Performance Summary", narratives.get("summary", ""))

    story.append(Paragraph(
        f"<b>Recommended Follow-Up:</b> {narratives.get('followup', '—')}",
        ParagraphStyle("FU", fontSize=9, textColor=colors.HexColor("#1e293b"),
                       backColor=colors.HexColor("#fefce8"), borderPad=6)
    ))
    story.append(Spacer(1, 16))

    # ── Attestation ──────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#bfdbfe")))
    story.append(Spacer(1, 8))
    story.append(Paragraph("ASSESSOR ATTESTATION", h2))

    attest_text = (
        "I attest that this assessment reflects my objective professional judgment of the pharmacist's "
        "performance based on direct observation and/or review of clinical work during the specified "
        "observation period. This evaluation was conducted in accordance with the institution's peer review "
        "process and is intended to support professional development, not punitive action. I have no conflict "
        "of interest that would compromise the objectivity of this assessment."
    )
    story.append(Paragraph(attest_text, body))
    story.append(Spacer(1, 16))

    attest_data = [
        [Paragraph("Assessor Name & Credentials:", label_bold),
         Paragraph(info.get("assessor_name", "") + " " + info.get("assessor_credentials", ""), body),
         Paragraph("Date:", label_bold),
         Paragraph(str(info.get("assessment_date", "")), body)],
        [Paragraph("Assessor Role:", label_bold),
         Paragraph(info.get("assessor_role", ""), body),
         Paragraph("Signature:", label_bold),
         Paragraph("____________________________", body)],
        [Paragraph("Pharmacist Acknowledgment:", label_bold),
         Paragraph("□ I have reviewed this assessment and discussed it with my assessor.", body),
         Paragraph("Date:", label_bold),
         Paragraph("____________________________", body)],
    ]
    atbl = Table(attest_data, colWidths=[1.8 * inch, 2.4 * inch, 1.0 * inch, 1.8 * inch])
    atbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(atbl)
    story.append(Spacer(1, 16))

    # ── Footer ───────────────────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "CONFIDENTIAL — For Peer Review / Quality Improvement Purposes Only  •  "
        "Protected under applicable peer review confidentiality statutes  •  "
        "Grounded in ASHP Accreditation Standards (2024), ACCP Clinical Pharmacist Competencies (2019), "
        "and JCPP Pharmacists' Patient Care Process  •  Generated by Clinical Pharmacist Assessment Tool v1.0",
        ParagraphStyle("Footer", fontSize=6.5, textColor=colors.HexColor("#94a3b8"),
                       alignment=TA_CENTER, leading=10)
    ))

    doc.build(story)
    buf.seek(0)
    return buf

# ─── CSV EXPORT ───────────────────────────────────────────────────────────────

def export_csv(info, ratings, narratives):
    """Export assessment to a flat CSV suitable for Smartsheet / Excel import."""
    row = {}

    # Info fields
    for k, v in info.items():
        row[k.replace("_", " ").title()] = v

    # Domain averages
    for dom in DOMAINS:
        item_ids = [it["id"] for it in dom["items"]]
        dom_ratings = {k: ratings.get(k) for k in item_ids}
        avg = calc_domain_avg(dom_ratings)
        row[f"Domain Avg — {dom['short']}"] = avg if avg else ""

    # Overall
    all_vals = [v for v in ratings.values() if v and v > 0]
    row["Overall Average Score"] = round(sum(all_vals) / len(all_vals), 2) if all_vals else ""
    row["Overall Performance Category"] = perf_category(row["Overall Average Score"] if row["Overall Average Score"] else None)
    row["Items Rated (n)"] = len(all_vals)

    # Individual item ratings
    for dom in DOMAINS:
        for item in dom["items"]:
            col = f"[{dom['short']}] {item['text'][:80]}"
            v = ratings.get(item["id"])
            row[col] = v if (v and v > 0) else "N/A"

    # Narratives
    row["Strengths"] = narratives.get("strengths", "")
    row["Areas for Development"] = narratives.get("development", "")
    row["Action Plan / Goals"] = narratives.get("goals", "")
    row["Overall Summary"] = narratives.get("summary", "")
    row["Recommended Follow-Up"] = narratives.get("followup", "")
    row["Attestation Confirmed"] = narratives.get("attestation", False)

    df = pd.DataFrame([row])
    buf = BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return buf

# ─── SESSION STATE INITIALIZATION ─────────────────────────────────────────────

def init_state():
    if "ratings" not in st.session_state:
        st.session_state.ratings = {}
    if "page" not in st.session_state:
        st.session_state.page = "assessment"
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

# ─── UI COMPONENTS ────────────────────────────────────────────────────────────

def render_epa_legend():
    st.markdown("""
    <div class='epa-box'>
    <b>EPA Rating Scale (ASHP/ACCP Entrustment Framework)</b><br/>
    <div class='epa-row'><span class='epa-dot' style='background:#dc2626'></span><b>1</b> — Needs Significant Development: significant supervision required</div>
    <div class='epa-row'><span class='epa-dot' style='background:#ea580c'></span><b>2</b> — Developing (Below Expectations): direct supervision required</div>
    <div class='epa-row'><span class='epa-dot' style='background:#ca8a04'></span><b>3</b> — Progressing (Approaching Expectations): indirect supervision</div>
    <div class='epa-row'><span class='epa-dot' style='background:#16a34a'></span><b>4</b> — Meets Expectations (Practice-Ready): independent practice</div>
    <div class='epa-row'><span class='epa-dot' style='background:#2563eb'></span><b>5</b> — Exemplary (Exceeds Expectations): role model / peer resource</div>
    <div class='epa-row'><span class='epa-dot' style='background:#94a3b8'></span><b>N/A</b> — Not observed or not applicable to this pharmacist's current role</div>
    </div>
    """, unsafe_allow_html=True)

def render_domain_ratings(domain, ratings_state):
    """Render all rating items for a domain."""
    st.markdown(f"<div class='domain-header'>{domain['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='domain-desc'>📚 <em>{domain['description']}</em></div>", unsafe_allow_html=True)

    for item in domain["items"]:
        opt_tag = " <small style='color:#94a3b8;'>*(Optional — rate N/A if not applicable to role)*</small>" if item.get("optional") else ""
        st.markdown(f"<div class='item-card'>{item['text']}{opt_tag}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='anchor-hint'>"
            f"<span>⬇ Low: <em>{item['low']}</em></span>"
            f"<span style='text-align:right'>⬆ High: <em>{item['high']}</em></span>"
            f"</div>",
            unsafe_allow_html=True
        )
        current = ratings_state.get(item["id"], 0)
        # Map value back to display option
        reverse_map = {v: k for k, v in RATING_OPTIONS.items()}
        current_label = reverse_map.get(current, "N/A — Not observed / Not applicable to role")
        chosen = st.radio(
            label=" ",
            options=list(RATING_OPTIONS.keys()),
            index=list(RATING_OPTIONS.keys()).index(current_label),
            key=f"radio_{item['id']}",
            horizontal=False,
            label_visibility="collapsed",
        )
        ratings_state[item["id"]] = RATING_OPTIONS[chosen]
        st.divider()

def render_score_summary(ratings):
    """Show domain and overall scores in a visual summary."""
    st.markdown("<div class='section-title'>📊 Assessment Results Preview</div>", unsafe_allow_html=True)

    all_vals = [v for v in ratings.values() if v and v > 0]
    overall = round(sum(all_vals) / len(all_vals), 2) if all_vals else None

    if overall:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(
                f"<div class='overall-box'>"
                f"<div class='big-score'>{overall}</div>"
                f"<div style='font-size:0.75rem;opacity:0.7;'>out of 5.0</div>"
                f"<div class='cat'>{perf_category(overall)}</div>"
                f"<div class='sub'>{len(all_vals)} items rated</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col2:
            for dom in DOMAINS:
                item_ids = [it["id"] for it in dom["items"]]
                avg = calc_domain_avg({k: ratings.get(k) for k in item_ids})
                n = len([v for v in [ratings.get(iid) for iid in item_ids] if v and v > 0])
                clr = score_color(avg)
                bg  = score_bg(avg)
                st.markdown(
                    f"<div class='score-card' style='background:{bg};border-color:{clr}40'>"
                    f"<div class='score-card-title'>{dom['short']}</div>"
                    f"<div class='score-card-value' style='color:{clr}'>"
                    f"{avg if avg else '—'}</div>"
                    f"<div class='score-card-label'>{perf_category(avg)} &nbsp;•&nbsp; {n}/{len(dom['items'])} rated</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
    else:
        st.info("Complete ratings above to see your results preview.")

# ─── PAGES ────────────────────────────────────────────────────────────────────

def page_assessment():
    """Main assessment entry page."""

    st.markdown("""
    <div class='app-header'>
      <h1>⚕️ Clinical Pharmacist Performance Assessment</h1>
      <p>Acute Care Hospital | Manager & Peer Review Tool | ASHP · ACCP · JCPP Standards</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='callout-blue'>
    <b>For Assessors:</b> This tool is designed to support <b>objective, standardized</b> performance assessment
    of clinical pharmacists practicing on an acute care patient care unit. All domains and rating criteria are
    grounded in nationally recognized standards. Complete all applicable items based on <b>direct observation
    and/or documented clinical work</b> during the specified observation period. Rate items <b>N/A</b> only if
    the activity was not observed or is not within the pharmacist's current scope of practice.
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION 1: Assessment Info ─────────────────────────────────────────
    st.markdown("<div class='section-title'>📋 Section 1 — Assessment Information</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        p_name = st.text_input("Pharmacist Being Assessed (Last, First)", placeholder="Smith, Jane")
        p_cred = st.text_input("Pharmacist Credentials", placeholder="PharmD, BCPS")
        unit   = st.selectbox("Clinical Unit / Service", UNIT_OPTIONS)
        assess_type = st.selectbox("Assessment Type", ASSESSMENT_TYPES)
    with c2:
        a_name = st.text_input("Assessor Name (Last, First)", placeholder="Jones, Robert")
        a_cred = st.text_input("Assessor Credentials", placeholder="PharmD, BCPS, BCCCP")
        a_role = st.selectbox("Assessor Role", [
            "Clinical Pharmacy Manager",
            "Peer Clinical Pharmacist",
            "Clinical Pharmacy Coordinator",
            "Pharmacy Director / Associate Director",
            "Residency Program Director (RPD)",
            "Preceptor (Resident/Student Assessment)",
            "Other",
        ])
        assess_date = st.date_input("Assessment Date", value=date.today())

    c3, c4 = st.columns(2)
    with c3:
        obs_start = st.date_input("Observation Period — Start", value=date.today().replace(day=1))
    with c4:
        obs_end = st.date_input("Observation Period — End", value=date.today())

    context_notes = st.text_area(
        "Assessment Context / Additional Notes (optional)",
        placeholder="e.g., Observed during 2 months of MICU rotation; reviewed 15 clinical intervention notes; "
                    "attended rounds 3× per week. Note any extenuating circumstances.",
        height=80,
    )

    info = {
        "pharmacist_name": p_name,
        "pharmacist_credentials": p_cred,
        "unit": unit,
        "assessor_name": a_name,
        "assessor_credentials": a_cred,
        "assessor_role": a_role,
        "assessment_type": assess_type,
        "assessment_date": str(assess_date),
        "obs_start": str(obs_start),
        "obs_end": str(obs_end),
        "context_notes": context_notes,
    }

    # ── SECTION 2: EPA Legend ──────────────────────────────────────────────
    st.markdown("<div class='section-title'>📐 Section 2 — Rating Scale Reference</div>", unsafe_allow_html=True)
    render_epa_legend()

    st.markdown("""
    <div class='callout'>
    <b>Objectivity Reminder:</b> Rate based solely on observed performance and documented clinical work.
    Do not allow personal relationships, demographics, or other non-performance factors to influence ratings.
    The purpose of this tool is professional development and quality improvement.
    </div>
    """, unsafe_allow_html=True)

    # ── SECTION 3–7: Domain Ratings ────────────────────────────────────────
    st.markdown("<div class='section-title'>🩺 Section 3 — Performance Ratings by Domain</div>", unsafe_allow_html=True)
    st.markdown("*Rate each item based on your observations. Use anchor descriptions as calibration guides.*")

    ratings = st.session_state.ratings
    for domain in DOMAINS:
        render_domain_ratings(domain, ratings)

    # ── SECTION 8: Score Summary ───────────────────────────────────────────
    render_score_summary(ratings)

    # ── SECTION 9: Narrative Comments ─────────────────────────────────────
    st.markdown("<div class='section-title'>✍️ Section 4 — Narrative Assessment</div>", unsafe_allow_html=True)
    st.markdown(
        "*Narrative comments are required for all ratings of 1–2 and strongly encouraged for all ratings. "
        "Be specific, objective, and behavior-based.*"
    )

    strengths = st.text_area(
        "Clinical Strengths",
        placeholder="Describe specific, observed strengths with clinical examples. "
                    "e.g., 'Consistently identifies drug-drug interactions on rounds before team notices; "
                    "independently manages complex vancomycin dosing in CRRT patients.'",
        height=130,
    )
    development = st.text_area(
        "Areas for Development",
        placeholder="Describe specific performance gaps with behavioral examples. "
                    "e.g., 'Documentation of clinical interventions is often delayed beyond 24 hours; "
                    "antimicrobial de-escalation opportunities are identified but not always communicated to team.'",
        height=130,
    )
    goals = st.text_area(
        "Action Plan / Goals",
        placeholder="List specific, measurable goals with timelines. "
                    "e.g., '1. Complete all intervention documentation within same shift by [date]. "
                    "2. Propose one antimicrobial stewardship intervention per week at rounds. "
                    "3. Complete BCPS certification revier by Q3.'",
        height=130,
    )
    summary = st.text_area(
        "Overall Performance Summary",
        placeholder="Provide an overall narrative summary of this pharmacist's performance, "
                    "professional trajectory, and readiness for expanded responsibilities.",
        height=110,
    )
    followup = st.selectbox("Recommended Follow-Up Timeline", FOLLOW_UP_OPTIONS)

    # ── SECTION 10: Attestation ────────────────────────────────────────────
    st.markdown("<div class='section-title'>✅ Section 5 — Assessor Attestation</div>", unsafe_allow_html=True)
    st.markdown("""
    *By confirming below, I attest that this assessment reflects my objective professional judgment
    based on direct observation and/or documented clinical work during the specified observation period.
    I confirm no conflict of interest that would compromise objectivity.*
    """)
    attested = st.checkbox("I confirm this assessment is objective, complete, and based on observed performance.")

    narratives = {
        "strengths": strengths,
        "development": development,
        "goals": goals,
        "summary": summary,
        "followup": followup,
        "attestation": attested,
    }

    # ── SECTION 11: Export ─────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📤 Section 6 — Export Assessment</div>", unsafe_allow_html=True)

    if not p_name or not a_name:
        st.warning("⚠️ Please complete the pharmacist name and assessor name fields before exporting.")

    col_csv, col_pdf = st.columns(2)

    with col_csv:
        st.markdown("**Export CSV** — Import directly into Smartsheet, Excel, or any spreadsheet app")
        if st.button("📊 Download CSV", disabled=not (p_name and a_name)):
            csv_buf = export_csv(info, ratings, narratives)
            fname = f"PharmAssessment_{p_name.replace(', ', '_').replace(' ', '_')}_{assess_date}.csv"
            st.download_button(
                label="⬇ Click to Download CSV",
                data=csv_buf,
                file_name=fname,
                mime="text/csv",
            )

    with col_pdf:
        st.markdown("**Export PDF** — Professional report for HR files, accreditation, or peer review records")
        if st.button("📄 Generate PDF Report", disabled=not (p_name and a_name and attested)):
            with st.spinner("Generating PDF report..."):
                pdf_buf = generate_pdf_report(info, ratings, narratives)
            if pdf_buf:
                fname = f"PharmAssessment_{p_name.replace(', ', '_').replace(' ', '_')}_{assess_date}.pdf"
                st.download_button(
                    label="⬇ Click to Download PDF",
                    data=pdf_buf,
                    file_name=fname,
                    mime="application/pdf",
                )
            else:
                st.error("PDF generation requires reportlab. Run: pip install reportlab")

    st.markdown("---")
    st.markdown("""
    <div class='attr'>
    <b>Clinical Pharmacist Assessment Tool v1.0</b><br/>
    Domains grounded in: ASHP Accreditation Standard for Postgraduate Residency Programs (2024) •
    ACCP Clinical Pharmacist Competencies (JACCP 2019) •
    JCPP Pharmacists' Patient Care Process (PPCP) •
    ASHP Practice Advancement Initiative (PAI) 2030<br/>
    <em>Confidential — Peer Review Protected Document</em>
    </div>
    """, unsafe_allow_html=True)


def page_about():
    """About page with references and methodology."""
    st.markdown("""
    <div class='app-header'>
      <h1>📚 About This Tool — Standards & References</h1>
      <p>Methodology, evidence base, and accreditation alignment</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Purpose")
    st.markdown("""
    This tool provides a **standardized, objective framework** for assessing the clinical performance of
    pharmacists practicing on acute care hospital patient care units. It is designed for use by clinical
    pharmacy managers and peer pharmacists conducting formal or informal performance reviews.

    The tool explicitly addresses criteria identified in the **ASHP Residency Accreditation Standard**
    as relevant to measuring pharmacist clinical performance, and is calibrated to the level of
    a practice-ready acute care clinical pharmacist (EPA Level 4).
    """)

    st.markdown("### Standards Alignment")

    with st.expander("🏥 ASHP Accreditation Standard (2024) — PGY1 Required Competency Areas"):
        st.markdown("""
        The ASHP Accreditation Standard for Postgraduate Residency Programs (2024) defines four
        **Required Competency Areas** for PGY1 programs. This assessment tool maps to all four:

        | ASHP Competency Area | Assessment Domain |
        |---|---|
        | **R1 — Patient Care** | Domain 1 (PPCP) + Domain 2 (Drug Therapy) + Domain 3 (Communication) |
        | **R2 — Advancing Practice and Improving Patient Care** | Domain 4 (Systems/Quality/Safety) |
        | **R3 — Leadership and Management** | Domain 5 (Leadership & Development) |
        | **R4 — Teaching, Education, and Dissemination of Knowledge** | Domain 5 (item: preceptor/educator) |

        *Source: [ASHP PGY1 Harmonized CAGO (2024)](https://www.ashp.org/-/media/assets/professional-development/residencies/docs/PGY1-Harmonized-CAGO-BOD-Approved-2024.pdf)*
        """)

    with st.expander("🧪 ACCP Clinical Pharmacist Competencies"):
        st.markdown("""
        The ACCP Clinical Pharmacist Competencies (JACCP, 2019) define **six core competency domains**
        for direct patient care pharmacists. This tool covers all six:

        | ACCP Competency Domain | Assessment Domain |
        |---|---|
        | Direct Patient Care | Domain 1 (PPCP) |
        | Pharmacotherapy Knowledge | Domain 2 (Drug Therapy & Knowledge) |
        | Systems-Based Care & Population Health | Domain 4 (Systems, Quality & Safety) |
        | Communication | Domain 3 (Communication & Collaboration) |
        | Professionalism | Domain 5 (Leadership & Development) |
        | Continuing Professional Development | Domain 5 (item: self-directed learning) |

        *Source: Engle JP et al. ACCP Clinical Pharmacist Competencies. JACCP. 2019;2(6):550-556.*
        """)

    with st.expander("🔄 JCPP Pharmacists' Patient Care Process (PPCP)"):
        st.markdown("""
        The **Pharmacists' Patient Care Process** (PPCP), published by the Joint Commission of Pharmacy
        Practitioners (JCPP) and endorsed by ASHP, ACCP, APhA, and all major pharmacy organizations,
        provides the foundational framework for Domain 1 of this assessment.

        The five steps — **Collect, Assess, Plan, Implement, Follow-up/Monitor** — are assessed as
        distinct competencies with behavioral anchors appropriate for acute care practice.

        *Source: JCPP. Pharmacists' Patient Care Process. 2014. Endorsed by ASHP, ACCP, APhA.*
        """)

    with st.expander("📊 EPA Rating Scale"):
        st.markdown("""
        The **Entrustable Professional Activities (EPA)** framework, adapted for practicing pharmacists,
        is used as the 5-point rating scale. This scale is consistent with ASHP residency evaluation
        language and ACGME milestone frameworks:

        | Level | Label | Meaning |
        |---|---|---|
        | 1 | Needs Significant Development | Significant supervision required; potential patient safety concern |
        | 2 | Developing | Direct supervision required; below expectations |
        | 3 | Progressing | Indirect supervision; approaching expectations |
        | 4 | Meets Expectations | Practice-ready; independent practice; meets all standards |
        | 5 | Exemplary | Exceeds expectations; role model; advances practice |

        *Level 4 (Meets Expectations) is the expected standard for a competent acute care clinical pharmacist.*
        """)

    st.markdown("### References")
    st.markdown("""
    1. ASHP. *Accreditation Standard for Postgraduate Year One (PGY1) Pharmacy Residency Programs.* 2024.
       [ashp.org](https://www.ashp.org/professional-development/residency-information)

    2. ASHP. *PGY1 Required Competency Areas, Goals, and Objectives (Harmonized CAGO).* Board Approved 2024.
       [PDF](https://www.ashp.org/-/media/assets/professional-development/residencies/docs/PGY1-Harmonized-CAGO-BOD-Approved-2024.pdf)

    3. Engle JP, et al. *ACCP Clinical Pharmacist Competencies.*
       Journal of the American College of Clinical Pharmacy. 2019;2(6):550-556.
       [PubMed](https://pubmed.ncbi.nlm.nih.gov/28464300/)

    4. Joint Commission of Pharmacy Practitioners (JCPP).
       *Pharmacists' Patient Care Process.* 2014.
       Endorsed by ASHP, ACCP, APhA, AACP, NACDS, NCPA, AMCP.

    5. ASHP. *Practice Advancement Initiative (PAI) 2030.*
       [ashp.org/PAI2030](https://www.ashp.org/pharmacy-practice/pai)

    6. Murphy JE, et al. *ACCP Comprehensive Medication Management in Team-Based Care.*
       Pharmacotherapy. 2019;39(10):923-935.
    """)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    init_state()

    with st.sidebar:
        st.markdown("### ⚕️ Clinical Pharmacist Assessment")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            ["📋 New Assessment", "📚 About & Standards"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.markdown("""
        **Quick Tips:**
        - Rate all observed items
        - Use N/A only for unobserved activities
        - Narrative comments required for ratings of 1–2
        - Attest before generating PDF
        - CSV exports to Smartsheet-ready format
        """)
        st.markdown("---")
        st.caption("v1.0 | ASHP · ACCP · JCPP\nConfidential — Peer Review Protected")

    if "Assessment" in page:
        page_assessment()
    else:
        page_about()


if __name__ == "__main__":
    main()
