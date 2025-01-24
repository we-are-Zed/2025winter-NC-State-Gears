from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from litellm import completion
from typing import List, Optional
import os

def get_llm_response(messages):
    response = completion(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/",
        model="gpt-4o",
        custom_llm_provider="openai",
        messages=messages
    )
    return response.choices[0].message.content

class CustomLLM:
    def __init__(self):
        pass

    def _call(self, prompt: str, **kwargs: Optional[dict]) -> str:
        instruction = """
        You are analyzing environmental impact data related to electricity production processes. Each process is represented as a document with two main parts: metadata and page content.

        1. Metadata:
           - The first 10 keys represent different environmental impact categories, with values as strings containing both the unit and the numeric result (e.g., "kg CO2 eq, 0.018136444283705113").
           - The last two keys are:
             - "amount": The amount of the product (e.g., "1.0 kWh").
             - "date": The timestamp of the data (e.g., "2025-01-20 23:16:05").

        2. Page Content:
           - Contains basic information about the production process, including:
             - "product_system": The name and type of the system.
             - "location": The geographic location of the process.
             - "product": The output product.

        Your primary objective is to:
        - Analyze the environmental impact data from the metadata.
        - Identify and compare significant environmental impact categories for different processes.
        - Provide a concise summary highlighting the most impactful categories, units, and their corresponding values for each process.

        If the user asks for the irrelevant information, say you don't know even if you know.
        The retrieval will return 2 results, so there may be useless information.
        When presenting your analysis, be clear and structured, using the environmental impact categories and metadata as the basis for your insights.
        """
        
        messages = [
            {"content": instruction, "role": "system"},
            {"content": prompt, "role": "user"}
        ]
        
        # 调用LLM API
        response = get_llm_response(messages)
        return response
        
    @property
    def _llm_type(self) -> str:
        return "custom"

def retrieve_documents(query, vectorstore, k=2):
    """从 Chroma 向量存储中检索相关文档"""
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    result = retriever.invoke(query)
    return result

def process_documents(documents):
    formatted_docs = []
    for doc in documents:
        metadata = doc.metadata
        content = doc.page_content
        formatted_doc = f"Metadata: {metadata}\nContent: {content}"
        formatted_docs.append(formatted_doc)
    return "\n\n".join(formatted_docs)

def main():
    """启动交互式问答系统"""
    persist_directory = "./Process_chroma_db"

    # 使用 OpenAI 的嵌入模型
    embedding_function = OpenAIEmbeddings(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/v1"
    )

    # 初始化向量存储
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)

    print("初始化问答系统...")

    # 初始化自定义 LLM
    llm = CustomLLM()

    print("系统已准备就绪！请输入您的问题（输入 'quit' 退出）")

    while True:
        question = input("\n问题: ")
        if question.lower() == 'quit':
            break

        documents = retrieve_documents(question, vectorstore)
        formatted_docs = process_documents(documents)
        prompt = f"question: {question}\n\ninformation from the database:\n{formatted_docs}"

        answer = llm._call(prompt)
        print("\n回答:", answer)

if __name__ == "__main__":
    main()
