# AI Question Generation Guide
# AI生成小学6年级奥数题指南

## Overview / 概述

This system generates high-quality Grade 6 math competition questions using AI, replacing the poor-quality OCR extraction approach.

本系统使用AI生成高质量的小学6年级奥数题，替代质量较差的OCR提取方式。

## Features / 特点

✅ **36 Knowledge Points** - 6 categories, 36 specific topics
✅ **Multiple AI Services** - Gemini, OpenAI, Claude, or local Ollama
✅ **Quality Control** - Structured JSON output with detailed solutions
✅ **Batch Generation** - Generate hundreds of questions automatically
✅ **Interactive CLI** - Easy-to-use command-line interface

## Knowledge Points / 知识点

### 数论 (Number Theory)
- 质数与合数 (Primes and Composites)
- 因数与倍数 (Factors and Multiples)
- 最大公约数 (GCD)
- 最小公倍数 (LCM)
- 整除性质 (Divisibility)
- 余数问题 (Remainder Problems)

### 计算 (Computation)
- 四则运算 (Four Operations)
- 简便计算 (Simplified Calculation)
- 定义新运算 (Defined Operations)
- 循环小数 (Repeating Decimals)
- 分数计算 (Fraction Calculation)
- 百分数应用 (Percentage Applications)

### 几何 (Geometry)
- 周长与面积 (Perimeter and Area)
- 立体图形 (3D Shapes)
- 图形变换 (Transformations)
- 角度计算 (Angle Calculation)
- 相似与全等 (Similarity and Congruence)
- 勾股定理 (Pythagorean Theorem)

### 应用题 (Word Problems)
- 行程问题 (Distance-Rate-Time)
- 工程问题 (Work Problems)
- 浓度问题 (Concentration Problems)
- 利润问题 (Profit Problems)
- 年龄问题 (Age Problems)
- 鸡兔同笼 (Chickens and Rabbits)

### 组合 (Combinatorics)
- 排列组合 (Permutations and Combinations)
- 概率统计 (Probability and Statistics)
- 抽屉原理 (Pigeonhole Principle)
- 容斥原理 (Inclusion-Exclusion)
- 逻辑推理 (Logical Reasoning)
- 数字谜题 (Number Puzzles)

### 代数 (Algebra)
- 方程与不等式 (Equations and Inequalities)
- 比例问题 (Proportion Problems)
- 函数思想 (Function Concepts)
- 数列规律 (Sequence Patterns)
- 代数式化简 (Algebraic Simplification)
- 列方程解题 (Solving by Equations)

## Usage / 使用方法

### Method 1: Interactive CLI (Easiest) / 方法1：交互式界面（最简单）

```bash
python interactive_generator.py
```

Follow the prompts to:
1. Select knowledge points
2. Choose AI service
3. Set difficulty level
4. Generate questions

### Method 2: Python API / 方法2：Python API

```python
from generate_with_api import generate_questions_batch

# Generate 5 questions for each knowledge point
generate_questions_batch(
    knowledge_points=["数论-质数与合数", "应用题-行程问题"],
    api_type="gemini",
    api_key="your-api-key",
    difficulty="中等",
    questions_per_point=5,
    output_file="output/my_questions.json"
)
```

### Method 3: Manual Prompts / 方法3：手动提示词

```python
from generate_questions import generate_question_prompt

# Generate prompt
prompt = generate_question_prompt("数论-质数与合数", "中等")

# Copy prompt and paste into any AI chat
# AI will return structured JSON
```

## AI Service Options / AI服务选项

### 1. Google Gemini (Recommended / 推荐)
- ✅ Free tier available / 有免费额度
- ✅ Good Chinese support / 中文支持好
- ✅ Fast response / 响应快
- Get API key: https://makersuite.google.com/app/apikey

### 2. OpenAI GPT
- ✅ High quality / 质量高
- ❌ Paid only / 仅付费
- Get API key: https://platform.openai.com/api-keys

### 3. Anthropic Claude
- ✅ Excellent reasoning / 推理能力强
- ❌ Paid only / 仅付费
- Get API key: https://console.anthropic.com/

