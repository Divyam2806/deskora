import regex as re, json
import regex, json

def extract_json(text: str) -> dict:
    """Extract and parse the first valid JSON block with 'reply' and 'actions' keys."""
    matches = re.findall(r"\{(?:[^{}]|(?R))*\}", text, re.DOTALL)

    for candidate in matches:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict) and "reply" in parsed and "actions" in parsed:
                return parsed
        except json.JSONDecodeError:
            continue

    return {"reply": "Sorry, I didn't quite understand that.", "actions": []}



output = """
 {
  "reply": "Sure Divyam! Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources. It allows you to access your data and applications from anywhere, as long as you have an internet connection.",
  "actions": [
    { "type": "store", "key": "cloud_definition", "value": "Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources."},
    { "type": "run", "skill": "open_browser"},
    { "type": "store", "key": "cloud_benefits", "value": "Benefits of cloud computing include scalability, flexibility, cost-effectiveness, and accessibility."},
    { "type": "run", "skill": "open_browser"}
  ]
}
"""

parsed = extract_json(output)
print(parsed)


#