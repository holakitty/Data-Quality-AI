from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(15, 23, 42)
BLUE = RGBColor(59, 130, 246)
TEAL = RGBColor(20, 184, 166)
GRAY = RGBColor(100, 116, 139)
WHITE = RGBColor(255, 255, 255)
ORANGE = RGBColor(249, 115, 22)
PURPLE = RGBColor(168, 85, 247)
GREEN = RGBColor(34, 197, 94)
PINK = RGBColor(236, 72, 153)

def add_bg(slide, color=NAVY):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

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

def add_card(slide, left, top, width, height, title, body, accent_color=BLUE, body_size=12):
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
        p2.font.size = Pt(body_size)
        p2.font.color.rgb = WHITE
        p2.space_after = Pt(4)

# === PART 3: Advanced Topics ===
# Slide 1 - Title
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 1, 1.5, 11, 1.5, "Part 3: Advanced Topics", font_size=44, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(s, 1, 3, 11, 1, "Next-Level AI Agent Systems", font_size=28, color=BLUE, align=PP_ALIGN.CENTER)

# Slide 2 - LLM Integration
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "LLM Integration Patterns", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
patterns = [
    ("Direct API Call", "OpenAI / Anthropic / Groq"),
    ("RAG Pipeline", "Retrieve-Generate with memory"),
    ("Function Calling", "Agents call tools/APIs"),
    ("Chain of Thought", "Step-by-step reasoning"),
    ("Multi-Step Planning", "ReAct framework"),
]
for i, (name, desc) in enumerate(patterns):
    x = 0.5 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 2.5
    add_card(s, x, y, 3.8, 2, name, [desc], [ORANGE, BLUE, TEAL][i % 3])

# Slide 3 - RAG Architecture
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "RAG Architecture for Agents", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_card(s, 0.5, 1.8, 6, 4.5, "Data Flow", [
    "1. User query enters",
    "2. Embed query into vector space",
    "3. Search Pinecone/Weaviate",
    "4. Retrieve top-k relevant rules",
    "5. Augment prompt with retrieved context",
    "6. Generate response from LLM",
    "7. Return answer with sources"
], TEAL)
add_card(s, 6.9, 1.8, 5.8, 4.5, "Components", [
    "Embedding Model (text-embedding-3-small)",
    "Vector Database (Pinecone / Weaviate)",
    "Retrieval Engine (similarity search)",
    "Prompt Builder (context injection)",
    "LLM Generator (gpt-4o-mini)",
], ORANGE)

# Slide 4 - Multi-Agent Frameworks
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Multi-Agent Frameworks", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
frameworks = [
    ("LangGraph", "Stateful agent graphs"),
    ("CrewAI", "Role-based agent teams"),
    ("AutoGen", "Conversational agents"),
    ("MetaGPT", "Software company simulation"),
]
for i, (name, desc) in enumerate(frameworks):
    x = 0.5 + (i % 2) * 6.2
    y = 1.8 + (i // 2) * 2.5
    add_card(s, x, y, 5.8, 2, name, [desc], [BLUE, TEAL, ORANGE, PURPLE][i])

# Slide 5 - Evaluation Metrics
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Agent Evaluation Metrics", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
metrics = [
    ("Accuracy", "Correct anomaly detection rate"),
    ("Precision", "Low false positive rate"),
    ("Recall", "All real anomalies caught"),
    ("F1 Score", "Balance of precision/recall"),
    ("Latency", "Response time per agent call"),
    ("Cost", "API token usage per task"),
]
for i, (name, desc) in enumerate(metrics):
    x = 0.5 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 2.5
    add_card(s, x, y, 3.8, 2, name, [desc], [ORANGE, BLUE, TEAL][i % 3])

# Slide 6 - Production Deployment
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Production Deployment", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
deploy = [
    ("Docker Container", "Package all dependencies"),
    ("Kubernetes", "Orchestrate agent pods"),
    ("CI/CD Pipeline", "Auto-deploy on commit"),
    ("Health Monitoring", "Uptime & performance"),
    ("Auto-scaling", "Handle traffic spikes"),
]
for i, (name, desc) in enumerate(deploy):
    x = 0.5 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 2.5
    add_card(s, x, y, 3.8, 2, name, [desc], [ORANGE, BLUE, TEAL][i % 3])

# Slide 7 - Security & Governance
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Security & Governance", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_card(s, 0.5, 1.8, 5.8, 4.5, "Security Best Practices", [
    "API key rotation & secrets management",
    "Input validation & sanitization",
    "Rate limiting on all endpoints",
    "TLS encryption in transit",
    "Role-based access control",
], ORANGE)
add_card(s, 6.9, 1.8, 5.8, 4.5, "Governance", [
    "Audit logs for all agent actions",
    "Human approval for critical ops",
    "Explainability & transparency",
    "Bias detection in AI decisions",
    "Compliance with data regulations",
], TEAL)

# Slide 8 - Learning Path
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Learning Path", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
steps = [
    ("Step 1", "Python Basics + OpenAI API"),
    ("Step 2", "Single Agent Systems"),
    ("Step 3", "Multi-Agent Orchestration"),
    ("Step 4", "Vector Databases & RAG"),
    ("Step 5", "Production Deployment"),
    ("Step 6", "Advanced Frameworks"),
]
for i, (step, topic) in enumerate(steps):
    x = 0.5 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 2.5
    add_card(s, x, y, 3.8, 2, step, [topic], [ORANGE, BLUE, TEAL][i % 3])

# Save Part 3
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Part3_Advanced_Topics.pptx")
prs.save(output_path)
print(f"Part 3 saved: {output_path}")