### 4. Ollama (Local / 本地)
- ✅ Completely free / 完全免费
- ✅ No API key needed / 无需API密钥
- ✅ Privacy / 隐私保护
- ❌ Requires local setup / 需要本地安装
- Install: https://ollama.ai/

## Output Format / 输出格式

Each generated question follows this structure:

```json
{
  "题号": 1,
  "题目": "小明从家到学校，如果每分钟走60米，需要15分钟；如果每分钟走75米，需要多少分钟？",
  "选项": [
    "A. 10分钟",
    "B. 12分钟",
    "C. 14分钟",
    "D. 16分钟"
  ],
  "答案": "B. 12分钟",
  "解析": "首先计算距离：60×15=900米。然后计算时间：900÷75=12分钟。",
  "知识点": "应用题-行程问题",
  "难度": "中等",
  "题型": "选择题",
  "生成时间": "2026-03-12 17:00:00"
}
```

## Batch Generation Examples / 批量生成示例

### Generate 100 questions across all topics / 生成100题覆盖所有知识点

```python
from generate_questions import get_all_knowledge_points
from generate_with_api import generate_questions_batch

all_points = get_all_knowledge_points()  # 36 knowledge points

generate_questions_batch(
    knowledge_points=all_points,
    api_type="gemini",
    api_key="your-key",
    difficulty="中等",
    questions_per_point=3,  # 36 × 3 = 108 questions
    output_file="output/complete_question_bank.json"
)
```

### Generate by difficulty level / 按难度生成

```python
# Easy questions for practice
generate_questions_batch(
    knowledge_points=["数论-质数与合数"],
    difficulty="简单",
    questions_per_point=10
)

# Hard questions for competition
generate_questions_batch(
    knowledge_points=["组合-逻辑推理"],
    difficulty="困难",
    questions_per_point=5
)
```

## Quality Comparison / 质量对比

### OCR Extraction (Old Method) / OCR提取（旧方法）
- ❌ Poor quality / 质量差
- ❌ OCR errors / OCR错误
- ❌ Incomplete formulas / 公式不完整
- ❌ Manual cleanup needed / 需要手动清理
- ✅ Real exam questions / 真实考题

### AI Generation (New Method) / AI生成（新方法）
- ✅ High quality / 质量高
- ✅ Perfect formatting / 格式完美
- ✅ Detailed solutions / 详细解析
- ✅ Customizable / 可定制
- ✅ Unlimited quantity / 数量无限

## Cost Estimation / 成本估算

### Gemini (Free Tier)
- 60 requests/minute
- ~1500 requests/day
- Can generate ~500 questions/day for free

### OpenAI GPT-3.5
- ~$0.002 per question
- 1000 questions = ~$2

### Ollama (Local)
- $0 (completely free)
- Unlimited questions
- Requires GPU for best performance

## Tips / 使用技巧

1. **Start small** - Generate 10-20 questions first to test quality
2. **Review samples** - Check a few questions before batch generation
3. **Mix difficulties** - Generate easy, medium, and hard questions
4. **Save regularly** - Questions are appended to JSON file automatically
5. **Use local LLM** - For unlimited free generation with Ollama

## Troubleshooting / 故障排除

### API Key Error
- Check API key is correct
- Verify API service is enabled
- Check account has credits

### JSON Parse Error
- AI response may not be valid JSON
- Try regenerating the question
- Check prompt format

### Rate Limit Error
- Add delays between requests (already implemented)
- Use free tier limits wisely
- Consider using Ollama for unlimited generation

## Next Steps / 下一步

1. Generate a small test batch (10 questions)
2. Review quality and adjust prompts if needed
3. Generate full question bank (100-500 questions)
4. Organize by topic and difficulty
5. Create practice sets and exams

## Files / 文件说明

- `generate_questions.py` - Core generator with knowledge points
- `generate_with_api.py` - API integration for batch generation
- `interactive_generator.py` - Interactive CLI interface
- `output/generated_questions.json` - Generated questions database

---

**Ready to generate high-quality math questions!** 🎓
