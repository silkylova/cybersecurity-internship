"""
Day 11: Social Engineering Awareness Training Module
Interactive CLI Quiz Engine
"""
import json

QUESTIONS = [
    {
        "q": "An email asks you to verify your password via a link. You should:",
        "opts": ["A) Click the link", "B) Call IT directly", "C) Reply with password"],
        "ans": "B",
        "exp": "Always verify via official channels, never click email links."
    },
    {
        "q": "You find a USB drive in the parking lot. You should:",
        "opts": ["A) Plug it in to check", "B) Hand to security", "C) Keep it"],
        "ans": "B",
        "exp": "USB drops are a classic baiting attack vector."
    },
    {
        "q": "A recruiter connects on LinkedIn. They have 0 posts and no profile picture. This is likely:",
        "opts": ["A) A networking opportunity", "B) A new user", "C) A fake profile for reconnaissance"],
        "ans": "C",
        "exp": "Accounts missing profile photos with zero posts are classic indicators of automated fake profiles used for social engineering."
    },
    {
        "q": "You visit a trusted industry news site, but your browser blocks a hidden background script. This is likely:",
        "opts": ["A) A watering hole attack", "B) A phishing email", "C) Tailgating"],
        "ans": "A",
        "exp": "Watering hole attacks compromise trusted sites to deliver drive-by downloads via hidden scripts or pixels."
    }
]


def run_quiz():
    print("=== Social Engineering Awareness Training ===")
    print("Please answer A, B, or C for the following scenarios.\n")

    score = 0
    results_log = []

    for i, q in enumerate(QUESTIONS, 1):
        print(f"Q{i}: {q['q']}")
        for o in q['opts']:
            print(f"  {o}")

        # Input validation loop
        while True:
            ans = input("Your answer (A/B/C): ").strip().upper()
            if ans in ['A', 'B', 'C']:
                break
            print("Invalid input. Please enter A, B, or C.")

        is_correct = (ans == q['ans'])
        if is_correct:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong. The correct answer was {q['ans']}.")
            print(f"   Reason: {q['exp']}")

        # Track the data for JSON logging
        results_log.append({
            "question": q['q'],
            "user_answer": ans,
            "correct": is_correct
        })
        print("-" * 50)

    print(f"\nFinal Score: {score}/{len(QUESTIONS)}")

    # Save the session to a JSON file
    report_data = {
        "final_score": score,
        "total_questions": len(QUESTIONS),
        "details": results_log
    }

    with open("quiz_results.json", "w") as f:
        json.dump(report_data, f, indent=4)

    print("Quiz complete. Results saved to 'quiz_results.json'.")


if __name__ == "__main__":
    run_quiz()