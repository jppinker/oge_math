

#In this version, the algorithm decreases the difficulty of next question by 1 if the answer was wrong

import sqlite3
import random
from collections import defaultdict, deque

# Skill graph and test configuration
skill_graph = {
    # [Your complete skill_graph dictionary as provided]
    1: [],  # Натуральные и целые числа (фундаментальный)
    2: [1, 39],  # Научная форма числа -> Целые числа, Степень
    3: [1],  # Делимость чисел -> Натуральные числа
    4: [3],  # Признаки делимости -> Делимость
    5: [3],  # НОД и НОК -> Делимость
    6: [1],  # Обыкновенные и десятичные дроби -> Натуральные числа
    7: [6],  # Нахождение доли от числа -> Дроби
    8: [7],  # Вычисление процентов -> Доли
    9: [8],  # Повышение/понижение на процент -> Проценты
    10: [6], # Бесконечные периодические дроби -> Дроби
    11: [6, 1], # Определение рациональных чисел -> Дроби, Целые числа
    12: [11], # Расположение на координатной прямой -> Рац. числа
    13: [12], # Сравнение и упорядочивание -> Расположение на прямой
    14: [6, 5], # Преобразование дробей -> Дроби, НОД/НОК
    15: [14], # Арифметические действия с обыкновенными дробями -> Преобразование дробей
    16: [6],  # Арифметические действия с десятичными дробями -> Дроби
    17: [1],  # Раскрытие скобок, распределительное свойство (базовое)
    18: [11, 54], # Классификация действительных чисел -> Рац. числа, Корни
    19: [54], # Приближённое значение корня -> Определение корней
    20: [15, 16], # Арифметические действия с рациональными числами -> Действия с дробями
    21: [],  # Понятие точности и погрешности (концептуальное)
    22: [16], # Округление чисел -> Десятичные дроби
    23: [22], # Приближённые вычисления -> Округление
    24: [1], 25: [1], 26: [1], 27: [1], 28: [1], 29: [1], 30: [1], 31: [1], # Базовое чтение
    32: [27, 123, 16], # Путешествия -> Карта, Пифагор, Арифметика
    33: [26, 146], # Квартиры и участки -> План помещения, Площадь
    34: [28, 149, 142], # Шины, теплицы и т.д. -> Таблицы, Площади, Длина окружности
    35: [20], # Выражения с переменными -> Арифметика с рац. числами
    36: [35], # Подстановка значений -> Выражения с переменными
    37: [35, 17], # Упрощение выражений -> Выражения, Раскрытие скобок
    38: [17, 45], # Раскрытие скобок -> Распред. свойство, Многочлены
    39: [1],  # Определение степени с целым показателем -> Целые числа
    40: [39], # Степень с рац. показателем (Корни) -> Степень
    41: [39], # Умножение и деление степеней -> Степень
    42: [39], # Возведение степени в степень -> Степень
    43: [39], # Степень произведения и частного -> Степень
    44: [39], # Отрицательные степени -> Степень
    45: [35], # Одночлены и многочлены -> Выражения с переменными
    46: [45], # Приведение подобных членов -> Многочлены
    47: [46], # Сложение и вычитание многочленов -> Приведение подобных
    48: [47], # Умножение многочленов -> Сложение многочленов
    49: [48], # Разложение на множители -> Умножение многочленов
    50: [49, 15], # Алгебраические дроби -> Факторизация, Обыкн. дроби
    51: [50], # Основное свойство алг. дроби -> Алг. дроби
    52: [51], # Арифметика с алг. дробями -> Свойство алг. дроби
    53: [52], # Преобразование выражений с алг. дробями -> Арифметика с алг. дробями
    54: [1], # Определение корней (базовое)
    55: [54, 39], # Свойства корней -> Определение корней, Степень
    56: [55], # Арифметика с корнями -> Свойства корней
    57: [56], # Рационализация знаменателя -> Арифметика с корнями
    58: [37, 20], # Решение линейных уравнений -> Упрощение выражений, Арифметика
    59: [58], # Уравнения с дробями и скобками -> Линейные уравнения
    60: [58, 49, 55], # Квадратные уравнения -> Лин. уравнения, Факторизация, Свойства корней
    61: [58], # Системы линейных уравнений -> Линейные уравнения
    62: [53, 60], # Рациональные уравнения -> Выражения с алг. дробями, Квадр. уравнения
    63: [58], # Решение линейных неравенств -> Решение лин. уравнений
    64: [12], # Графическое представление решений -> Координатная прямая
    65: [63], # Решение систем неравенств -> Лин. неравенства
    66: [60, 94], # Квадратные неравенства -> Квадр. уравнения, Параболы
    67: [62], # Рациональные неравенства -> Рац. уравнения
    68: [66], # Метод интервалов -> Квадр. неравенства
    69: [],  # Перевод текста в уравнение (фундаментальный для блока)
    70: [69, 9, 15], # Задачи на проценты, сплавы -> Перевод в уравнение, Проценты, Дроби
    71: [69, 58], # Движение по прямой -> Перевод в уравнение, Лин. уравнения
    72: [71], # Движение по воде -> Движение по прямой
    73: [69, 58], # Совместная работа -> Перевод в уравнение, Лин. уравнения
    74: [69, 9], # Задачи про бизнес -> Перевод в уравнение, Проценты
    75: [69], # Разные текстовые задачи -> Перевод в уравнение
    76: [1],  # Запись последовательностей
    77: [76], # Способы задания последовательностей -> Запись
    78: [77], # Правило n-го члена -> Способы задания
    79: [78], # Определение следующего члена -> Правило n-го члена
    80: [78, 20], # Арифметическая прогрессия -> n-й член, Арифметика
    81: [80], # Сумма АП -> Арифметическая прогрессия
    82: [80], # Определение разности и первого члена АП -> АП
    83: [81, 69], # Текстовые задачи на АП -> Сумма АП, Перевод в уравнение
    84: [78, 20], # Геометрическая прогрессия -> n-й член, Арифметика
    85: [84], # Сумма ГП -> Геометрическая прогрессия
    86: [84], # Определение разности и первого члена ГП -> ГП
    87: [85, 69], # Текстовые задачи на ГП -> Сумма ГП, Перевод в уравнение
    88: [84, 9],  # Сложные проценты -> Геом. прогрессия, Проценты
    89: [],  # Определение функции (базовое)
    90: [89], # Область определения и множество значений -> Определение функции
    91: [89], # Нули функции
    92: [89, 110], # Построение графиков -> Определение функции, Построение точек
    93: [92, 58], # Линейные функции -> Построение, Лин. уравнения
    94: [92, 60], # Квадратичные функции -> Построение, Квадр. уравнения
    95: [92], # Гиперболы -> Построение
    96: [91], # Промежутки знакопостоянства -> Нули функции
    97: [90], # Промежутки монотонности -> Область определения
    98: [24], # Чтение графиков функции -> Чтение графиков (общий навык)
    99: [98], # Максимумы и минимумы -> Чтение графиков
    100: [99], # Наибольшее/наименьшее значение -> Максимумы/минимумы
    101: [92], # Кусочно-непрерывные функции -> Построение
    102: [92], # Растяжения и сдвиги -> Построение
    103: [12], # Расположение чисел на прямой -> Расположение рац. чисел
    104: [103], # Расстояние между точками на прямой -> Расположение
    105: [104], # Модули -> Расстояние
    106: [], # Интервалы (базовое)
    107: [13], # Неравенства (сравнение) -> Сравнение рац. чисел
    108: [103], # Сравнение на коорд. прямой -> Расположение
    109: [108], # Выбор верного утверждения -> Сравнение
    110: [], # Построение точек по координатам на плоскости
    111: [110, 123], # Расстояние между точками на плоскости -> Построение, Пифагор
    112: [], # Точки, прямые, отрезки (базовое)
    113: [112], # Углы и их виды -> Прямые
    114: [113], # Измерение углов -> Углы
    115: [113], # Параллельные и перпендикулярные прямые -> Углы
    116: [115, 118], # Серединный перпендикуляр -> Прямые, Элементы треугольника
    117: [112], # Виды треугольников -> Точки, прямые
    118: [117], # Элементы треугольника -> Виды треугольников
    119: [118], # Свойства углов треугольника -> Элементы
    120: [118], # Признаки равенства треугольников -> Элементы
    121: [118], # Признаки подобия треугольников -> Элементы
    122: [118], # Неравенство треугольника -> Элементы
    123: [117, 55], # Теорема Пифагора -> Прямоуг. треугольник, Свойства корней
    124: [123, 15], # Тригонометрия -> Пифагор, Действия с дробями
    125: [112], # Виды многоугольников -> Прямые
    126: [125], # Элементы многоугольников -> Виды
    127: [126], # Углы многоугольников -> Элементы
    128: [127], # Правильные многоугольники -> Углы
    129: [125], # Деление на треугольники -> Многоугольники
    130: [125, 115], # Прямоугольник -> Многоугольник, Параллельные прямые
    131: [133], # Ромб -> Параллелограмм
    132: [130, 131], # Квадрат -> Прямоугольник, Ромб
    133: [125, 115], # Параллелограмм -> Многоугольник, Параллельные прямые
    134: [125, 115], # Трапеция -> Многоугольник, Параллельные прямые
    135: [], # Элементы окружности (базовое)
    136: [135, 113], # Центральные и вписанные углы -> Элементы окружности, Углы
    137: [135, 125], # Вписанные фигуры -> Окружность, Многоугольники
    138: [135, 125], # Описанные фигуры -> Окружность, Многоугольники
    139: [], # Длина отрезка (базовое)
    140: [126, 139], # Периметр -> Элементы многоугольника, Длина отрезка
    141: [115], # Расстояние от точки до прямой -> Перпендикулярные прямые
    142: [135], # Длина окружности -> Элементы окружности
    143: [114], # Градусная мера угла -> Измерение углов
    144: [136, 142], # Угол и дуга -> Вписанные углы, Длина окружности
    145: [], # Площадь и её свойства (базовое)
    146: [130, 20], # Площадь прямоугольника -> Прямоугольник, Арифметика
    147: [133, 20], # Площадь параллелограмма -> Параллелограмм, Арифметика
    148: [134, 20], # Площадь трапеции -> Трапеция, Арифметика
    149: [117, 20], # Площадь треугольника -> Треугольник, Арифметика
    150: [135, 20], # Площадь круга -> Окружность, Арифметика
    151: [145, 7], # Пропорциональное деление площади -> Площадь, Доли
    152: [20], # Формулы объёма -> Арифметика
    153: [110, 145], # Фигуры на квадратной решётке -> Координаты, Площадь
    154: [110], # Направление и длина вектора -> Координаты
    155: [154], # Координаты вектора -> Направление и длина
    156: [155], # Сложение и вычитание векторов -> Координаты вектора
    157: [155], # Умножение вектора на число -> Координаты вектора
    158: [], # Анализ геометрических высказываний (логика)
    159: [], # Работа с чертежами (базовое)
    160: [120, 121, 130, 133], # Задачи на доказательство -> Признаки равенства/подобия и т.д.
    161: [160], # Геометрические задачи повышенной сложности -> Доказательство
    162: [], # Сбор данных
    163: [25, 28], # Таблицы и диаграммы в статистике -> Чтение схем
    164: [162, 16], # Среднее арифметическое -> Сбор данных, Арифметика
    165: [162], # Мода и медиана -> Сбор данных
    166: [], # Определение событий (базовое)
    167: [166, 7], # Нахождение вероятности -> События, Нахождение доли
    168: [167], # Применение формул вероятности -> Нахождение вероятности
    169: [1], # Перестановки -> Натуральные числа
    170: [1], # Размещения
    171: [1], # Сочетания
    172: [169, 170, 171], # Подсчёт с использованием формул -> Комбинаторика
    173: [], # Операции с множествами
    174: [173], # Диаграммы Эйлера–Венна -> Множества
    175: [], # Вершины и рёбра (базовое)
    176: [175], # Связность графа -> Вершины и рёбра
    177: [176], # Поиск путей -> Связность
    178: [177], # Решение прикладных задач с графами -> Поиск путей
}

