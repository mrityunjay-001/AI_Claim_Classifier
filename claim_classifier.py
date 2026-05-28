import json
from llm import ask
import time
import sys

ALLOWED_CLAIM_TYPES = [
    "motor",
    "property",
    "liability",
    "health"
]

ALLOWED_SEVERITY = [
    "low",
    "medium",
    "high"
]

claims = [
    "Customer car hit another vehicle in traffic.",
    "House roof damaged during heavy storm.",
    "Customer slipped in mall and filed lawsuit.",
    "Medical expenses claimed after surgery.",
    "Motorcycle stolen from parking area.",
    "Office building caught fire.",
    "Truck crashed into divider.",
    "Water leakage damaged apartment walls.",
    "Restaurant customer claimed food poisoning.",
    "Hospitalization after road accident.",
    "Broken windshield due to hailstorm.",
    "Warehouse damaged due to flood.",
    "Dog bite injury claim against homeowner.",
    "Customer fractured arm while playing football.",
    "Car engine damaged after accident.",
    "Unknown financial issue happened suddenly.",
    "Something damaged property but details unclear.",
    "A complaint was filed without exact issue."
]


def classify_claim(claim_text):

    prompt = f"""
    Classify this insurance claim.

    Return ONLY raw JSON.
    No explanation.
    No markdown.

    Format:

    {{
      "claim_text": "...",
      "claim_type": "motor/property/liability/health",
      "severity": "low/medium/high",
      "estimated_loss": number
    }}

    Claim:
    {claim_text}
    """

    messages = [
        {
            "role": "system",
            "content": "You are an insurance claim classifier."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Use ask() from llm.py
    response = ask(
        messages=messages,
        temperature=0
    )

    # Extract content
    content = response.choices[0].message.content

    # Clean markdown if present
    content = content.strip()
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    print(content)

    return json.loads(content)

# Validation Function

def validate_record(record):

    required_fields = [
        "claim_text",
        "claim_type",
        "severity",
        "estimated_loss"
    ]

    # Required fields check
    for field in required_fields:
        if field not in record:
            return False, f"Missing field: {field}"

    # Enum validation
    if record["claim_type"] not in ALLOWED_CLAIM_TYPES:
        return False, "Invalid claim_type"

    if record["severity"] not in ALLOWED_SEVERITY:
        return False, "Invalid severity"

    # Numeric validation
    if not isinstance(record["estimated_loss"], (int, float)):
        return False, "estimated_loss must be numeric"

    if not (100 <= record["estimated_loss"] <= 100000):
        return False, "estimated_loss out of allowed range"

    return True, "Valid"

valid_records = []
error_records = []

for claim in claims:

    try:
        result = classify_claim(claim)

        is_valid, reason = validate_record(result)

        if is_valid:
            valid_records.append(result)

        else:
            error_records.append({
                "claim": claim,
                "error": reason,
                "output": result
            })

    except Exception as e:

        error_records.append({
            "claim": claim,
            "error": str(e)
        })

    # delay after every request
    time.sleep(12)


with open("valid_records.json", "w") as f:
    json.dump(valid_records, f, indent=4)

with open("errors.json", "w") as f:
    json.dump(error_records, f, indent=4)

print("Done")
print("Valid Records:", len(valid_records))
print("Errors:", len(error_records))

sys.exit(0)