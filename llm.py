import ollama
import json

def extract_contract_data(contract_text):

    prompt = f"""
    You are a legal expert.

    Extract the following details from the contract.
    If not found, return "Not found".

    Return ONLY valid JSON in this format:

    {{
        "party_1": "",
        "party_2": "",
        "start_date": "",
        "end_date": "",
        "payment_terms": "",
        "risk_level": "Low/Medium/High"
    }}

    Contract:
    {contract_text}
    """

    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response['message']['content']

    try:
        json_start = output.find("{")
        json_end = output.rfind("}") + 1
        json_str = output[json_start:json_end]
        data = json.loads(json_str)
        return data
    except:
        return None