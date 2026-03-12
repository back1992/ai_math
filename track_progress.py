"""
Progress tracking utility to avoid duplicate processing
"""
import json
import os
from datetime import datetime

PROGRESS_FILE = 'progress.json'

def load_progress():
    """Load progress tracking data"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "project": "ai_math_extraction",
        "total_pages": 90,
        "completed_pages": [],
        "in_progress_pages": [],
        "skipped_pages": [],
        "last_updated": "",
        "notes": {}
    }

def save_progress(progress_data):
    """Save progress tracking data"""
    progress_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Progress saved to {PROGRESS_FILE}")

def mark_completed(page_nums, note=""):
    """Mark pages as completed"""
    progress = load_progress()
    
    if isinstance(page_nums, int):
        page_nums = [page_nums]
    
    for page in page_nums:
        if page not in progress['completed_pages']:
            progress['completed_pages'].append(page)
        # Remove from in_progress if exists
        if page in progress['in_progress_pages']:
            progress['in_progress_pages'].remove(page)
    
    progress['completed_pages'].sort()
    
    if note:
        progress['notes'][f"pages_{min(page_nums)}_{max(page_nums)}"] = note
    
    save_progress(progress)
    print(f"✅ Marked pages {page_nums} as completed")

def mark_in_progress(page_nums):
    """Mark pages as in progress"""
    progress = load_progress()
    
    if isinstance(page_nums, int):
        page_nums = [page_nums]
    
    for page in page_nums:
        if page not in progress['in_progress_pages'] and page not in progress['completed_pages']:
            progress['in_progress_pages'].append(page)
    
    progress['in_progress_pages'].sort()
    save_progress(progress)
    print(f"🔄 Marked pages {page_nums} as in progress")

def mark_skipped(page_nums, reason=""):
    """Mark pages as skipped"""
    progress = load_progress()
    
    if isinstance(page_nums, int):
        page_nums = [page_nums]
    
    for page in page_nums:
        if page not in progress['skipped_pages']:
            progress['skipped_pages'].append(page)
    
    progress['skipped_pages'].sort()
    
    if reason:
        progress['notes'][f"skipped_{min(page_nums)}_{max(page_nums)}"] = reason
    
    save_progress(progress)
    print(f"⏭️  Marked pages {page_nums} as skipped")

def get_pending_pages():
    """Get list of pages that haven't been processed yet"""
    progress = load_progress()
    total = progress['total_pages']
    completed = set(progress['completed_pages'])
    skipped = set(progress['skipped_pages'])
    in_progress = set(progress['in_progress_pages'])
    
    processed = completed | skipped | in_progress
    pending = [p for p in range(1, total + 1) if p not in processed]
    
    return pending

def get_next_batch(batch_size=10):
    """Get next batch of pages to process"""
    pending = get_pending_pages()
    return pending[:batch_size]

def is_page_completed(page_num):
    """Check if a page has been completed"""
    progress = load_progress()
    return page_num in progress['completed_pages']

def show_status():
    """Display current progress status"""
    progress = load_progress()
    total = progress['total_pages']
    completed = len(progress['completed_pages'])
    skipped = len(progress['skipped_pages'])
    in_progress = len(progress['in_progress_pages'])
    pending = len(get_pending_pages())
    
    print("\n" + "="*50)
    print("📊 EXTRACTION PROGRESS STATUS")
    print("="*50)
    print(f"Total Pages:      {total}")
    print(f"✅ Completed:     {completed} pages {progress['completed_pages']}")
    print(f"🔄 In Progress:   {in_progress} pages {progress['in_progress_pages']}")
    print(f"⏭️  Skipped:       {skipped} pages {progress['skipped_pages']}")
    print(f"⏳ Pending:       {pending} pages")
    print(f"📈 Progress:      {((completed + skipped) / total * 100):.1f}%")
    print(f"🕐 Last Updated:  {progress['last_updated']}")
    print("="*50)
    
    if progress['notes']:
        print("\n📝 Notes:")
        for key, note in progress['notes'].items():
            print(f"  • {key}: {note}")
    
    print("\n🔜 Next batch to process:", get_next_batch(10))
    print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        show_status()
    else:
        command = sys.argv[1]
        
        if command == "status":
            show_status()
        elif command == "complete":
            pages = list(map(int, sys.argv[2].split(',')))
            note = sys.argv[3] if len(sys.argv) > 3 else ""
            mark_completed(pages, note)
        elif command == "skip":
            pages = list(map(int, sys.argv[2].split(',')))
            reason = sys.argv[3] if len(sys.argv) > 3 else ""
            mark_skipped(pages, reason)
        elif command == "next":
            batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            print(f"Next {batch_size} pages:", get_next_batch(batch_size))
        else:
            print("Usage:")
            print("  python track_progress.py status")
            print("  python track_progress.py complete 11,12,13 'note'")
            print("  python track_progress.py skip 1,2,3,4,5 'reason'")
            print("  python track_progress.py next [batch_size]")
