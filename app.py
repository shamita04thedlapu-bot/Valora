import streamlit as st
from ai_analyzer import analyze_content

# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="Valora",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- HEADER ----------------

st.title("🛡️ Valora")
st.subheader("AI Brand Governance Platform")

st.write(
    "Review your content before publication for "
    "brand consistency, accuracy and accessibility."
)

st.divider()

# ---------------- CONTENT INPUT ----------------

content = st.text_area(
    "Paste your content here",
    height=250,
    placeholder="Enter the content you want Valora to review..."
)

# ---------------- ANALYZE ----------------

if st.button("🔍 Analyze Content"):

    if content.strip():

        with open("data/brand_guidelines.txt", "r", 
    encoding="utf-8") as file:
         guidelines = file.read()

    result = analyze_content(content, guidelines)

    st.divider()

    st.header("📊 Valora Review Report")

        # ---------------- SCORE ----------------

    score = result["score"]

    if score >= 80:
            st.success(
                f"🟢 Brand Compliance Score: {score}/100"
            )
    elif score >= 50:
            st.warning(
                f"🟡 Brand Compliance Score: {score}/100"
            )
    else:
            st.error(
                f"🔴 Brand Compliance Score: {score}/100"
            )

        # ---------------- PASSED CHECKS ----------------

    st.subheader("✅ Passed Checks")

    if result["passed"]:

            for item in result["passed"]:
                st.write("✓", item)

    else:
            st.write("No checks passed.")

        # ---------------- ISSUES ----------------

    st.subheader("⚠️ Issues Found")

    if result["issues"]:

            for issue in result["issues"]:

                if issue["severity"] == "High":

                    st.error(
                        f"**{issue['category']}** — "
                        f"{issue['message']}"
                    )

                else:

                    st.warning(
                        f"**{issue['category']}** — "
                        f"{issue['message']}"
                    )

                st.caption(
                    f"Detected: {issue['evidence']}"
                )

    else:

            st.success(
                "No major issues detected."
            )

        # ---------------- SUGGESTIONS ----------------

    st.subheader("💡 Suggested Improvements")

    if result["suggestions"]:

            for suggestion in result["suggestions"]:
                st.info(suggestion)

    else:

            st.success(
                "No suggestions needed."
            )

else:

        st.warning(
            "Please enter some content first."
        )