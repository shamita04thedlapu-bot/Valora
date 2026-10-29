
import re


def analyze_content(content, guidelines):
    issues = []
    suggestions = []
    passed = []
    failed_checks = 0
    total_checks = 0

    text = content.lower()
    guideline_text = guidelines.lower()

    def record_check(category, failed, message, evidence, suggestion, success):
        """Record a check and update the score only once per check."""
        nonlocal failed_checks, total_checks

        total_checks += 1

        if failed:
            failed_checks += 1
            issues.append({
                "category": category,
                "severity": "Warning",
                "message": message,
                "evidence": evidence
            })
            suggestions.append(suggestion)
        else:
            passed.append(success)

    def extract_terms(labels):
        """Read comma-separated terms from explicitly labelled guideline lines."""
        terms = []

        for line in guidelines.splitlines():
            line = line.strip()

            for label in labels:
                pattern = rf"^\s*{re.escape(label)}\s*:\s*(.+)$"
                match = re.match(pattern, line, re.IGNORECASE)

                if match:
                    values = re.split(r"[,;]", match.group(1))
                    terms.extend(
                        item.strip().strip("\"'").lower()
                        for item in values
                        if item.strip()
                    )
                    break

        return list(dict.fromkeys(terms))

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
        if re.search(
            rf"\b{re.escape(word)}\b",
            text
        )
    ]

    record_check(
        "Tone",
        bool(found_informal),
        "Informal language detected.",
        ", ".join(found_informal),
        "Replace casual expressions with professional and friendly language.",
        "Professional tone"
    )

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

    record_check(
        "Claims",
        bool(found_claims),
        "Potentially unsupported claim detected.",
        ", ".join(found_claims),
        "Verify the claim with reliable evidence or use more precise wording.",
        "No obvious unsupported claims"
    )

    # ---------------- TERMINOLOGY CHECK ----------------

    preferred_customer = (
        "customer" in guideline_text
        and re.search(r"\buser\b", text)
    )

    record_check(
        "Terminology",
        bool(preferred_customer),
        "The word 'user' may not match the preferred brand terminology.",
        "user" if preferred_customer else "",
        "Consider replacing 'user' with 'customer' according to the brand guidelines.",
        "Preferred terminology"
    )

    # ---------------- ACCESSIBILITY CHECK ----------------

    sentences = re.split(r"[.!?]+", content)

    long_sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) > 30
    ]

    record_check(
        "Accessibility",
        bool(long_sentences),
        "A very long sentence may be difficult to read.",
        long_sentences[0][:150] if long_sentences else "",
        "Break long sentences into shorter and clearer sentences.",
        "Readable sentence structure"
    )

    # ---------------- CAPITALIZATION CHECK ----------------

    has_letters = any(char.isalpha() for char in content)
    all_uppercase = has_letters and content.upper() == content

    record_check(
        "Accessibility",
        all_uppercase,
        "The content is written entirely in uppercase.",
        content[:100] if all_uppercase else "",
        "Use normal capitalization to improve readability.",
        "Normal capitalization"
    )

    # ---------------- BANNED TERMS CHECK ----------------

    default_banned_terms = [
        "cheap",
        "guaranteed results",
        "best in the world"
    ]

    configured_banned_terms = extract_terms([
        "Banned words",
        "Banned phrases",
        "Prohibited terms",
        "Avoid"
    ])

    banned_terms = list(dict.fromkeys(
        default_banned_terms + configured_banned_terms
    ))

    found_banned = [
        term for term in banned_terms
        if re.search(rf"\b{re.escape(term)}\b", text)
    ]

    record_check(
        "Brand Governance",
        bool(found_banned),
        "Banned or discouraged brand wording detected.",
        ", ".join(found_banned),
        "Replace the flagged wording with an approved brand-safe alternative.",
        "No banned terms detected"
    )

    # ---------------- REQUIRED TERMS CHECK ----------------

    required_terms = extract_terms([
        "Required terms",
        "Required words",
        "Must include"
    ])

    if required_terms:
        missing_terms = [
            term for term in required_terms
            if not re.search(rf"\b{re.escape(term)}\b", text)
        ]

        record_check(
            "Brand Governance",
            bool(missing_terms),
            "Required brand terminology is missing.",
            ", ".join(missing_terms),
            "Include the missing required terms where they fit naturally.",
            "Required brand terminology included"
        )

    # ---------------- SCORE ----------------

    score = round(
        ((total_checks - failed_checks) / total_checks) * 100
    ) if total_checks else 100

    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "passed": passed
    }


