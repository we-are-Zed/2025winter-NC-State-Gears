from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from litellm import completion
from langchain_openai import OpenAIEmbeddings
import os
from langchain_core.language_models import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, List, Optional

def get_llm_response(messages):
    response = completion(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/",
        model="gpt-4o",
        custom_llm_provider="openai",
        messages=messages
    )
    return response.choices[0].message.content

class CustomLLM(LLM):
    def __init__(self):
        super().__init__()
        
    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
        messages = [{"content": prompt, "role": "user"}]
        response = get_llm_response(messages)
        return response
        
    @property
    def _llm_type(self) -> str:
        return "custom"

    @property
    def _identifying_params(self) -> dict:
        return {}

def create_rag_database(file_path):
    # 加载文本文件，指定编码为utf-8
    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()
    
    # 将文档分割成小块
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )
    splits = text_splitter.split_documents(documents)
    
    # 创建向量存储
    embeddings = OpenAIEmbeddings(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/v1"
    )
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    return vectorstore

def create_qa_chain(vectorstore):
    # 使用自定义LLM
    llm = CustomLLM()
    
    # 创建问答链
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    return qa_chain

def main():
    # 指定txt文件路径
    file_path = "1.txt"
    
    print("正在创建RAG数据库...")
    vectorstore = create_rag_database(file_path)
    
    print("初始化问答系统...")
    qa_chain = create_qa_chain(vectorstore)
    
    chat_history = []
    print("系统已准备就绪！请输入您的问题（输入'quit'退出）")
    
    while True:
        question = input("\n问题: ")
        if question.lower() == 'quit':
            break
            
        # 获取回答
        result = qa_chain({"question": question, "chat_history": chat_history})
        answer = result["answer"]
        
        print("\n回答:", answer)
        
        # 更新对话历史
        chat_history.append((question, answer))

if __name__ == "__main__":
    main()