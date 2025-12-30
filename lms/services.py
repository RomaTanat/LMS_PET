import subprocess
import json
import os
from django.conf import settings
from .models import Submission

def analyze_code_submission(submission):
    problem = submission.problem
    test_cases = problem.test_cases
    code = submission.code
    
    # --- HARD CHECK (SANDBOX) ---
    all_passed = True
    results = []
    
    # Создаем временный файл для кода
    temp_file = f"temp_submission_{submission.id}.py"
    with open(temp_file, "w") as f:
        f.write(code)
    
    try:
        for i, test in enumerate(test_cases):
            stdin = test.get('stdin', '')
            expected_stdout = test.get('stdout', '').strip()
            timeout = test.get('timeout', 2)
            
            try:
                process = subprocess.run(
                    ['python3', temp_file],
                    input=stdin,
                    text=True,
                    capture_output=True,
                    timeout=timeout
                )
                
                actual_stdout = process.stdout.strip()
                
                if process.returncode != 0:
                    results.append({
                        'test_index': i,
                        'status': 'RUNTIME_ERROR',
                        'error': process.stderr
                    })
                    all_passed = False
                    break
                
                if actual_stdout != expected_stdout:
                    results.append({
                        'test_index': i,
                        'status': 'WRONG_ANSWER',
                        'stdin': stdin if not test.get('is_hidden') else '[HIDDEN]',
                        'expected': expected_stdout if not test.get('is_hidden') else '[HIDDEN]',
                        'actual': actual_stdout if not test.get('is_hidden') else '[HIDDEN]'
                    })
                    all_passed = False
                    break
                
            except subprocess.TimeoutExpired:
                results.append({
                    'test_index': i,
                    'status': 'TIME_LIMIT_EXCEEDED'
                })
                all_passed = False
                break
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    if all_passed:
        submission.status = 'ACCEPTED'
        submission.feedback = "Все тесты пройдены успешно!"
    else:
        submission.status = 'FAILED'
        # --- AI ANALYSIS (LLM) ---
        ai_feedback = get_ai_feedback(code, results[-1])
        submission.feedback = f"Тесты не пройдены. {ai_feedback}"
        
    submission.save()
    return submission

AI_INTEGRATIONS_OPENAI_API_KEY = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
AI_INTEGRATIONS_OPENAI_BASE_URL = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")

def get_ai_feedback(code, failure_reason):
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=AI_INTEGRATIONS_OPENAI_API_KEY,
            base_url=AI_INTEGRATIONS_OPENAI_BASE_URL
        )
        
        prompt = f"""
        Ты - опытный ментор по Python. Студент пытается решить задачу, но его код не проходит тесты.
        
        Код студента:
        ```python
        {code}
        ```
        
        Результат теста:
        {json.dumps(failure_reason)}
        
        Дай короткую, но емкую подсказку, что именно не так в логике кода. Не давай готовое решение, направь студента.
        Ответ верни в формате JSON: {{"hint": "текст подсказки"}}
        """
        
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content).get('hint', 'Попробуй проверить логику еще раз.')
    except Exception as e:
        return f"Ошибка при анализе кода: {str(e)}"
