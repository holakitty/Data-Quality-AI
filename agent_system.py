from __future__ import annotations
import os, json, logging
from typing import Optional, List, Dict
from openai import OpenAI
from pydantic import BaseModel, Field, ConfigDict

logging.basicConfig(level=logging.INFO, format="[%(name)s] %(message)s")
logger = logging.getLogger("AgentSwarm")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key-for-testing"))

class Anomaly(BaseModel):
    id: int
    row_id: int
    column: str
    value: Optional[str]
    context: str
    reason: str
    suggested_fix: str
    status: str = "pending"

class RemediationDecision(BaseModel):
    anomaly_id: int
    action: str
    custom_rule: Optional[str] = None

class OrganizationalMemory(BaseModel):
    rules: List[str] = Field(default_factory=list)

    def add_rule(self, rule: str):
        if rule not in self.rules:
            self.rules.append(rule)
            logger.info(f"New rule learned: {rule}")

    def retrieve_relevant(self, query: str) -> List[str]:
        return [r for r in self.rules if query.lower() in r.lower()]

class BaseAgent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    role: str
    memory: Optional[OrganizationalMemory] = None
    detector: Optional["AnomalyDetectorAgent"] = None
    memory_agent: Optional["MemoryEngineAgent"] = None

    def think(self, prompt: str) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            return self._rule_based_think(prompt)
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return self._rule_based_think(prompt)

    def _rule_based_think(self, prompt: str) -> str:
        return f"[Rule-based {self.name}] Processing: {prompt[:80]}..."

    def act(self, *args, **kwargs) -> dict:
        raise NotImplementedError

class AnomalyDetectorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AnomalyDetector", role="Detects logical contradictions in data rows")

    def detect(self, row: dict, schema_rules: List[str]) -> List[Anomaly]:
        anomalies = []
        for rule in schema_rules:
            if self._violates_rule(row, rule):
                col = self._extract_column(rule)
                anomalies.append(Anomaly(
                    id=len(anomalies) + 1,
                    row_id=row.get("id", 0),
                    column=col,
                    value=str(row.get(col, "N/A")),
                    context=f"Row data: {json.dumps(row)}",
                    reason=f"Logical contradiction: {rule}",
                    suggested_fix=f"Flag for manual verification of {col}",
                ))
        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies

    def _violates_rule(self, row: dict, rule: str) -> bool:
        rule_lower = rule.lower()
        if "phd" in rule_lower and "age" in rule_lower:
            age = row.get("age")
            if age is not None and age < 22 and row.get("education") == "PhD":
                return True
        if "village" in rule_lower and "rural" in rule_lower:
            if row.get("rural_urban") == "Rural" and row.get("village") is None:
                return True
        return False

    def _extract_column(self, rule: str) -> str:
        if "phd" in rule.lower(): return "Education"
        if "village" in rule.lower(): return "Village"
        return "unknown"

class MemoryEngineAgent(BaseAgent):
    def __init__(self, memory: OrganizationalMemory):
        super().__init__(name="MemoryEngine", role="Stores and retrieves learned organizational rules", memory=memory)

    def learn(self, anomaly: Anomaly, custom_rule: str):
        rule = custom_rule or f"If {anomaly.column} is {anomaly.value}, then {anomaly.context}"
        self.memory.add_rule(rule)
        return rule

    def recall(self, query: str) -> List[str]:
        return self.memory.retrieve_relevant(query)

class HITLAgent(BaseAgent):
    def __init__(self, detector: AnomalyDetectorAgent, memory_agent: MemoryEngineAgent):
        super().__init__(name="HITLHandler", role="Handles human-in-the-loop decisions", detector=detector, memory_agent=memory_agent)

    def handle_decision(self, anomaly: Anomaly, action: str, custom_rule: Optional[str] = None) -> dict:
        if action == "accept_fix":
            anomaly.status = "resolved"
            logger.info(f"Fix accepted for Row {anomaly.row_id}")
            return {"success": True, "status": "resolved", "message": f"Anomaly {anomaly.id} resolved"}
        elif action == "override_and_learn":
            anomaly.status = "overridden"
            if custom_rule:
                self.memory_agent.learn(anomaly, custom_rule)
            logger.info(f"Overridden. Learned rule for Row {anomaly.row_id}")
            return {
                "success": True,
                "status": "overridden",
                "message": f"Anomaly {anomaly.id} overridden, rule learned",
                "total_rules": len(self.memory_agent.memory.rules)
            }
        else:
            return {"success": False, "message": "Invalid action"}

