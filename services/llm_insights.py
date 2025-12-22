import json
import os
from openai import OpenAI
from services.openai_client import client


def build_prompt(profile: dict) -> str:
    column_summary = profile.get("column_summary", {})
    numeric_stats = profile.get("numeric_stats", {})
    missing_values = profile.get("missing_values", {})
    outliers = profile.get("outliers", {})

    prompt = f"""
You are a senior data analyst.

Based on the provided dataset profile and summary statistics, generate:

1. Exactly 10 concise, business-oriented insights describing sales behavior,
   profitability, variability, risks, and analytical opportunities.
2. A conclusion and next steps section including:
   - Summary of Insights
   - Data Preparation / Cleaning Plan
   - Proposed Modeling Approach

Dataset Profile:
- Rows: {profile.get("rows")}
- Columns: {profile.get("columns")}
- Numeric columns: {len(column_summary.get("numeric", []))}
- Categorical columns: {len(column_summary.get("categorical", []))}
- Datetime columns: {len(column_summary.get("datetime", []))}
- Text columns: {len(column_summary.get("text", []))}
- Total missing values: {sum(missing_values.values()) if missing_values else 0}
- Columns with missing columns: {len(missing_values)}
- Columns with outliers: {len(outliers)}

Key Numeric Ranges:
{json.dumps(numeric_stats, indent=2)}

Important rules:
- Do NOT assume specific countries, products, or categories.
- Phrase insights conditionally when group-wise data is unavailable.
- Do NOT invent values or rankings.
- Keep insights generalizable to any dataset.
- Use professional, non-technical language.

Return ONLY valid JSON in this format:
{{
  "insights": ["...", "... (exactly 10 items)"],
  "conclusion": {{
    "summary": "...",
    "data_preparation": ["...", "..."],
    "modeling": ["...", "..."]
  }}
}}
"""
    return prompt


def generate_llm_insights(profile: dict) -> dict:
    prompt = build_prompt(profile)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # fast + cheap + good
        messages=[
            {"role": "system", "content": "You are a senior data analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        return {
            "error": "Invalid LLM response",
            "raw": content
        }
