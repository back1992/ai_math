"""
Interactive tool to review and clean OCR errors in extracted questions
"""
import json
import re

def load_questions(json_path='output/beijing_math_all_questions.json'):
    """Load extracted questions"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_questions(data, json_path='output/beijing_math_cleaned.json'):
    """Save cleaned questions"""
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved to {json_path}")

def detect_ocr_issues(text):
    """Detect common OCR errors"""
    issues = []
    
    # Common OCR errors
    if '了' in text and len(text) < 50:
        issues.append("Possible '了' misread")
    if '〈' in text or '〉' in text:
        issues.append("Angle brackets (should be parentheses)")
    if re.search(r'[A-Z]，', text):
        issues.append("Chinese comma after English letter")
    if re.search(r'\d+[xX]\d+', text):
        issues.append("Multiplication symbol (x vs ×)")
    if '。 )' in text or '( 。 )' in text:
        issues.append("Period inside parentheses")
    
    return issues

def auto_fix_common_errors(text):
    """Automatically fix common OCR errors"""
    # Fix angle brackets
    text = text.replace('〈', '(').replace('〉', ')')
    
    # Fix Chinese comma after English letters
    text = re.sub(r'([A-Z])，', r'\1.', text)
    
    # Fix period in parentheses
    text = text.replace('( 。 )', '( )')
    text = text.replace('。 )', ')')
    
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def generate_review_report(data):
    """Generate a review report of all questions"""
    report = []
    issues_count = 0
    
    for page in data:
        if not page['questions']:
            continue
        
        for q in page['questions']:
            content = q['content']
            issues = detect_ocr_issues(content)
            
            if issues:
                issues_count += 1
                report.append({
                    'page': page['page'],
                    'question_num': q['number'],
                    'content': content[:100],
                    'issues': issues
                })
    
    return report, issues_count

def auto_clean_all(data):
    """Automatically clean all questions"""
    cleaned_count = 0
    
    for page in data:
        for q in page['questions']:
            original = q['content']
            cleaned = auto_fix_common_errors(original)
            
            if original != cleaned:
                q['content'] = cleaned
                cleaned_count += 1
    
    return cleaned_count

def show_statistics(data):
    """Show data statistics"""
    total_pages = len(data)
    pages_with_q = sum(1 for p in data if p['questions'])
    total_q = sum(len(p['questions']) for p in data)
    
    print(f"\n📊 Statistics:")
    print(f"  Total pages: {total_pages}")
    print(f"  Pages with questions: {pages_with_q}")
    print(f"  Total questions: {total_q}")
    print(f"  Avg questions/page: {total_q/pages_with_q:.1f}")

def main():
    """Main review and cleanup workflow"""
    print("🔍 Beijing Math Questions - Review & Cleanup Tool\n")
    
    # Load data
    data = load_questions()
    show_statistics(data)
    
    # Generate review report
    print("\n📋 Analyzing OCR issues...")
    report, issues_count = generate_review_report(data)
    
    print(f"\n⚠️  Found {issues_count} questions with potential OCR issues")
    
    # Show sample issues
    if report:
        print(f"\n🔍 Sample issues (first 10):")
        for item in report[:10]:
            print(f"\n  Page {item['page']}, Q{item['question_num']}:")
            print(f"    Content: {item['content']}...")
            print(f"    Issues: {', '.join(item['issues'])}")
    
    # Auto-clean
    print(f"\n🔧 Auto-fixing common errors...")
    cleaned_count = auto_clean_all(data)
    print(f"  ✅ Auto-fixed {cleaned_count} questions")
    
    # Save cleaned version
    save_questions(data)
    
    # Re-analyze
    print(f"\n📋 Re-analyzing after cleanup...")
    report2, issues_count2 = generate_review_report(data)
    print(f"  Remaining issues: {issues_count2}")
    print(f"  Improvement: {issues_count - issues_count2} issues fixed")
    
    # Export issues for manual review
    if report2:
        with open('output/manual_review_needed.json', 'w', encoding='utf-8') as f:
            json.dump(report2, f, ensure_ascii=False, indent=2)
        print(f"\n📝 Exported {len(report2)} items needing manual review")
        print(f"  See: output/manual_review_needed.json")

if __name__ == "__main__":
    main()
