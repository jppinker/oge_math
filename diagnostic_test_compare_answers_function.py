

def openrouter_request(problem_text, correct_answer, student_answer):
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-2.5-flash-preview-05-20",
        "messages": [
            {"role": "system", "content": "Ты учитель по математике."},
            {"role": "user", "content": f"Правильный ответ: {correct_answer}. Текст задачи: {problem_text}. Ответ студента: {student_answer}. Требование: не решай задачу, сравни ответ студента 'начало ответа' {student_answer} 'конец ответа' с правильным ответом 'начало ответа' {correct_answer} 'конец ответа'. Дай ответ как '1' если ответы совпадают, дай ответ как '0' если ответы не совпадают"}
        ],
        "max_tokens": 2000,
        "temperature": 0.2,
    }
    try:
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers, timeout=20)
        response.raise_for_status() # Проверка на HTTP ошибки
        # Проверка на корректность ответа от API
        content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        if content in ['0', '1']:
            return content
        else:
            print(f"Неожиданный ответ от API: {content}. Считаем ответ неверным.")
            return '0' # Если ответ не 0 или 1, считаем его неверным
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к OpenRouter: {e}")
        return '0' # В случае ошибки API считаем ответ неверным
    except (IndexError, KeyError, json.JSONDecodeError) as e:
        print(f"Ошибка обработки ответа от OpenRouter: {e}")
        return '0' # В случае ошибки парсинга считаем ответ неверным
