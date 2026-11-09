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

# === PART 2: Agent Deep Dive ===
# Slide 1
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 1, 1.5, 11, 1.5, "Part 2: Agent Deep Dive", font_size=44, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(s, 1, 3, 11, 1, "Multi-Agent Architecture Patterns", font_size=28, color=BLUE, align=PP_ALIGN.CENTER)

# Slide 2 - Agent Types
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Agent Types in the System", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_card(s, 0.5, 1.8, 3.8, 4.5, "Reactive Agent", [
    "Responds to immediate data events",
    "No memory of past interactions",
    "Fast inference, low overhead",
    "Best for real-time detection"
], ORANGE)
add_card(s, 4.8, 1.8, 3.8, 4.5, "Deliberative Agent", [
    "Plans ahead using schema rules",
    "Considers multiple scenarios",
    "Uses organizational memory",
    "Best for complex analysis"
], TEAL)
add_card(s, 9.1, 1.8, 3.8, 4.5, "Social Agent", [
    "Communicates with other agents",
    "Shares findings and context",
    "Collaborative problem solving",
    "Best for swarm coordination"
], PURPLE)

# Slide 3 - Communication Patterns
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Communication Patterns", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
patterns = [
    ("Broadcast", "All agents receive same event"),
    ("Direct Message", "Point-to-point agent comms"),
    ("Shared Memory", "Centralized knowledge store"),
    ("Event Bus", "Publish/subscribe model"),
]
for i, (name, desc) in enumerate(patterns):
    x = 0.5 + (i % 2) * 6.2
    y = 1.8 + (i // 2) * 2.5
    add_card(s, x, y, 5.8, 2, name, [desc], [ORANGE, BLUE, TEAL, PURPLE][i])

# Slide 4 - Agent Lifecycle
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Agent Lifecycle", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
lifecycle = [
    ("1. Initialization", "Load config, connect to memory"),
    ("2. Idle / Listening", "Wait for events or triggers"),
    ("3. Processing", "Analyze data, run inference"),
    ("4. Decision", "Choose action based on reasoning"),
    ("5. Action", "Execute, update state, notify swarm"),
    ("6. Reflection", "Learn from outcomes, update memory"),
]
for i, (stage, desc) in enumerate(lifecycle):
    x = 0.5 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 2.5
    add_card(s, x, y, 3.8, 2, stage, [desc], [ORANGE, BLUE, TEAL][i % 3])

# Slide 5 - Concurrency & Parallelism
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Concurrency Model", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_card(s, 0.5, 1.8, 5.8, 4.5, "Parallel Agent Execution", [
    "Each agent runs independently",
    "No blocking on other agents",
    "Event-driven architecture",
    "Scales horizontally with load",
    "Async/await for non-blocking IO",
    "Worker pool for heavy tasks"
], TEAL)
add_card(s, 6.9, 1.8, 5.8, 4.5, "Synchronization Strategies", [
    "Mutex locks on shared memory",
    "Message queues for ordering",
    "Consensus on critical decisions",
    "Event sourcing for audit trail",
    "Checkpoint-based recovery",
    "Conflict resolution protocols"
], ORANGE)

# Slide 6 - Error Handling
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Error Handling & Resilience", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_card(s, 0.5, 1.8, 3.8, 4.5, "Failure Modes", [
    "Agent timeout",
    "LLM API failure",
    "Memory store unreachable",
    "Invalid data input",
    "Network partition",
], ORANGE)
add_card(s, 4.8, 1.8, 3.8, 4.5, "Recovery Strategies", [
    "Retry with exponential backoff",
    "Fallback to rule-based logic",
    "Circuit breaker pattern",
    "Graceful degradation",
    "Dead letter queue",
], TEAL)
add_card(s, 9.1, 1.8, 3.8, 4.5, "Monitoring", [
    "Health checks per agent",
    "Latency tracking",
    "Error rate dashboards",
    "Alert on anomaly spikes",
    "Logging & tracing",
], PURPLE)

# Slide 7 - Testing Agents
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Testing the Agent System", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_card(s, 0.5, 1.8, 5.8, 4.5, "Unit Testing Agents", [
    "Mock LLM responses",
    "Test detect() with known inputs",
    "Verify anomaly classification",
    "Test memory add/retrieve",
    "Validate remediation logic",
], ORANGE)
add_card(s, 6.9, 1.8, 5.8, 4.5, "Integration Testing", [
    "Full pipeline end-to-end",
    "Multi-agent interaction tests",
    "Load testing with 1000+ rows",
    "Verify state consistency",
    "HITL decision flow tests",
], TEAL)

# Slide 8 - Scaling
s = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(s)
add_text(s, 0.5, 0.5, 12, 1, "Scaling to Production", font_size=36, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
scaling = [
    ("Horizontal Scaling", "Spin up agent instances per workload"),
    ("Queue-Based Load", "RabbitMQ/Celery for job distribution"),
    ("Caching Layer", "Redis for frequent memory lookups"),
    ("Model Optimization", "Quantized models, caching embeddings"),
    ("Load Balancing", "Distribute across worker nodes"),
]
for i, (title, desc) in enumerate(scaling):
    x = 0.5 + (i % 3) * 4.1
    y = 1.8 + (i // 3) * 2.5
    add_card(s, x, y, 3.8, 2, title, [desc], [ORANGE, BLUE, TEAL][i % 3])

# Save Part 2
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Part2_Agent_Deep_Dive.pptx")
prs.save(output_path)
print(f"Part 2 saved: {output_path}")
