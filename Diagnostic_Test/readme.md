
## Key Features of the Implementation:

### 1. **Database Integration**
- Connects to SQLite database at specified path
- Queries questions based on skill number and difficulty level
- Handles missing questions gracefully

### 2. **Test Execution**
- Presents questions in the exact order specified in `test_config`
- Collects student answers and compares with correct answers
- Allows skipping questions
- Provides immediate feedback

### 3. **Sophisticated Analysis Algorithm**
- **Direct failure propagation**: If skill A fails, all descendants are marked weak
- **Graph-based inference**: Uses skill dependencies to infer knowledge of untested skills
- **Importance scoring**: Calculates skill importance based on:
  - Number of dependent skills (descendants)
  - Depth in dependency tree
  - Overall connectivity

### 4. **Learning Recommendations**
- Categorizes weak skills by priority based on:
  - Importance score (skills with more dependents get higher priority)
  - Depth in dependency tree (foundational skills first)
  - Divides recommendations into three priority groups

### 5. **Comprehensive Output**
- **weak_skills**: All skills identified as weak (failed + their descendants)
- **foundational_skills_to_address_first**: Highest priority skills to study
- **foundational_skills_to_address_second**: Medium priority skills
- **foundational_skills_to_address_third**: Lower priority skills

The algorithm properly handles the cascading effect where failing a foundational skill (like skill 1 - Natural numbers) would mark all dependent skills as weak, while prioritizing the most foundational and impactful skills for remediation.

################################################################################################################################################################################

1. First, we have to state clearly what our goal is. The goal of our Entry Diagnostic Test is to identify SIGNIFICANT knowledge gaps in CRUCIAL areas.

Users are not willing to solve a lot of questions on first login. So we have to implement solution given the problem: "for the least possible amount of questions determine the crucial knowledge gaps in the OGE math curriculum".


2. To make our inference of a student's weak areas more effective, we structured SKILLS needed for the OGE exam in the form of a Graph, where each node is a skill and edges are representing the child-parent relations between skills. We make the Graph definition out of Math logic (for example, "natural numbers" -> "arithmetic operations" -> linear equations -> "systems of linear equations").

3. We need to make a classification of skills in the context of their place in the Graph.


===== A. =====

We find the parent skills for each skill (we count as 1 the skill itself, so root skills have values of 1)

{1: 1, 2: 3, 3: 2, 4: 3, 5: 3, 6: 2, 7: 3, 8: 4, 9: 5, 10: 3, 11: 3, 12: 4, 13: 5, 14: 4, 15: 5, 16: 3, 17: 2, 18: 4, 19: 3, 20: 6, 21: 1, 22: 4, 23: 5, 24: 2, 25: 2, 26: 2, 27: 2, 28: 2, 29: 2, 30: 2, 31: 2, 32: 5, 33: 8, 34: 5, 35: 7, 36: 8, 37: 8, 38: 8, 39: 2, 40: 3, 41: 3, 42: 3, 43: 3, 44: 3, 45: 8, 46: 9, 47: 10, 48: 11, 49: 12, 50: 13, 51: 14, 52: 15, 53: 16, 54: 2, 55: 3, 56: 4, 57: 5, 58: 9, 59: 10, 60: 13, 61: 10, 62: 17, 63: 10, 64: 5, 65: 11, 66: 14, 67: 18, 68: 15, 69: 1, 70: 7, 71: 10, 72: 11, 73: 10, 74: 6, 75: 2, 76: 2, 77: 3, 78: 4, 79: 5, 80: 7, 81: 8, 82: 8, 83: 9, 84: 7, 85: 8, 86: 8, 87: 9, 88: 8, 89: 1, 90: 2, 91: 2, 92: 2, 93: 11, 94: 14, 95: 3, 96: 3, 97: 3, 98: 3, 99: 4, 100: 5, 101: 3, 102: 3, 103: 5, 104: 6, 105: 7, 106: 1, 107: 6, 108: 6, 109: 7, 110: 1, 111: 5, 112: 1, 113: 2, 114: 3, 115: 3, 116: 5, 117: 2, 118: 3, 119: 4, 120: 4, 121: 4, 122: 4, 123: 4, 124: 6, 125: 2, 126: 3, 127: 4, 128: 5, 129: 3, 130: 4, 131: 5, 132: 5, 133: 4, 134: 4, 135: 1, 136: 3, 137: 4, 138: 4, 139: 1, 140: 4, 141: 4, 142: 2, 143: 4, 144: 4, 145: 1, 146: 7, 147: 7, 148: 7, 149: 7, 150: 3, 151: 5, 152: 7, 153: 3, 154: 2, 155: 3, 156: 4, 157: 4, 158: 1, 159: 1, 160: 5, 161: 6, 162: 1, 163: 3, 164: 4, 165: 2, 166: 1, 167: 4, 168: 5, 169: 2, 170: 2, 171: 2, 172: 3, 173: 1, 174: 2, 175: 1, 176: 2, 177: 3, 178: 4}



Root Skills (Depth 1): Skills with no prerequisites (e.g., 1, 21, 69, 89, 106, 110, 112, 135, 139, 145, 158, 159, 162, 166, 173, 175).

Maximum Depth (18): Skill 67 (Рациональные неравенства) has the deepest dependency chain.

Longest Chain Example: Skill 67 (depth 18) depends on Skill 62 (depth 17), which depends on Skill 53 (depth 16), and so on, down to root skills.

We will write down the Root Skills:

[1, 21, 69, 89, 106, 110, 112, 135, 139, 145, 158, 159, 162, 166, 173, 175]



===== B. ====== 

