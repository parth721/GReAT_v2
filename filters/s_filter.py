def is_supported_issue_type(issue_type, supported_types=None):
    if supported_types is None:
        supported_types = ["login", "payment", "technical error", "account", "reset password"]
    # Normalize
    issue_type = issue_type.lower().strip()
    return issue_type in supported_types 