#!/usr/bin/env python3
"""
Interactive CLI for generating math questions
"""
from generate_questions import KNOWLEDGE_POINTS, show_knowledge_points
from generate_with_api import generate_questions_batch

def select_knowledge_points():
    """Interactive knowledge point selection"""
    print("\n📚 选择知识点：")
    print("1. 全部知识点")
    print("2. 选择类别")
    print("3. 自定义选择")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        from generate_questions import get_all_knowledge_points
        return get_all_knowledge_points()
    
    elif choice == "2":
        print("\n类别：")
        categories = list(KNOWLEDGE_POINTS.keys())
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        cat_choice = input("\n选择类别 (1-6): ").strip()
        try:
            cat_idx = int(cat_choice) - 1
            category = categories[cat_idx]
            points = KNOWLEDGE_POINTS[category]
            return [f"{category}-{p}" for p in points]
        except:
            print("❌ 无效选择")
            return []
    
    elif choice == "3":
        show_knowledge_points()
        custom = input("\n输入知识点（用逗号分隔）: ").strip()
        return [p.strip() for p in custom.split(',')]
    
    return []

def select_api():
    """Select API type"""
    print("\n🤖 选择AI服务：")
    print("1. Google Gemini (推荐，有免费额度)")
    print("2. OpenAI GPT")
    print("3. Anthropic Claude")
    print("4. Ollama (本地，免费)")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    api_map = {
        "1": "gemini",
        "2": "openai",
        "3": "anthropic",
        "4": "ollama"
    }
    
    return api_map.get(choice, "gemini")

def main():
    """Interactive main function"""
    print("="*60)
    print("🎓 小学6年级奥数题生成器 - 交互式界面")
    print("="*60)
    
    # Select knowledge points
    knowledge_points = select_knowledge_points()
    
    if not knowledge_points:
        print("❌ 未选择知识点")
        return
    
    print(f"\n✅ 已选择 {len(knowledge_points)} 个知识点")
    
    # Select API
    api_type = select_api()
    
    # Get API key if needed
    api_key = None
    if api_type != "ollama":
        api_key = input(f"\n请输入 {api_type.upper()} API Key: ").strip()
        if not api_key:
            print("❌ 需要API Key")
            return
    
    # Select difficulty
    print("\n📊 选择难度：")
    print("1. 简单")
    print("2. 中等")
    print("3. 困难")
    
    diff_choice = input("\n请选择 (1-3, 默认2): ").strip() or "2"
    difficulty_map = {"1": "简单", "2": "中等", "3": "困难"}
    difficulty = difficulty_map.get(diff_choice, "中等")
    
    # Questions per point
    questions_per_point = input("\n每个知识点生成几题？(默认3): ").strip() or "3"
    try:
        questions_per_point = int(questions_per_point)
    except:
        questions_per_point = 3
    
    # Output file
    output_file = input("\n输出文件名 (默认: output/generated_questions.json): ").strip()
    if not output_file:
        output_file = "output/generated_questions.json"
    
    # Confirm
    print("\n" + "="*60)
    print("📋 生成配置：")
    print("="*60)
    print(f"知识点数量: {len(knowledge_points)}")
    print(f"AI服务: {api_type}")
    print(f"难度: {difficulty}")
    print(f"每个知识点: {questions_per_point} 题")
    print(f"总计: {len(knowledge_points) * questions_per_point} 题")
    print(f"输出文件: {output_file}")
    print("="*60)
    
    confirm = input("\n确认开始生成？(y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\n🚀 开始生成...\n")
        generate_questions_batch(
            knowledge_points=knowledge_points,
            api_type=api_type,
            api_key=api_key,
            difficulty=difficulty,
            questions_per_point=questions_per_point,
            output_file=output_file
        )
    else:
        print("❌ 已取消")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
