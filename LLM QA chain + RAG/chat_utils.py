from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from litellm import completion

def get_llm_response(messages):
    response = completion(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/",
        model="gpt-o1",
        custom_llm_provider="openai",
        messages=messages
    )
    return response.choices[0].message.content

class AnalyzeLLM:
    def __init__(self):
        pass

    def _call(self, prompt: str, history=None) -> str:
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
            {"content": history, "role": "system"},
            {"content": prompt, "role": "user"}
        ]
        
        return get_llm_response(messages)
        
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
        
        return get_llm_response(messages)
        
    @property
    def _llm_type(self) -> str:
        return "custom"

class PrelimLLM:
    def __init__(self):
        pass

    def _call(self, prompt: str, history=None) -> str:
        instruction = """
        You are answering questions related to electricity production processes.
        We have data about the environmental impact of the process in the database. 
        If the user asks for the irrelevant information, say you don't know even if you know.
        If you think you need data(especially when the user asks for the impact), just output "need_data" to get the data from the database.
        But if you think the user wants to compare the data, just output "need_compare" instead of "need_data".
        """
        
        messages = [
            {"content": instruction, "role": "system"},
            {"content": history, "role": "system"},
            {"content": prompt, "role": "user"}
        ]
        
        return get_llm_response(messages)
        
    @property
    def _llm_type(self) -> str:
        return "custom"
    
class Chroma:
    persist_directory = "./Process_chroma_db"

    embedding_function = OpenAIEmbeddings(
        api_key="sk-DItn6zcaiTeKjRdNulAWsg",
        base_url="http://18.216.253.243:4000/v1"
    )
    def __init__(self):
        self.vectorstore = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding_function)
    
    def retrieve_documents(self, query, k):
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
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

analyze_llm = AnalyzeLLM()
prelim_llm = PrelimLLM()
file_llm = FileLLM()
rag = Chroma()
