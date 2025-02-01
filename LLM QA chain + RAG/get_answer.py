from chat_utils import analyze_llm, prelim_llm, file_llm, rag
import json

def get_answer(history, prompt):
    prelim_answer = prelim_llm._call(prompt, history) 
    if prelim_answer == "need_data" or prelim_answer == "need_compare": 
        documents = rag.retrieve_documents(prompt, 5)
        formatted_docs = rag.process_documents(documents)
        new_prompt = f"question: {prompt}\n\nprocesses in the database:\n{formatted_docs}"
        answer = analyze_llm._call(new_prompt, history)
            
        numbers = answer.split('\n')[0]
        number_array = [int(x) for x in numbers.split(',')]
        result_list = [] 
        for number in number_array:
            metadata = documents[number].metadata
            name = documents[number].page_content.split(":")[1].split('"')[1].split('"')[0]
            values = []
            for i, (key, value) in enumerate(metadata.items()):
                if i < 10:  
                    number = float(value.split(", ")[1]) 
                    values.append(number)

            result_list.append({"name": name, "values": values})

        answer = '\n'.join(answer.split('\n')[1:]).strip()
        
        if prelim_answer == "need_compare":
            flag = 1
        else:
            flag = 0

        return answer, json.dumps(result_list), flag
            
    else:
        return answer, [], -1

def get_answer_with_file(history, prompt, file):
    file_answer = file_llm._call(file) 
            
    documents = rag.retrieve_documents(file_answer, 1) 
    formatted_docs = rag.process_documents(documents)
    prompt = f"question: {prompt}\n\nuser's data(the second line of data is in the sequence of the ten environmental impacts same as the data in the database):\n{file_answer}\n\nprocesses in the database:\n{formatted_docs}"
    answer = analyze_llm._call(prompt, history)

    metadata = documents[0].metadata
    name = documents[0].page_content.split(":")[1].split('"')[1].split('"')[0]
    values = []
    for i, (key, value) in enumerate(metadata.items()):
        if i < 10:  
            number = float(value.split(", ")[1]) 
            values.append(number)
    
    result_list = []
    userdata_name = file_answer.split("\n")[0]
    userdata_values = file_answer.split("\n")[1]
    userdata_values_array = [float(x) for x in userdata_values.split(",")]
    
    result_list.append({"name": userdata_name, "values": userdata_values_array}) 
    result_list.append({"name": name, "values": values})

    return answer, json.dumps(result_list), 1

#两个函数都返回answer, result_list, flag
#flag = 0 表示不需要比较
#flag = 1 表示需要比较
#flag = -1 表示没有返回数据
#数据返回格式看代码
#有文件时返回的数据用户数据在前

#传入history时格式如下：(提前拼接好以字符串传过来)
# chat history:
# user:...
# system:...
# user:...
# system:...

