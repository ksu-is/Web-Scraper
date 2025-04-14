from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following HTML content:\n\n{dom_content}\n\n"
    "Your goal is to return data that directly matches this description:\n\n{parse_description}\n\n"
    "Instructions:\n"
    "1. Return only the relevant extracted data.\n"
    "2. If the data fits a structured format (like a table), output it using pipe symbols (`|`) between columns and newlines between rows.\n"
    "3. If not structured (e.g., bios, article summaries), output the relevant text cleanly and concisely.\n"
    "4. Never include extra explanations or introductory text.\n"
    "5. If no matching information is found, return an empty string ('')."
)

model = OllamaLLM(model="llama3")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