# Test configuration: skills and their difficulty levels
test_config = {
    "1": 1, "6": 3, "20": 3, "69": 3, "89": 2, "110": 2, "112": 2, "135": 2, 
    "106": 2, "139": 3, "145": 2, "158": 1, "162": 3, "167": 1, "173": 1, 
    "48": 2, "56": 2, "80": 1, "120": 2, "133": 2
}

class MathTester:
    def __init__(self, db_path):
        """Initialize the tester with database connection"""
        self.db_path = db_path
        self.student_answers = []  # Store (skill, difficulty, correct_answer, student_answer, is_correct)
        self.current_difficulty = None  # Track current difficulty level
        self.questions_asked = 0  # Track number of questions asked
    def connect_db(self):
        """Connect to the SQLite database"""
        return sqlite3.connect(self.db_path)
    
    def get_question(self, skill, difficulty):
        """Get a random question for specific skill and difficulty"""
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Query for questions with the specific skill and difficulty
        cursor.execute("""
            SELECT problem_text, answer 
            FROM problems_oge_diagnostic 
            WHERE skills = ? AND difficulty = ?
        """, (skill, difficulty))
        
        questions = cursor.fetchall()
        conn.close()
        
        if not questions:
            print(f"Warning: No questions found for skill {skill}, difficulty {difficulty}")
            return None, None
            
        # Return a random question from available options
        problem_text, answer = random.choice(questions)
        return problem_text, answer
    
    def run_test(self):
        """Run the complete diagnostic test with adaptive difficulty"""
        print("=== Диагностический тест для ОГЭ по математике ===")
        print("✓ Прохождение теста не займет много времени! ✓")
        print("Вам будут предложены 20 задач с вариантами ответов.\n")
        
        question_number = 1
        skills = list(test_config.keys())
        current_difficulty = None
    
        for i, skill_str in enumerate(skills):
            skill = int(skill_str)
        
            # Determine difficulty for this question
            if i == 0:
                # First question uses base difficulty
                current_difficulty = test_config[skill_str]
            else:
                # Subsequent questions use adjusted difficulty based on previous answer
                prev_correct = self.student_answers[-1][4]  # Get correctness of previous answer
                base_difficulty = test_config[skill_str]
                
                if prev_correct is False:  # Previous answer was incorrect
                    current_difficulty = max(1, base_difficulty - 1)
                else:  # Previous correct or skipped
                    current_difficulty = base_difficulty
            
            print(f"\n--- Задача {question_number} (Навык {skill}, Сложность {current_difficulty}) ---")
            
            # Get question for this skill and difficulty
            problem_text, correct_answer = self.get_question(skill, current_difficulty)
            
            if problem_text is None:
                # If no question available, mark as skipped
                self.student_answers.append((skill, current_difficulty, None, None, None))
                question_number += 1
                continue
            
            # Display question
            print(f"Задача: {problem_text}")
            
            # Get student answer
            student_answer = input("Ваш ответ: ").strip()
            
            # Check if answer is correct
            if student_answer == "":
                is_correct = None  # Skipped
            else:
                is_correct = self.check_answer(student_answer, correct_answer)
                
            # Store result
            self.student_answers.append((skill, current_difficulty, correct_answer, student_answer, is_correct))
            
            # Provide feedback
            if is_correct is None:
                print("Задача пропущена")
            elif is_correct:
                print("✓ Ваш ответ ВЕРНЫЙ!")
            else:
                print(f"✗ Ваш ответ НЕВЕРНЫЙ. Правильный ответ: {correct_answer}")
            
            question_number += 1
        
        print("\n=== Тест завершен! ===")
        return self.analyze_results()
    
    def check_answer(self, student_answer, correct_answer):
        """Check if student answer matches correct answer"""
        # Simple string comparison - could be enhanced for mathematical equivalence
        try:
            # Try numerical comparison first
            return float(student_answer) == float(correct_answer)
        except ValueError:
            # Fall back to string comparison
            return student_answer.lower().strip() == str(correct_answer).lower().strip()
    
    def build_children_graph(self):
        """Build reverse graph to find children of each skill"""
        children = defaultdict(list)
        for child, parents in skill_graph.items():
            for parent in parents:
                children[parent].append(child)
        return children
    
    def get_all_descendants(self, skill, children_graph):
        """Get all descendant skills using BFS"""
        descendants = set()
        queue = deque([skill])
        
        while queue:
            current = queue.popleft()
            for child in children_graph[current]:
                if child not in descendants:
                    descendants.add(child)
                    queue.append(child)
        
        return descendants
    
    def get_all_ancestors(self, skill):
        """Get all ancestor skills using BFS"""
        ancestors = set()
        queue = deque([skill])
        visited = set([skill])
        
        while queue:
            current = queue.popleft()
            for parent in skill_graph.get(current, []):
                if parent not in visited:
                    ancestors.add(parent)
                    visited.add(parent)
                    queue.append(parent)
        
        return ancestors
    
    def calculate_skill_importance(self):
        """Calculate importance scores for skills based on graph structure"""
        children_graph = self.build_children_graph()
        importance = {}
        
        for skill in skill_graph.keys():
            # Count ancestors (depth in dependency tree)
            ancestors = self.get_all_ancestors(skill)
            ancestor_count = len(ancestors)
            
            # Count descendants (how many skills depend on this one)
            descendants = self.get_all_descendants(skill, children_graph)
            descendant_count = len(descendants)
            
            # Importance = base + descendants + depth_penalty
            # Skills with more descendants are more important
            # Skills deeper in the tree get slight penalty (they're more advanced)
            importance[skill] = 10 + descendant_count * 2 - ancestor_count * 0.1
        
        return importance
    
    def analyze_results(self):
        """Analyze test results and generate diagnostic report"""
        children_graph = self.build_children_graph()
        
        # Track directly tested skills
        directly_failed = set()
        directly_passed = set()
        
        # Analyze direct test results
        for skill, difficulty, correct_answer, student_answer, is_correct in self.student_answers:
            if is_correct is False:  # Failed (not skipped)
                directly_failed.add(skill)
            elif is_correct is True:  # Passed
                directly_passed.add(skill)
        
        # Infer weak skills based on dependencies
        weak_skills = set(directly_failed)
        
        # If a skill failed, mark all its descendants as weak
        for failed_skill in directly_failed:
            descendants = self.get_all_descendants(failed_skill, children_graph)
            weak_skills.update(descendants)
        
        # Infer knowledge for untested skills
        all_tested_skills = set(int(skill) for skill, _, _, _, _ in self.student_answers)
        all_skills = set(skill_graph.keys())
        untested_skills = all_skills - all_tested_skills
        
        # For untested skills, infer based on prerequisites
        inferred_knowledge = {}
        for skill in untested_skills:
            prerequisites = set(skill_graph.get(skill, []))
            
            if prerequisites:
                # If any prerequisite is weak, this skill is likely weak
                if prerequisites.intersection(weak_skills):
                    weak_skills.add(skill)
                    inferred_knowledge[skill] = "likely_weak"
                # If all prerequisites are strong, this might be okay
                elif prerequisites.issubset(directly_passed):
                    inferred_knowledge[skill] = "likely_okay"
                else:
                    inferred_knowledge[skill] = "uncertain"
            else:
                # Foundational skill - assume okay if not tested
                inferred_knowledge[skill] = "assumed_okay"
        
        # Calculate importance scores
        importance_scores = self.calculate_skill_importance()
        
        # Categorize foundational skills to address
        weak_foundational = []
        for skill in weak_skills:
            # Add importance score for sorting
            score = importance_scores.get(skill, 0)
            ancestors = self.get_all_ancestors(skill)
            depth = len(ancestors)
            
            weak_foundational.append({
                'skill': skill,
                'importance': score,
                'depth': depth,
                'prerequisite_count': len(skill_graph.get(skill, [])),
                'dependent_count': len(self.get_all_descendants(skill, children_graph))
            })
        
        # Sort by importance (high importance first) and depth (shallow first)
        weak_foundational.sort(key=lambda x: (-x['importance'], x['depth']))
        
        # Divide into three priority groups
        total_weak = len(weak_foundational)
        first_third = total_weak // 3
        second_third = 2 * total_weak // 3
        
        # Generate recommendations
        diagnostic_report = {
            "weak_skills": list(weak_skills),
            "foundational_skills_to_address_first": [s['skill'] for s in weak_foundational[:first_third]],
            "foundational_skills_to_address_second": [s['skill'] for s in weak_foundational[first_third:second_third]],
            "foundational_skills_to_address_third": [s['skill'] for s in weak_foundational[second_third:]]
        }
        
        # Print detailed report
        print(f"\n=== ДИАГНОСТИЧЕСКИЙ РЕПОРТ ===")
        print(f"Всего отвечено вопросов: {len(self.student_answers)}")
        print(f"Провалено навыков напрямую (неправильные ответы): {len(directly_failed)}")
        print(f"Всего слабых навыков (с учётом зависимостей): {len(weak_skills)}")
        print(f"\nРезультаты тестирования:")
        for skill, difficulty, correct, student, is_correct in self.student_answers:
            status = "✓" if is_correct else "✗" if is_correct is False else "⊝"
            print(f"  Навык {skill}: {status}")
        
        print(f"\nВыявленные слабые навыки: {sorted(weak_skills)}")
        print(f"\nПриоритеты обучения:")
        print(f"  В первую очередь: {diagnostic_report['foundational_skills_to_address_first']}")
        print(f"  Во вторую очередь: {diagnostic_report['foundational_skills_to_address_second']}")
        print(f"  В третью очередь: {diagnostic_report['foundational_skills_to_address_third']}")
        
        return diagnostic_report

def main():
    """Main function to run the diagnostic test"""
    db_path = "/home/alex/Downloads/ideas/ogemath/final_stuff_diagnostic/problems_oge_diagnostic.db"
    
    # Initialize and run the test
    tester = MathTester(db_path)
    
    try:
        # Run the diagnostic test
        diagnostic_report = tester.run_test()
        
        # Save report to file (optional)
        import json
        with open("diagnostic_report.json", "w", encoding="utf-8") as f:
            json.dump(diagnostic_report, f, indent=2, ensure_ascii=False)
        
        print(f"\nДиагностический Репорт сохранен в корневую директорию: 'diagnostic_report.json'")
        
        return diagnostic_report
        
    except Exception as e:
        print(f"Error running test: {e}")
        return None

if __name__ == "__main__":
    main()
