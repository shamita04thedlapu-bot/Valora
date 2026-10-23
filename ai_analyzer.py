import re


def analyze_content(content, guidelines):

    issues = []
    suggestions = []
    passed = []

    text = content.lower()
    guideline_text = guidelines.lower()

    # ---------------- TONE CHECK ----------------

    informal_words = [
        "gonna",
        "wanna",
        "lol",
        "hey guys",
        "stuff"
    ]

    found_informal = [
        word for word in informal_words
        if word in text
    ]

    if found_informal:
        issues.append({
            "category": "Tone",
            "severity": "Warning",
            "message": "Informal language detected.",
            "evidence": ", ".join(found_informal)
        })

        suggestions.append(
            "Replace casual expressions with professional and friendly language."
        )
    else:
        passed.append("Professional tone")

    # ---------------- CLAIM CHECK ----------------

    risky_claims = [
        "best in the world",
        "100% guaranteed",
        "number one",
        "guaranteed results",
        "works for everyone",
        "no risk"
    ]

    found_claims = [
        phrase for phrase in risky_claims
        if phrase in text
    ]

    if found_claims:
        issues.append({
            "category": "Claims",
            "severity": "High",
            "message": "Potentially unsupported claim detected.",
            "evidence": ", ".join(found_claims)
        })

        suggestions.append(
            "Verify the claim with reliable evidence or use more precise wording."
        )
    else:
        passed.append("No obvious unsupported claims")

    # ---------------- TERMINOLOGY CHECK ----------------

    if "user" in text and "customer" in guideline_text:
        issues.append({
            "category": "Terminology",
            "severity": "Warning",
            "message": "The word 'user' does not match the preferred terminology.",
            "evidence": "user"
        })

        suggestions.append(
            "Consider replacing 'user' with 'customer' according to the brand guidelines."
        )
    else:
        passed.append("Preferred terminology")

    # ---------------- ACCESSIBILITY CHECK ----------------

    sentences = re.split(r"[.!?]+", content)

    long_sentences = [
        sentence
        for sentence in sentences
        if len(sentence.split()) > 30
    ]

    if long_sentences:
        issues.append({
            "category": "Accessibility",
            "severity": "Warning",
            "message": "A very long sentence may be difficult to read.",
            "evidence": long_sentences[0][:150]
        })

        suggestions.append(
            "Break long sentences into shorter and clearer sentences."
        )
    else:
        passed.append("Readable sentence structure")

    # ---------------- UPPERCASE CHECK ----------------

    if content.isupper() and len(content.strip()) > 10:

        issues.append({
            "category": "Accessibility",
            "severity": "Warning",
            "message": "The content is written entirely in uppercase.",
            "evidence": content[:100]
        })

        suggestions.append(
            "Use normal capitalization to improve readability."
        )
    else:
        passed.append("Normal capitalization")

    # ---------------- SCORE ----------------

    total_checks = 5
    failed_checks = min(len(issues), total_checks)

    score = round(
        ((total_checks - failed_checks) / total_checks) * 100
    )

    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "passed": passed
    }