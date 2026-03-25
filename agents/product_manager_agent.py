from core.llm import get_llm

llm = get_llm()


def create_product_spec(prompt):

    pm_prompt = f"""
You are a product manager.

Convert the user request into a clear product specification.

User request:
{prompt}

Include:
- features
- API endpoints
- frontend pages
- database needs
"""

    spec = llm.invoke(pm_prompt)

    return {
    "plan": spec
    }