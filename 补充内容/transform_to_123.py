"""
数字黑洞游戏:
这段代码实现了一个数字转换程序。给定一个自然数,程序会统计其中偶数位、奇数位和总位数,
并按"偶-奇-总"顺序组成新数字。重复此过程直到得到数字123,同时打印每一步的转换结果。
"""

def count_digits(n):
    """
    统计数字n中的偶数位数、奇数位数和总位数，并按照“偶-奇-总”的顺序生成新数。
    """
    even = 0
    odd = 0
    total = 0
    for digit in str(n):
        if digit.isdigit():
            d = int(digit)
            if d % 2 == 0:
                even += 1
            else:
                odd += 1
            total += 1
    new_number = int(f"{even}{odd}{total}")
    return new_number

def transform_to_123(n):
    """
    对输入的自然数n重复执行“偶-奇-总”转换，直到结果为123。
    打印每一步的转换过程。
    """
    seen = set()
    current = n
    print(f"初始数: {current}")
    while current != 123:
        if current in seen:
            print("检测到循环，无法收敛到123。")
            return
        seen.add(current)
        current = count_digits(current)
        print(f"转换后: {current}")
    print("最终结果: 123")

if __name__ == "__main__":
    try:
        input_number = int(input("请输入一个自然数: "))
        if input_number <= 0:
            raise ValueError
        transform_to_123(input_number)
    except ValueError:
        print("请输入一个有效的自然数（正整数）。")
