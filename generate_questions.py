"""
AI Question Generator for Grade 6 Math (小学6年级奥数题)
Uses free local LLM or API to generate high-quality questions
"""
import json
import os
from datetime import datetime

# Load knowledge points from JSON file
def load_knowledge_points():
    """Load knowledge points from data/knowledge_points.json"""
    json_path = 'data/knowledge_points.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Global knowledge points data
KNOWLEDGE_DATA = load_knowledge_points()

def get_all_modules():
    """Get all modules with their topics"""
    return KNOWLEDGE_DATA['modules']

def get_all_knowledge_points():
    """Get flat list of all knowledge points (module-topic format)"""
    points = []
    for module in KNOWLEDGE_DATA['modules']:
        module_name = module['name']
        for topic in module['topics']:
            topic_name = topic['name']
            points.append(f"{module_name}-{topic_name}")
    return points

def get_knowledge_points_by_phase(phase=1):
    """Get knowledge points for a specific learning phase"""
    phase_key = f"phase_{phase}"
    module_ids = KNOWLEDGE_DATA['learning_path'][phase_key]['modules']
    
    points = []
    for module_id in module_ids:
        module = next(m for m in KNOWLEDGE_DATA['modules'] if m['id'] == module_id)
        module_name = module['name']
        for topic in module['topics']:
            points.append(f"{module_name}-{topic['name']}")
    return points

def generate_question_prompt(knowledge_point, difficulty="中等"):
    """
    Generate prompt for AI to create a question
    
    Args:
        knowledge_point: 知识点 (e.g., "数论-质数与合数")
        difficulty: 难度 (简单/中等/困难)
    
    Returns:
        Prompt string
    """
    prompt = f"""请出一道小学6年级的奥数题，要求如下：

知识点：{knowledge_point}
难度：{difficulty}

请按以下JSON格式输出：
{{
  "题目": "完整的题目描述",
  "选项": ["A. ...", "B. ...", "C. ...", "D. ..."],  // 如果是选择题
  "答案": "正确答案",
  "解析": "详细的解题步骤和思路",
  "知识点": "{knowledge_point}",
  "难度": "{difficulty}",
  "题型": "选择题/填空题/解答题"
}}

要求：
1. 题目要有实际应用场景，贴近生活
2. 难度适合小学6年级学生
3. 解析要详细，包含解题思路和步骤
4. 如果是选择题，要有4个选项
5. 只返回JSON，不要其他文字

请生成题目："""
    
    return prompt

def save_generated_question(question_data, output_file='output/generated_questions.json'):
    """Save generated question to JSON file"""
    # Load existing questions
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    else:
        questions = []
    
    # Add metadata
    question_data['生成时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    question_data['题号'] = len(questions) + 1
    
    # Append new question
    questions.append(question_data)
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存第 {len(questions)} 题到 {output_file}")
    return len(questions)

def generate_batch_prompts(knowledge_points, difficulty="中等", count_per_point=3):
    """
    Generate batch of prompts for multiple questions
    
    Args:
        knowledge_points: List of knowledge points
        difficulty: 难度
        count_per_point: Number of questions per knowledge point
    
    Returns:
        List of prompts
    """
    prompts = []
    for kp in knowledge_points:
        for i in range(count_per_point):
            prompt = generate_question_prompt(kp, difficulty)
            prompts.append({
                'knowledge_point': kp,
                'difficulty': difficulty,
                'prompt': prompt,
                'index': i + 1
            })
    return prompts

def show_knowledge_points():
    """Display all available knowledge points"""
    print("\n📚 小学6年级奥数知识点：\n")
    print(f"来源：{KNOWLEDGE_DATA['metadata']['source']}")
    print(f"难度：{KNOWLEDGE_DATA['metadata']['difficulty_range']}\n")
    
    for module in KNOWLEDGE_DATA['modules']:
        difficulty_stars = "★" * module['difficulty']
        print(f"【{module['id']}. {module['name']}】 {difficulty_stars} ({module['frequency']})")
        print(f"   {module['name_en']}")
        for i, topic in enumerate(module['topics'], 1):
            print(f"   {i}. {topic['name']} / {topic['name_en']}")
        print()

def main():
    """Main function - example usage"""
    print("🎓 小学6年级奥数题生成器\n")
    
    # Show available knowledge points
    show_knowledge_points()
    
    # Example: Generate prompts for a few knowledge points
    sample_points = [
        "数论-质数与合数",
        "应用题-行程问题",
        "几何-周长与面积"
    ]
    
    print(f"📝 示例：生成 {len(sample_points)} 个知识点的题目提示词\n")
    
    for kp in sample_points:
        prompt = generate_question_prompt(kp, "中等")
        print(f"知识点：{kp}")
        print(f"提示词长度：{len(prompt)} 字符")
        print("-" * 60)
        print(prompt[:200] + "...")
        print("=" * 60)
        print()
    
    print("\n💡 使用方法：")
    print("1. 选择知识点")
    print("2. 生成提示词")
    print("3. 发送给AI (Gemini/GPT/Claude/本地LLM)")
    print("4. 保存返回的JSON到文件")
    print("\n或者使用 generate_with_api.py 自动批量生成")

if __name__ == "__main__":
    main()
