import urllib.request
import json
import uuid
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_url = "http://127.0.0.1:8000/api/ask"

def ask(query, conv_id=None):
    payload = {"query": query}
    if conv_id:
        payload["conversation_id"] = conv_id
    req = urllib.request.Request(
        base_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

if __name__ == "__main__":
    # 1. Test Greeting
    r_greet = ask("Hello")
    print("=== GREETING RESPONSE ===")
    print("Intent:", r_greet.get("intent"))
    print("Answer:", r_greet.get("answer"))
    print("Sources:", r_greet.get("sources"))

    # 2. Test General Knowledge
    r_gk = ask("What is PostgreSQL?")
    print("\n=== GENERAL KNOWLEDGE RESPONSE ===")
    print("Intent:", r_gk.get("intent"))
    print("Source Classification:", r_gk.get("source_classification"))
    print("Answer:\n", r_gk.get("answer"))

    # 3. Test 7-Step Scenario
    cid = str(uuid.uuid4())
    print("\n=== STEP 1: Query Project X Database ===")
    s1 = ask("Which database should we use for Project X?", cid)
    print("Answer:\n", s1.get("answer"))

    print("\n=== STEP 3: Propose Change ===")
    s3 = ask("No. For the current project we're choosing Supabase because it gives us faster delivery and the team already has experience with it.", cid)
    print("Answer:\n", s3.get("answer"))

    print("\n=== STEP 5: Confirm Change ===")
    s5 = ask("Yes, please record it.", cid)
    print("Answer:\n", s5.get("answer"))

    print("\n=== STEP 7: Query Project X Database Again ===")
    s7 = ask("Which database should we use for Project X?", cid)
    print("Answer:\n", s7.get("answer"))
    print("Sources:", s7.get("sources"))
