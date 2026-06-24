def run_rca(logs):
  text = logs.lower()
  causes = []
  catagory = "unknown"
  confidence = "low"
  impact = "System distruption observed"
  fix = "Investigate further"

#infra
if "oom" in text or "memory" in text:
  causes.append("Memory exhaustion (OOMKILLED)")
  category = "infrastructure"
  confidence = "high"
  impact = "Container restart / downtime"
  fix = "Increase memory limits"

#CI/CD
elif "pipeline" in text or "build failed" in text or "test suite failed" in text:
  causes.append("CI/CD pipeline failure due to failing tests")
  category = "ci/cd"
  confidence = "high"
  impact = "Build failed -> deployment blocked"
  fix = "Fix failing test cases or rollback code"

#AUTH
elif "unauthorized" in text or "jwt" in text:
  causes.append("Authentication failure")
  category = "security"
  confidence = "high"
  impact = "Access denined"
  fix = "Validate tokens"

return {
  "root_cause": causes[0] if causes else "Unknown issue"
  "impact": impact,
  "confidence": confidence,
  "category": category,
  "recommended_fix": fix
}
