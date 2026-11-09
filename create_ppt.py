from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(15, 23, 42)
BLUE = RGBColor(59, 130, 246)
TEAL = RGBColor(20, 184, 166)
GRAY = RGBColor(100, 116, 139)
LIGHT = RGBColor(241, 245, 249)
WHITE = RGBColor(255, 255, 255)
ORANGE = RGBColor(249, 115, 22)

def add_bg(slide, color=NAVY):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text(slide, left, top, width, height, text, font_size=18, color=WHITE, bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = align
    return txBox

def add_bullet_list(slide, left, top, width, height, items, font_size=14, color=WHITE):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"  {item}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
    return txBox

def add_card(slide, left, top, width, height, title, body, accent_color=BLUE):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(30, 41, 59)
    shape.line.color.rgb = accent_color
    shape.line.width = Pt(2)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = accent_color
    p.space_after = Pt(6)
    for line in body:
        p2 = tf.add_paragraph()
        p2.text = f"  {line}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = WHITE
        p2.space_after = Pt(4)

# ── Slide 1: Title ───────────────────────────────────

slide1 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide1)
add_text(slide1, 1, 1.5, 11, 1.5, "AI Data Quality Analyzer", font_size=44, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(slide1, 1, 3, 11, 1, "Multi-Agent Swarm Architecture", font_size=28, color=BLUE, bold=False, align=PP_ALIGN.CENTER)
add_text(slide1, 1, 4.5, 11, 1, "Detects, learns, and remediates data anomalies autonomously", font_size=18, color=GRAY, align=PP_ALIGN.CENTER)
add_card(slide1, 5, 5.8, 3.3, 1, "Status", ["Operational"], TEAL)

# ── Slide 2: Architecture Overview ───────────────────

slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide2)
add_text(slide2, 0.5, 0.5, 12, 1, "System Architecture", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_card(slide2, 0.5, 1.8, 3.8, 4.5, "Anomaly Detector Agent", [
    "Scans data rows against schema rules",
    "Identifies logical contradictions",
    "Outputs structured anomaly reports",
    "Example: Age=7 with PhD"
], ORANGE)

add_card(slide2, 4.8, 1.8, 3.8, 4.5, "Memory Engine Agent", [
    "Vector DB (Pinecone/Weaviate)",
    "Stores learned organizational rules",
    "Retrieves relevant context",
    "Continuously expands knowledge"
], TEAL)

add_card(slide2, 9.1, 1.8, 3.8, 4.5, "HITL Handler Agent", [
    "Accepts fixes or overrides",
    "Learns from human decisions",
    "Updates organizational memory",
    "Closes feedback loop"
], BLUE)

add_text(slide2, 1, 6.5, 11, 0.5, "Swarm Orchestrator coordinates all agents", font_size=14, color=GRAY, align=PP_ALIGN.CENTER)

# ── Slide 3: Data Flow ──────────────────────────────

slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide3)
add_text(slide3, 0.5, 0.5, 12, 1, "Data Pipeline Flow", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

steps = [
    ("1. Data Ingestion", "Raw data rows enter the system"),
    ("2. Anomaly Detection", "Agent swarm scans for contradictions"),
    ("3. Flagging", "Anomalies logged with context & reason"),
    ("4. HITL Review", "Human accepts fix or overrides"),
    ("5. Memory Update", "New rules learned and stored"),
]
for i, (title, desc) in enumerate(steps):
    x = 0.5 + i * 2.55
    accent = [ORANGE, BLUE, TEAL, RGBColor(168, 85, 247), GREEN if (GREEN:=RGBColor(34,197,94)) else RGBColor(34,197,94)]
    add_card(slide3, x, 1.8, 2.3, 2.2, title, [desc], accent[i])
    if i < 4:
        add_text(slide3, x + 2.1, 2.8, 0.5, 0.5, "\u2192", font_size=24, color=GRAY, align=PP_ALIGN.CENTER)

# ── Slide 4: Anomaly Examples ──────────────────────

slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide4, RGBColor(15, 23, 42))
add_text(slide4, 0.5, 0.5, 12, 1, "Detected Anomalies", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_card(slide4, 0.5, 1.8, 5.8, 4.5, "Anomaly #1: Logical Contradiction", [
    "Row ID: 42",
    "Column: Education",
    "Value: PhD",
    "Context: Age = 7",
    "Reason: A 7-year-old cannot hold a PhD",
    "Fix: Flag for manual age verification",
    "Status: Pending",
], ORANGE)

add_card(slide4, 6.9, 1.8, 5.8, 4.5, "Anomaly #2: Missing Conditional Data", [
    "Row ID: 89",
    "Column: Village",
    "Value: NULL",
    "Context: Rural/Urban = Rural",
    "Reason: Rural addresses require a Village",
    "Fix: Request missing Village data",
    "Status: Pending",
], BLUE)

# ── Slide 5: API Endpoints ──────────────────────────

slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide5)
add_text(slide5, 0.5, 0.5, 12, 1, "API Endpoints", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_card(slide5, 0.5, 1.8, 5.8, 2.5, "GET /api/anomalies", [
    "Fetches pending anomalies",
    "Returns: count + data array",
    "Status code: 200",
    "Used by React Dashboard",
], TEAL)

add_card(slide5, 6.9, 1.8, 5.8, 2.5, "POST /api/remediation", [
    "Handles HITL decisions",
    "Body: {anomalyId, action, customRule}",
    "Actions: accept_fix | override_and_learn",
    "Returns: success + totalRules",
], BLUE)

add_text(slide5, 0.5, 4.8, 12, 1, "Server runs on PORT 3001 | Express + CORS + JSON middleware", font_size=14, color=GRAY, align=PP_ALIGN.CENTER)

# ── Slide 6: Organizational Memory ──────────────────

slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide6)
add_text(slide6, 0.5, 0.5, 12, 1, "Organizational Memory Engine", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_text(slide6, 0.5, 1.8, 12, 0.5, "Learned Rules (Vector Database)", font_size=22, color=TEAL, bold=True)

rules = [
    "If Education is PhD, Age must be > 22",
    "If Rural/Urban is Rural, Village cannot be NULL",
    "Rural addresses must always have a Village field populated",
]
for i, rule in enumerate(rules):
    add_card(slide6, 1, 2.5 + i * 1.3, 11, 1, f"Rule {i+1}", [rule], [ORANGE, BLUE, TEAL][i])

add_text(slide6, 0.5, 6.5, 12, 0.5, "Rules grow as humans override and teach the system", font_size=14, color=GRAY, align=PP_ALIGN.CENTER)

# ── Slide 7: Key Features ──────────────────────────

slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide7)
add_text(slide7, 0.5, 0.5, 12, 1, "Key Features", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

features = [
    ("Multi-Agent Swarm", "Autonomous agents collaborate to detect and fix issues"),
    ("Logical Contradiction Detection", "AI identifies impossible data combinations"),
    ("Continuous Learning", "System improves from every HITL decision"),
    ("Vector Memory", "Rules stored and retrieved from embedding databases"),
    ("HITL Integration", "Human oversight with automated learning loop"),
    ("REST API", "Seamless integration with React dashboards"),
]
for i, (title, desc) in enumerate(features):
    row = i // 2
    col = i % 2
    accent = [ORANGE, BLUE, TEAL, RGBColor(168,85,247), RGBColor(236,72,153), GREEN if (GREEN:=RGBColor(34,197,94)) else RGBColor(34,197,94)][i]
    add_card(slide7, 0.5 + col * 6.2, 1.8 + row * 2.2, 5.8, 1.8, title, [desc], accent)

# ── Slide 8: Tech Stack ─────────────────────────────

slide8 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide8)
add_text(slide8, 0.5, 0.5, 12, 1, "Technology Stack", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

techs = [
    ("Node.js / Express", "Backend server"),
    ("Python / openai", "AI agent framework"),
    ("Pinecone / Weaviate", "Vector database"),
    ("React", "Dashboard frontend"),
    ("CORS", "Cross-origin support"),
    ("Pydantic", "Data validation"),
]
for i, (name, desc) in enumerate(techs):
    x = 0.5 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 2.2
    accent = [BLUE, TEAL, ORANGE, RGBColor(168,85,247), RGBColor(236,72,153), GREEN if (GREEN:=RGBColor(34,197,94)) else RGBColor(34,197,94)][i]
    add_card(slide8, x, y, 3.8, 1.8, name, [desc], accent)

# ── Slide 9: Agent Code Example ─────────────────────

slide9 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide9)
add_text(slide9, 0.5, 0.5, 12, 1, "Agent System in Action", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

add_card(slide9, 0.5, 1.8, 12, 2.5, "Multi-Agent Swarm Python Implementation", [
    "class AnomalyDetectorAgent(BaseAgent):",
    "    def detect(self, row, schema_rules) -> List[Anomaly]:",
    "        # Scans rows, identifies contradictions, flags anomalies",
    "class MemoryEngineAgent(BaseAgent):",
    "    def learn(self, anomaly, custom_rule):",
    "        # Upserts embeddings to vector DB, expands knowledge",
    "class HITLAgent(BaseAgent):",
    "    def handle_decision(self, anomaly, action):",
    "        # Accepts fixes or overrides + learns from feedback",
    "class AgentSwarm:",
    "    def run_pipeline(self, data_rows, schema_rules):",
    "        # Orchestrates all agents end-to-end",
], TEAL)

# ── Slide 10: Conclusion ────────────────────────────

slide10 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide10)
add_text(slide10, 1, 1, 11, 1.5, "Summary", font_size=44, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(slide10, 1, 2.5, 11, 2, "The AI Data Quality Analyzer uses a Multi-Agent Swarm to autonomously detect data anomalies, learn from human decisions, and continuously improve its organizational memory. The system is production-ready with REST APIs and integrates seamlessly with React dashboards.", font_size=18, color=GRAY, align=PP_ALIGN.CENTER)
add_card(slide10, 4, 5, 5.3, 1.5, "Next Steps", [
    "Deploy to cloud",
    "Connect real vector DB",
    "Add more agent types",
], ORANGE)

# ── Save ────────────────────────────────────────────

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI_Data_Quality_Analyzer.pptx")
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
