import os
from functools import lru_cache
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate

# Template for our RAG prompt
MEDICAL_RAG_TEMPLATE = """You are a medical assistant powered by BioMistral 7B, a specialized model for medical information.
Use the following context to answer the question. If you don't know the answer or the context doesn't provide the necessary information,
say "I don't have enough information to answer this question accurately" instead of making up an answer.

Context:
{context}

Question: {question}

Answer:"""


@lru_cache(maxsize=1)
def get_llm_model():
    """
    Load and return the LLM model using the model path from environment variables.
    Uses LRU cache to prevent reloading the model on each call.
    
    Returns:
        LlamaCpp: The loaded LLM model
    """
    model_path = os.getenv("MODEL_PATH", "/models/biomistral-7b-q4.gguf")
    context_window_size = int(os.getenv("CONTEXT_WINDOW_SIZE", "4096"))
    max_new_tokens = int(os.getenv("MAX_NEW_TOKENS", "512"))
    temperature = float(os.getenv("TEMPERATURE", "0.1"))
    
    # Load the model with specific parameters for medical Q&A
    return LlamaCpp(
        model_path=model_path,
        temperature=temperature,
        max_tokens=max_new_tokens,
        n_ctx=context_window_size,
        n_gpu_layers=-1,  # Auto-detect number of layers to offload to GPU
        n_batch=512,  # Batch size for prompt processing
        verbose=False,  # Set to True for debugging
    )


async def generate_response(query: str, context_documents: list[str]) -> str:
    """
    Generate a response to the query using the provided context documents.
    
    Args:
        query (str): The user's question
        context_documents (list[str]): List of context documents to use for answering
        
    Returns:
        str: The generated response
    """
    # Join context documents into a single string
    context = "\n\n".join(context_documents)
    
    # Create the prompt
    prompt_template = PromptTemplate.from_template(MEDICAL_RAG_TEMPLATE)
    prompt = prompt_template.format(context=context, question=query)
    
    # Get the LLM model
    model = get_llm_model()
    
    # Generate and return the response
    return model(prompt)