We define a critical_number for a skill X as a number of skills that require the skill X in their prerequisites. For example, Let X be 1, critical_number is 0 by default, then we take skill 2 and find its all deepest parents and if there is X among them we update critical_number as critical_number+1. And then we check the same condition for skill 3 and so on up to skill 178.

Top 20 skills by critical numbers:

[1, 20, 58, 6, 69, 125, 39, 89, 92, 115, 135, 110, 118, 12, 15, 16, 35, 45, 78, 112]

The critical_numbers are:

{
  "1": 77,
  "2": 0,
  "3": 2,
  "4": 0,
  "5": 2,
  "6": 7,
  "7": 2,
  "8": 3,
  "9": 3,
  "10": 0,
  "11": 2,
  "12": 4,
  "13": 2,
  "14": 1,
  "15": 4,
  "16": 4,
  "17": 2,
  "18": 0,
  "19": 0,
  "20": 9,
  "21": 0,
  "22": 1,
  "23": 0,
  "24": 1,
  "25": 1,
  "26": 1,
  "27": 1,
  "28": 2,
  "29": 0,
  "30": 0,
  "31": 0,
  "32": 0,
  "33": 0,
  "34": 0,
  "35": 4,
  "36": 0,
  "37": 1,
  "38": 0,
  "39": 6,
  "40": 0,
  "41": 0,
  "42": 0,
  "43": 0,
  "44": 0,
  "45": 4,
  "46": 1,
  "47": 1,
  "48": 1,
  "49": 2,
  "50": 1,
  "51": 1,
  "52": 1,
  "53": 1,
  "54": 3,
  "55": 2,
  "56": 1,
  "57": 0,
  "58": 8,
  "59": 0,
  "60": 3,
  "61": 0,
  "62": 1,
  "63": 1,
  "64": 0,
  "65": 0,
  "66": 1,
  "67": 0,
  "68": 0,
  "69": 7,
  "70": 0,
  "71": 1,
  "72": 0,
  "73": 0,
  "74": 0,
  "75": 0,
  "76": 1,
  "77": 1,
  "78": 4,
  "79": 0,
  "80": 2,
  "81": 1,
  "82": 0,
  "83": 0,
  "84": 2,
  "85": 1,
  "86": 0,
  "87": 0,
  "88": 0,
  "89": 6,
  "90": 1,
  "91": 1,
  "92": 6,
  "93": 0,
  "94": 1,
  "95": 0,
  "96": 0,
  "97": 0,
  "98": 1,
  "99": 1,
  "100": 0,
  "101": 0,
  "102": 0,
  "103": 3,
  "104": 1,
  "105": 0,
  "106": 0,
  "107": 0,
  "108": 1,
  "109": 0,
  "110": 5,
  "111": 0,
  "112": 4,
  "113": 3,
  "114": 1,
  "115": 6,
  "116": 0,
  "117": 3,
  "118": 5,
  "119": 0,
  "120": 1,
  "121": 1,
  "122": 0,
  "123": 2,
  "124": 0,
  "125": 7,
  "126": 2,
  "127": 1,
  "128": 0,
  "129": 0,
  "130": 2,
  "131": 1,
  "132": 0,
  "133": 2,
  "134": 1,
  "135": 6,
  "136": 1,
  "137": 0,
  "138": 0,
  "139": 1,
  "140": 0,
  "141": 0,
  "142": 2,
  "143": 0,
  "144": 0,
  "145": 2,
  "146": 1,
  "147": 0,
  "148": 0,
  "149": 1,
  "150": 0,
  "151": 0,
  "152": 0,
  "153": 0,
  "154": 1,
  "155": 2,
  "156": 0,
  "157": 0,
  "158": 0,
  "159": 0,
  "160": 1,
  "161": 0,
  "162": 2,
  "163": 0,
  "164": 0,
  "165": 0,
  "166": 1,
  "167": 1,
  "168": 0,
  "169": 1,
  "170": 1,
  "171": 1,
  "172": 0,
  "173": 1,
  "174": 0,
  "175": 1,
  "176": 1,
  "177": 1,
  "178": 0
}





The intersection of =====A.===== and =====B.====== is given by skills  [1, 69, 89, 110, 112, 135]. These constitute the highest-priority testing targets in the diagnostic assessment.



Then we ask: supose a student failed the skills [1, 69, 89, 110, 112, 135], what skills will be considered as weak? The answer is all skills except [21, 106, 139, 145, 158, 159, 162, 165, 166, 173, 174, 175, 176, 177, 178].  From these skills we pick by hand the most important ones. These will be: 106, 139, 145, 158, 162, 166, 173.

Combining intersection skills and key independent skills yields the initial testing pool: [1, 69, 89, 110, 112, 135, 106, 139, 145, 158, 162, 167, 173]

To ensure comprehensive curriculum representation, we add skills from underrepresented domains. So we add skills from missing domains:

2. Алгебраические выражения
skills 48, 56

4. Числовые последовательности
skills 80

7. Геометрия
skills 120, 133


So the final list of skills we have to test if we want to cover the whole graph in the least amount of skills tested:

[1, 69, 89, 110, 112, 135, 106, 139, 145, 158, 162, 167, 173, 48, 56, 80, 120, 133]

To ensure accurate skill assessment, problem difficulty is inversely scaled to skill fundamentality: since some skills are simple we need to offer more difficult problems for simpler skills. Here is the dictionary with skills as keys and difficulty level as values:

{"1": 3, "69": 3, "89": 3, "110": 2, "112": 2, "135": 2, "106": 1, "139": 1, "145": 2, "158": 1, "162": 2, "167": 1, "173": 2, "48": 2, "56": 3, "80": 1, "120": 2, "133": 2}


