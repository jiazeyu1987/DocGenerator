import re

def is_safe_filename_old(filename: str) -> bool:
    """旧版本验证函数"""
    if not filename:
        return False
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', filename))

def is_safe_filename_new(filename: str) -> bool:
    """新版本验证函数"""
    if not filename:
        return False

    # 检查路径遍历攻击
    if '..' in filename or '/' in filename or '\\' in filename:
        return False

    # 检查文件名不以点开头（隐藏文件）
    if filename.startswith('.'):
        return False

    # 检查非法字符
    illegal_chars = '<>:"|?*\0'
    if any(char in filename for char in illegal_chars):
        return False

    # 检查文件名长度
    if len(filename) > 255:
        return False

    return True

# 测试文件名
test_filenames = [
    'HEM_Analyzer_专利交底书.md',
    'test.md',
    'test-file.md',
    '../../../etc/passwd',
    'test<script>.md',
    '.hidden.md',
    'normal_中文测试.md'
]

print("文件名验证测试:")
print("=" * 50)
for filename in test_filenames:
    old_result = is_safe_filename_old(filename)
    new_result = is_safe_filename_new(filename)
    print(f"文件名: {filename}")
    print(f"  旧版本: {'✓' if old_result else '✗'}")
    print(f"  新版本: {'✓' if new_result else '✗'}")
    print()