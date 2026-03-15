"""
.ipynb 파일 첫 번째 셀의 개인정보(학과/학번/이름)를 제거하는 스크립트
사용법: python remove_personal_info.py
"""

import json
import os
import glob
import re

# ✅ 처리할 폴더 경로 (필요시 수정)
TARGET_FOLDER = os.path.expanduser("~/Downloads")

# 개인정보 패턴 (학과, 학번, 이름으로 시작하는 줄)
PERSONAL_INFO_PATTERNS = [
    r"^#+\s*학과[:：].*",
    r"^#+\s*학번[:：].*",
    r"^#+\s*이름[:：].*",
]

def is_personal_info_line(line: str) -> bool:
    """해당 줄이 개인정보 줄인지 확인"""
    stripped = line.strip().rstrip("\\n").strip()
    return any(re.match(pattern, stripped) for pattern in PERSONAL_INFO_PATTERNS)

def remove_personal_info_from_cell(source: list) -> list:
    """셀 source에서 개인정보 줄만 제거"""
    return [line for line in source if not is_personal_info_line(line)]

def process_notebook(filepath: str) -> bool:
    """노트북 파일에서 개인정보 제거. 변경 있으면 True 반환"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        notebook = json.load(f)

    changed = False
    cells = notebook.get("cells", [])

    for cell in cells:
        if cell.get("cell_type") == "markdown":
            original = cell["source"]
            cleaned = remove_personal_info_from_cell(original)

            # 빈 줄만 남은 경우도 정리
            cleaned = [line for line in cleaned if line.strip() not in ("", "\\n")]

            if cleaned != original:
                cell["source"] = cleaned
                changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(notebook, f, ensure_ascii=False, indent=2)

    return changed

def main():
    pattern = os.path.join(TARGET_FOLDER, "**", "*.ipynb")
    files = glob.glob(pattern, recursive=True)

    if not files:
        print(f"[!] '{TARGET_FOLDER}' 에서 .ipynb 파일을 찾을 수 없습니다.")
        return

    print(f"[*] 총 {len(files)}개 파일 발견\n")

    modified = 0
    for filepath in files:
        filename = os.path.basename(filepath)
        changed = process_notebook(filepath)
        if changed:
            print(f"  ✅ 수정됨: {filename}")
            modified += 1
        else:
            print(f"  ⏭️  변경 없음: {filename}")

    print(f"\n[완료] {modified}/{len(files)}개 파일 수정됨")

if __name__ == "__main__":
    main()
