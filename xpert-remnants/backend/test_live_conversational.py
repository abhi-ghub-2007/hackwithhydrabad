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
    # 1. Test "Are you mad?"
    r_mad = ask("Are you mad?")
    print("=== EMOTIONAL SMALL TALK ===")
    print("Query: Are you mad?")
    print("Answer:", r_mad.get("answer"))
    print("Sources:", r_mad.get("sources"))

    # 2. Test "What database is used?"
    r_db = ask("What database is used?")
    print("\n=== SIMPLE FACT QUERY ===")
    print("Query: What database is used?")
    print("Answer:", r_db.get("answer"))
    print("Sources:", r_db.get("sources"))

    # 3. Multi-turn follow-up
    cid = str(uuid.uuid4())
    print("\n=== MULTI-TURN FOLLOW-UP ===")
    f1 = ask("Which database should we use for Project X?", cid)
    print("Turn 1 (Which database should we use for Project X?):")
    print("Answer:", f1.get("answer")[:200] + "...")

    f2 = ask("Why?", cid)
    print("\nTurn 2 (Why?):")
    print("Answer:", f2.get("answer"))
    print("Intent:", f2.get("intent"))

    f3 = ask("What about Supabase?", cid)
    print("\nTurn 3 (What about Supabase?):")
    print("Answer:", f3.get("answer"))
    print("Intent:", f3.get("intent"))
