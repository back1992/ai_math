"""
Automated question generator using AI APIs
Supports: OpenAI, Anthropic, Google Gemini, or local LLMs
"""
import json
import os
import time
from generate_questions import (
    KNOWLEDGE_POINTS, 
    generate_question_prompt,
    save_generated_question,
    get_all_knowledge_points
)

def generate_with_openai(prompt, api_key):
    """Generate using OpenAI API"""
    try:
        import openai
        openai.api_key = api_key
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的小学数学老师，擅长出奥数题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        return None

def generate_with_anthropic(prompt, api_key):
    """Generate using Anthropic Claude API"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        print(f"❌ Anthropic Error: {e}")
        return None

def generate_with_gemini(prompt, api_key):
    """Generate using Google Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return None

def generate_with_ollama(prompt, model="qwen2.5:7b"):
    """Generate using local Ollama"""
    try:
        import requests
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False
            }
        )
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            print(f"❌ Ollama Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        return None

def parse_json_response(response_text):
    """Extract JSON from AI response"""
    # Remove markdown code blocks
    text = response_text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        print(f"响应内容: {text[:200]}...")
        return None

def generate_questions_batch(
    knowledge_points,
    api_type="gemini",
    api_key=None,
    difficulty="中等",
    questions_per_point=3,
    output_file='output/generated_questions.json'
):
    """
    Batch generate questions
    
    Args:
        knowledge_points: List of knowledge points or "all"
        api_type: "openai", "anthropic", "gemini", or "ollama"
        api_key: API key (not needed for ollama)
        difficulty: 难度级别
        questions_per_point: Number of questions per knowledge point
        output_file: Output JSON file
    """
    if knowledge_points == "all":
        knowledge_points = get_all_knowledge_points()
    
    total = len(knowledge_points) * questions_per_point
    print(f"🚀 开始生成题目")
    print(f"📚 知识点数量: {len(knowledge_points)}")
    print(f"📝 每个知识点: {questions_per_point} 题")
    print(f"📊 总计: {total} 题")
    print(f"🤖 使用API: {api_type}")
    print(f"💾 输出文件: {output_file}\n")
    
    generated_count = 0
    failed_count = 0
    
    for kp in knowledge_points:
        print(f"\n{'='*60}")
        print(f"📖 知识点: {kp}")
        print(f"{'='*60}")
        
        for i in range(questions_per_point):
            print(f"\n  生成第 {i+1}/{questions_per_point} 题...", end=" ")
            
            # Generate prompt
            prompt = generate_question_prompt(kp, difficulty)
            
            # Call AI API
            if api_type == "openai":
                response = generate_with_openai(prompt, api_key)
            elif api_type == "anthropic":
                response = generate_with_anthropic(prompt, api_key)
            elif api_type == "gemini":
                response = generate_with_gemini(prompt, api_key)
            elif api_type == "ollama":
                response = generate_with_ollama(prompt)
            else:
                print(f"❌ 不支持的API类型: {api_type}")
                return
            
            if response:
                # Parse JSON
                question_data = parse_json_response(response)
                
                if question_data:
                    # Save
                    save_generated_question(question_data, output_file)
                    generated_count += 1
                    print("✅")
                else:
                    failed_count += 1
                    print("❌ JSON解析失败")
            else:
                failed_count += 1
                print("❌ API调用失败")
            
            # Rate limiting
            time.sleep(1)
    
    print(f"\n{'='*60}")
    print(f"✅ 生成完成!")
    print(f"{'='*60}")
    print(f"成功: {generated_count} 题")
    print(f"失败: {failed_count} 题")
    print(f"输出: {output_file}")

def main():
    """Main function with examples"""
    print("🎓 AI自动生成小学6年级奥数题\n")
    
    # Example 1: Generate with Gemini (free tier)
    print("示例1: 使用Gemini生成3个知识点，每个2题")
    print("-" * 60)
    
    sample_points = [
        "数论-质数与合数",
        "应用题-行程问题",
        "几何-周长与面积"
    ]
    
    # Uncomment and add your API key to run
    # api_key = input("请输入Gemini API Key: ")
    # generate_questions_batch(
    #     knowledge_points=sample_points,
    #     api_type="gemini",
    #     api_key=api_key,
    #     difficulty="中等",
    #     questions_per_point=2
    # )
    
    print("\n💡 使用方法:")
    print("1. 选择API类型 (gemini/openai/anthropic/ollama)")
    print("2. 准备API Key (ollama不需要)")
    print("3. 运行生成:")
    print("\n   from generate_with_api import generate_questions_batch")
    print("   generate_questions_batch(")
    print("       knowledge_points=['数论-质数与合数'],")
    print("       api_type='gemini',")
    print("       api_key='your-api-key',")
    print("       questions_per_point=5")
    print("   )")

if __name__ == "__main__":
    main()
