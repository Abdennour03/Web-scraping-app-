from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template for extracting information from DOM content
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)
# Initialize the Ollama language model with the specified model gemma3:1b

model = OllamaLLM(model="gemma3:1b")
def parse_with_ollama(dom_chunks, parse_description):
    """
    Uses the Ollama LLM to parse DOM content chunks according to the given description.
    Returns the concatenated results from all chunks.
    """

    prompt = ChatPromptTemplate.from_template(template)  # Create a prompt from the template
    chain = prompt | model  # Combine the prompt and model into a chain

    parsed_result = []
    for i, chunk in enumerate(dom_chunks, start=1):
        # Invoke the chain with the current chunk and parsing description
        response = chain.invoke(
            {"dom_content":chunk, "parse_description": parse_description}
        )
        print(f"parsed batch {i} {len(dom_chunks)}")
        parsed_result.append(response)
    return "\n".join(parsed_result) # Return all results as a single string

