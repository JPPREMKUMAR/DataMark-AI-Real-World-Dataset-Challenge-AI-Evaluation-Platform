def execute_python_submission(code, sandbox_config=None):
    if not isinstance(code,str) or not code.strip(): return {"status":"rejected","reason":"empty submission"}
    return {"status":"not_executed","reason":"No isolated sandbox configured; untrusted code was not executed."}
