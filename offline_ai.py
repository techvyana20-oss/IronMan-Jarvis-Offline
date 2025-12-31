import json
import os
import time
import sys

BRAIN_FILE = "brain.json"

# ======================
# LOADING ANIMATION
# ======================
def loading(text="Loading"):
    for i in range(3):
        print(f"{text}{'.' * (i+1)}", end="\r")
        time.sleep(0.5)
    print(" " * 20, end="\r")

# ======================
# LOAD / SAVE BRAIN
# ======================
def load_brain():
    if not os.path.exists(BRAIN_FILE):
        return {}
    with open(BRAIN_FILE, "r") as f:
        return json.load(f)

def save_brain(brain):
    with open(BRAIN_FILE, "w") as f:
        json.dump(brain, f, indent=4)

brain = load_brain()

# ======================
# AI CORE LOGIC
# ======================
def analyze(question):
    words = question.lower().split()
    best_match = None
    highest_score = 0

    for key, data in brain.items():
        score = sum(1 for w in words if w in data["keywords"])
        if score > highest_score:
            highest_score = score
            best_match = key

    return best_match, highest_score

def confidence(score):
    if score >= 4:
        return "Very High"
    elif score >= 2:
        return "Medium"
    elif score == 1:
        return "Low"
    return "Unknown"

# ======================
# AUTO SUGGESTION
# ======================
def suggest():
    if not brain:
        return None
    return list(brain.keys())[0]

# ======================
# TEACH AI
# ======================
def teach():
    print("\n🧠 Teach Mode")
    category = input("Category: ").strip()
    keywords = input("Keywords (comma separated): ").lower().split(",")
    answer = input("Answer: ").strip()

    brain[category] = {
        "keywords": [k.strip() for k in keywords],
        "answer": answer
    }

    save_brain(brain)
    print("✅ AI learned & saved permanently\n")

# ======================
# ASK AI
# ======================
def ask():
    q = input("\nYou: ").strip()
    match, score = analyze(q)

    if match:
        print(f"\n🤖 AI: {brain[match]['answer']}")
        print(f"📊 Confidence: {confidence(score)}\n")
    else:
        print("\n🤖 AI: I don't know this yet.")
        s = suggest()
        if s:
            print(f"💡 Try asking about: {s}")
        ch = input("Teach me now? (y/n): ").lower()
        if ch == "y":
            teach()

# ======================
# MENU UI
# ======================
def menu():
    while True:
        print("""
╔════════════════════════════╗
║   🤖 OFFLINE AI ASSISTANT  ║
╠════════════════════════════╣
║ 1️⃣ Ask AI                 ║
║ 2️⃣ Teach AI               ║
║ 3️⃣ Brain Stats            ║
║ 4️⃣ Exit                   ║
╚════════════════════════════╝
""")
        choice = input("Select: ")

        if choice == "1":
            ask()
        elif choice == "2":
            teach()
        elif choice == "3":
            print(f"\n🧠 Total Knowledge Units: {len(brain)}\n")
        elif choice == "4":
            print("\n👋 AI shutting down (memory saved forever)")
            sys.exit()
        else:
            print("❌ Invalid option")

# ======================
# START
# ======================
loading("Starting Offline AI")
print("✅ Memory loaded:", len(brain), "topics\n")
menu()
