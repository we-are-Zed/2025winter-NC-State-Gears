from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from litellm import completion

def get_llm_response(messages):
    response = completion(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/",
        model="gpt-4o",
        custom_llm_provider="openai",
        messages=messages
    )
    return response.choices[0].message.content

class AnalyzeLLM:
    def __init__(self):
        pass

    def _call(self, prompt: str) -> str:
        instruction = """
        You are analyzing and comparing environmental impact data related to electricity production processes. 
        The retrieval will return several results, so there may be useless information.

        Each process is represented as a document with two main parts: metadata and page content.
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
        - Identify and compare significant environmental impact categories for different processes if the user asks for comparison.
        - If the user's data is provided, compare the user's data with the data in the database and analyze the difference and accuracy.
        - Provide a concise summary highlighting the most impactful categories, units, and their corresponding values for each process.

        Remember to output the index of the processes in the database you are analyzing. Put them in the first line without any other text like this: "1,2,4"
        But if there is user's data, don't output the index I mentioned in the previous sentence, just output the analysis or comparison.
        When presenting your analysis, be clear and structured, using the environmental impact categories and metadata as the basis for your insights.
        """
        
        messages = [
            {"content": instruction, "role": "system"},
            {"content": prompt, "role": "user"}
        ]
        
        response = get_llm_response(messages)
        return response
        
    @property
    def _llm_type(self) -> str:
        return "custom"
    
class FileLLM:
    def __init__(self):
        pass

    def _call(self, prompt: str) -> str:
        instruction = """
            You are reading environmental impact data related to electricity production processes. Your task is to extract the following ten environmental impact categories from the data and output them in a specified format:
                1 Acidification (kg SO2 eq)
                2 Carcinogenics (CTUh)
                3 Ecotoxicity (CTUe)
                4 Eutrophication (kg N eq)
                5 Fossil fuel depletion (MJ surplus)
                6 Global warming (kg CO2 eq)
                7 Non carcinogenics (CTUh)
                8 Ozone depletion (kg CFC-11 eq)
                9 Respiratory effects (kg PM2.5 eq)
                10 Smog (kg O3 eq)

            You should output the data in the following format:

            1. On the first line, output the name of the process (e.g., electricity production in North America).
            2. On the second line, output the values for each of the ten environmental impacts in the following order:
                - Acidification, Carcinogenics, Ecotoxicity, Eutrophication, Fossil fuel depletion, Global warming, Non carcinogenics, Ozone depletion, Respiratory effects, Smog
                - Values should be separated by commas.
                - If any value is missing, leave the position empty (i.e., ,,).

            Example output format:
                electricity production in north america
                1.0056,3.5546,,156.556,,,,,,

            Make sure that you maintain this specific structure, with the name of the process on the first line, followed by the values on the second line in the given order.
        """
        
        messages = [
            {"content": instruction, "role": "system"},
            {"content": prompt, "role": "user"}
        ]
        
        response = get_llm_response(messages)
        return response
        
    @property
    def _llm_type(self) -> str:
        return "custom"

class PrelimLLM:
    def __init__(self):
        pass

    def _call(self, prompt: str) -> str:
        instruction = """
        You are answering questions related to electricity production processes.
        We have data about the environmental impact of the process in the database. 
        If the user asks for the irrelevant information, say you don't know even if you know.
        If you think you need data(especially when the user asks for the impact), just output "need_data" to get the data from the database.
        But if you think the user wants to compare the data, just output "need_compare" instead of "need_data".
        """
        
        messages = [
            {"content": instruction, "role": "system"},
            {"content": prompt, "role": "user"}
        ]
        
        response = get_llm_response(messages)
        return response
        
    @property
    def _llm_type(self) -> str:
        return "custom"

def retrieve_documents(query, vectorstore, k):
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
    persist_directory = "./Process_chroma_db"

    embedding_function = OpenAIEmbeddings(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/v1"
    )

    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)

    print("Initializing...")

    analyze_llm = AnalyzeLLM()
    prelim_llm = PrelimLLM()
    file_llm = FileLLM()

    print("Initialized. Input 'quit' to exit.")

    while True:
        question = input("\nQuestion: ")
        if question.lower() == 'quit':
            break

        #todo: 历史记录数据库!
        #情况1：如果有文件数据
        file_path = "./impact.xlsx"
        #记得到时候把文件名也传进去
        if file_path != "":  
            if file_path.endswith('.csv'):
                import pandas as pd
                df = pd.read_csv(file_path)
                content = df.to_string()
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                import pandas as pd
                df = pd.read_excel(file_path)
                content = df.to_string()
            elif file_path.endswith('.json'):
                import json
                content = json.dumps(json.loads(content), indent=2)
            else:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

            
            file_answer = file_llm._call(content) 
            
            documents = retrieve_documents(file_answer, vectorstore, 1)
            formatted_docs = process_documents(documents)
            prompt = f"question: {question}\n\nuser's data(the second line of data is in the sequence of the ten environmental impacts same as the data in the database):\n{file_answer}\n\nprocesses in the database:\n{formatted_docs}"
            answer = analyze_llm._call(prompt)

            metadata = documents[0].metadata
            name = documents[0].page_content.split(":")[1].split('"')[1].split('"')[0]
            values = []
            for i, (key, value) in enumerate(metadata.items()):
                if i < 10:  
                    number = float(value.split(", ")[1]) 
                    values.append(number)
            print(name, values)

            userdata_name = file_answer.split("\n")[0]
            userdata_values = file_answer.split("\n")[1]
            userdata_values_array = [float(x) for x in userdata_values.split(",")]
            #todo: 绘制对比图表
            #userdata_name和userdata_values_array是用户提供数据
            #name和values是数据库数据(只有一个process)
            #values是数组，表示10个环境影响指标的值，顺序都是写死的，参照代码67行

            print(answer) #llm的回答
            continue

        #情况2：没有文件数据
        prelim_answer = prelim_llm._call(question) # 让llm判断是否需要数据、是分析还是比较
        if prelim_answer == "need_data" or prelim_answer == "need_compare": #需要数据、比较
            documents = retrieve_documents(question, vectorstore, 5)
            formatted_docs = process_documents(documents)
            prompt = f"question: {question}\n\nprocesses in the database:\n{formatted_docs}"
            answer = analyze_llm._call(prompt)
            
            numbers = answer.split('\n')[0]
            number_array = [int(x) for x in numbers.split(',')]
            for number in number_array:
                metadata = documents[number].metadata
                name = documents[number].page_content.split(":")[1].split('"')[1].split('"')[0]
                values = []
                for i, (key, value) in enumerate(metadata.items()):
                    if i < 10:  
                        number = float(value.split(", ")[1]) 
                        values.append(number)
                print(name, values)
            #todo: 绘制对比、分析图表，注意有多个process
            #if prelim_answer == "need_compare": ...... 
            


            answer = '\n'.join(answer.split('\n')[1:]).strip()
            print("\nAnswer:", answer)
        else:
            #不需要数据，直接回答
            print("\nAnswer:", prelim_answer)

if __name__ == "__main__":
    main()
