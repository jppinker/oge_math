def process_user_query(user_query):
    import requests
    import json
    import sqlite3
    import os
    import csv
    from datetime import datetime
    api_key = ""
    def get_oge_rag_data(X):
        """
        Query the oge_rag table and return system_prompt and context for a given ID
        
        Parameters:
        X (int): The id value to query
        
        Returns:
        tuple: (system_message, context) or (None, None) if not found
        """
        
        # Define the database path
        db_path = "/home/alex/Downloads/ideas/ogemath/final_staff_RAG/oge_entrypage_rag.db"
        
        try:
            # Connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query the database for the given ID
            cursor.execute("""
                SELECT system_prompt, context 
                FROM oge_rag 
                WHERE id = ?
            """, (X,))
            
            # Fetch the result
            result = cursor.fetchone()
            
            # Close the connection
            conn.close()
            
            # Return the results or (None, None) if not found
            if result:
                system_message, context = result
                return system_message, context
            else:
                #print(f"No row found with id = {X}")
                return None, None
                
        except sqlite3.Error as e:
            #print(f"Database error: {e}")
            return None, None
        except Exception as e:
            #print(f"Error: {e}")
            return None, None

    def openrouter_call(api_key, model_name, prompt, system_message, temperature):
        """
        Simple API call to OpenRouter
        
        Parameters:
        api_key (str): Your OpenRouter API key
        model_name (str): The model name to use
        prompt (str): The user prompt/message
        system_message (str): System message (optional)
        
        Returns:
        str: The generated response text or None if error
        """
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            #print(f"Error: {e}")
            return None

    def openrouter_call_stream(api_key, model_name, prompt, system_message, temperature):
        """
        Simple API call to OpenRouter
        
        Parameters:
        api_key (str): Your OpenRouter API key
        model_name (str): The model name to use
        prompt (str): The user prompt/message
        system_message (str): System message (optional)
        
        Returns:
        str: The generated response text or None if error
        """
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_message + " Give output using simple LaTeX syntax. *IMPORTATNT*: avoid environments enumerate, itemize"},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "stream": True,
            "max_tokens": 2000
        }
        
        try:
            with requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               json=payload, headers=headers, 
                               stream=True) as resp:
                resp.raise_for_status()  # Raise an exception for bad status codes
                for line in resp.iter_lines():
                    if line:
                        decoded = line.decode("utf-8")
                        if decoded.startswith("data: "):
                            payload = decoded[len("data: "):]
                            if payload.strip() == "[DONE]":
                                break
                            try:
                                event = json.loads(payload)
                                delta = event["choices"][0]["delta"].get("content", "")
                                if delta:
                                    print(delta, end="", flush=True)  # print tokens in real-time
                            except json.JSONDecodeError:
                                pass
        except requests.exceptions.RequestException as e:
            print(f"Неполадки в сети, попробуйте позже")
        except KeyError as e:
            print(f"Неполадки в сети, попробуйте позже")
        except Exception as e:
            print(f"Неполадки в сети, попробуйте позже")
        finally:
            print()  # newline after streaming

    def insert_user_query(userquery):
        """
        Insert a user query and current timestamp into the query_data table.
        
        Args:
            userquery (str): The user's query string to insert
        """
        db_path = "/home/alex/Downloads/ideas/ogemath/final_staff_RAG/entrypage_query_data.db"
        
        try:
            # Create connection
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Insert the user query with current timestamp
            cursor.execute(
                "INSERT INTO query_data (userquery, timestamp) VALUES (?, ?)",
                (userquery, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            
            # Commit the changes
            conn.commit()
            #print(f"Successfully inserted query: {userquery}")
            
        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    # Main function logic
    insert_user_query(user_query)
    router_prompt = f'''
Ты — классификатор. У тебя есть список категорий с номерами (см. ниже). Определи, к какой категории относится вопрос школьника, и верни только номер категории (одно число).
Список категорий:
1. Общий вопрос по математике — вопрос о математических понятиях, формулах, теоремах, методах решения.
2. Вопрос по математике в контексте экзамена ОГЭ — вопрос о решении заданий ОГЭ, типах задач по номерам, типах задач по навыкам/скиллам, типах задач по темам, математических методах, применяемых именно в ОГЭ.
3. Вопрос по проверке и анализу решения. Ключевые маркеры: 'проверь', 'где ошибка', 'правильно ли я решил', 'засчитают ли', и тому подобное.
4. Вопрос с требованием дать задачу определенного типа - например задачу 12, задачу 21, и так далее разных номеров, или задачу на определенную тему ОГЭ.
5. Вопросы о распространенных ошибках в задачах или на экзамене. Вопрос о разборе ошибок или типичных ловушках. 
6. Общий вопрос об экзамене ОГЭ по математике — вопрос о структуре экзамена, частях, типах задач, сложности задас, продолжительности экзамена, правилах проведения, без решения задач.
7. Вопрос о личном прогрессе в подготовке — какие темы нужно учить, насколько хорошо решаю задачи, какие задачи получаются хуже или лучше других, и тому подобное.
8. Вопрос о критериях оценивания и баллах — вопрос о том, сколько баллов нужно для сдачи, как переводятся баллы в оценки, как оценивают задания.
9. Вопрос об изменениях или новостях по ОГЭ — вопрос о новых правилах, изменениях КИМ, официальных распоряжениях.
10. Общий вопрос об учебе и подготовке — вопрос о методах подготовки, распределении времени, мотивации, не обязательно связанных с ОГЭ.
11. Вопрос о работе с платформой — вопрос о функциях платформы, интерфейсе, загрузке материалов, технических проблемах.
12. Вопрос об учебных материалах и источниках — вопрос о книгах, сайтах, видеоуроках, источниках задач.
13. Личные и мотивационные вопросы — вопрос о страхах, волнении, психологической поддержке, настрое перед экзаменом.
14. Вопрос, не относящийся к учебе — вопрос о темах, не связанных с математикой, ОГЭ или подготовкой.

Вопрос школьника: {user_query}

Ответь одним числом — номером категории.
'''
    result = openrouter_call(api_key, model_name="google/gemini-2.5-flash-lite-preview-06-17", prompt=router_prompt, system_message="Ты — классификатор. У тебя есть список категорий с номерами (см. ниже). Определи, к какой категории относится вопрос школьника, и верни только номер категории (одно число).", temperature=0)
    result = result.replace('\n','')
    #print(result)
    system_message, context = get_oge_rag_data(int(result))

    router_prompt = f'''
Вопрос школьника: {user_query}

Контекст: {context}
'''

    result = openrouter_call_stream(api_key, model_name="google/gemma-3-4b-it", prompt=router_prompt, system_message=system_message, temperature=0.7)
    
    return result