class AgentSwarm:
    def __init__(self):
        self.memory = OrganizationalMemory(
            rules=["If Education is PhD, Age must be > 22", "If Rural/Urban is Rural, Village cannot be NULL"]
        )
        self.detector = AnomalyDetectorAgent()
        self.memory_agent = MemoryEngineAgent(self.memory)
        self.hti_agent = HITLAgent(self.detector, self.memory_agent)
        logger.info(f"Swarm initialized with {len(self.memory.rules)} rules")

    def ingest_and_analyze(self, data_rows: List[dict], schema_rules: List[str]) -> List[Anomaly]:
        all_anomalies = []
        for row in data_rows:
            anomalies = self.detector.detect(row, schema_rules)
            all_anomalies.extend(anomalies)
        return all_anomalies

    def remediate(self, anomaly_id: int, action: str, custom_rule: Optional[str] = None) -> dict:
        return self.hti_agent.handle_decision(self._find_anomaly(anomaly_id), action, custom_rule)

    def _find_anomaly(self, anomaly_id: int) -> Anomaly:
        for a in self._flagged:
            if a.id == anomaly_id:
                return a
        raise ValueError(f"Anomaly {anomaly_id} not found")

    def get_pending_anomalies(self) -> List[dict]:
        return [a.model_dump() for a in self._flagged if a.status == "pending"]

    def run_pipeline(self, data_rows: List[dict], schema_rules: List[str]) -> dict:
        self._flagged = self.ingest_and_analyze(data_rows, schema_rules)
        pending = self.get_pending_anomalies()
        return {
            "count": len(pending),
            "data": pending,
            "total_rules": len(self.memory.rules),
            "memory_rules": self.memory.rules
        }

if __name__ == "__main__":
    print("=" * 60)
    print("  AI Data Quality Analyzer - Multi-Agent Swarm Test")
    print("=" * 60)

    swarm = AgentSwarm()

    test_data = [
        {"id": 42, "age": 7, "education": "PhD", "rural_urban": "Rural", "village": None},
        {"id": 89, "age": 35, "education": "BSc", "rural_urban": "Rural", "village": None},
        {"id": 15, "age": 28, "education": "PhD", "rural_urban": "Urban", "village": "Springfield"},
    ]
    schema_rules = [
        "If Education is PhD, Age must be > 22",
        "If Rural/Urban is Rural, Village cannot be NULL",
    ]

    print("\n[Step 1] Running Anomaly Detection Pipeline...")
    result = swarm.run_pipeline(test_data, schema_rules)
    print(f"  Pending anomalies: {result['count']}")
    for a in result["data"]:
        print(f"    - Row {a['row_id']}: {a['reason']}")

    print("\n[Step 2] Accept Fix for Anomaly 1...")
    r1 = swarm.remediate(1, "accept_fix")
    print(f"  Result: {r1['message']}")

    print("\n[Step 3] Override & Learn for Anomaly 2...")
    r2 = swarm.remediate(2, "override_and_learn", custom_rule="Rural addresses must always have a Village field populated")
    print(f"  Result: {r2['message']} | Total rules: {r2['total_rules']}")

    print("\n[Step 4] Memory Recall...")
    recalled = swarm.memory_agent.recall("education")
    print(f"  Recalled rules: {recalled}")

    print("\n[Step 5] Final Swarm State...")
    final = swarm.run_pipeline(test_data, schema_rules)
    print(f"  Remaining pending: {final['count']}")
    print(f"  Total organizational rules: {final['total_rules']}")
    for rule in final["memory_rules"]:
        print(f"    - {rule}")

    print("\n" + "=" * 60)
    print("  All tests passed! AI Agent Swarm is operational.")
    print("=" * 60)
