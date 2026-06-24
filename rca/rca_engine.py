def run_rca(logs):
    """
    Analyze logs and determine root cause of failure.
    
    Args:
        logs: Raw log text to analyze
        
    Returns:
        dict: RCA analysis with root_cause, impact, confidence, category, and recommended_fix
    """
    text = logs.lower()
    causes = []
    category = "unknown"
    confidence = "low"
    impact = "System disruption observed"
    fix = "Investigate further"

    # Infrastructure - Memory issues
    if "oom" in text or "memory" in text or "out of memory" in text:
        causes.append("Memory exhaustion (OOMKILLED)")
        category = "infrastructure"
        confidence = "high"
        impact = "Container restart / downtime"
        fix = "Increase memory limits or optimize memory usage"

    # Infrastructure - Disk space
    elif "disk space" in text or "no space left" in text or "disk full" in text:
        causes.append("Insufficient disk space")
        category = "infrastructure"
        confidence = "high"
        impact = "Service unable to write data / downtime"
        fix = "Increase disk capacity or clean up old files"

    # Network issues
    elif "connection refused" in text or "connection timeout" in text or "network unreachable" in text:
        causes.append("Network connectivity failure")
        category = "network"
        confidence = "high"
        impact = "Service communication blocked"
        fix = "Check network configuration and connectivity"

    # Database issues
    elif "database" in text or "sql" in text or "connection pool" in text or "db error" in text:
        causes.append("Database connectivity or query failure")
        category = "database"
        confidence = "high"
        impact = "Data operations failed / service degraded"
        fix = "Check database connection string and database health"

    # CI/CD pipeline issues
    elif "pipeline" in text or "build failed" in text or "test suite failed" in text or "test failed" in text:
        causes.append("CI/CD pipeline failure due to failing tests")
        category = "ci/cd"
        confidence = "high"
        impact = "Build failed -> deployment blocked"
        fix = "Fix failing test cases or rollback code"

    # Dependency/Package issues
    elif "import error" in text or "module not found" in text or "dependency" in text or "package" in text:
        causes.append("Missing or incompatible dependency")
        category = "dependency"
        confidence = "high"
        impact = "Application startup failed"
        fix = "Install missing dependencies or update versions"

    # Authentication/Security issues
    elif "unauthorized" in text or "forbidden" in text or "jwt" in text or "authentication" in text:
        causes.append("Authentication or authorization failure")
        category = "security"
        confidence = "high"
        impact = "Access denied / service unavailable"
        fix = "Validate credentials and token configuration"

    # Permission issues
    elif "permission denied" in text or "access denied" in text:
        causes.append("Permission or access control issue")
        category = "security"
        confidence = "high"
        impact = "Operation blocked due to insufficient privileges"
        fix = "Review and adjust file/directory permissions"

    # Timeout issues
    elif "timeout" in text or "timed out" in text:
        causes.append("Operation timeout")
        category = "performance"
        confidence = "high"
        impact = "Request processing failed / slow response"
        fix = "Increase timeout values or optimize slow operations"

    # Configuration issues
    elif "config" in text or "invalid configuration" in text or "env variable" in text:
        causes.append("Configuration error")
        category = "configuration"
        confidence = "medium"
        impact = "Application startup or behavior failed"
        fix = "Review configuration files and environment variables"

    return {
        "root_cause": causes[0] if causes else "Unknown issue",
        "impact": impact,
        "confidence": confidence,
        "category": category,
        "recommended_fix": fix
    }
