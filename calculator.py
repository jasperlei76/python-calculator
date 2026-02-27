# -*- coding: utf-8 -*-
"""
简易命令行计算器（优化版）
核心优化点：
1. 支持循环计算，无需重复运行程序
2. 兼容运算符首尾空格（如输入" + "仍可识别）
3. 捕获所有可能的异常，避免终端原生报错
4. 增加退出机制，支持手动输入指令退出
5. 优化用户交互提示，更友好的输入引导
"""

# 导入sys库，用于安全退出程序（可选，也可使用return）
import sys

def get_valid_number(prompt):
    """
    封装数字输入校验逻辑，复用性更高
    :param prompt: str - 输入提示文本（如"请输入第一个数字："）
    :return: float - 校验通过的数字；None - 用户终止输入/输入无效且选择退出
    """
    while True:  # 循环直到输入有效数字或用户选择退出
        try:
            # 获取用户输入并去除首尾空格（避免空输入/空格干扰）
            user_input = input(prompt).strip()
            
            # 支持退出指令：输入q/Q/退出 直接返回None，触发程序退出逻辑
            if user_input.lower() in ["q", "quit", "exit", "退出"]:
                print("👋 你选择退出数字输入，程序即将结束！")
                return None
            
            # 尝试转换为浮点型，支持整数/小数/科学计数法（如1e3、2.5）
            number = float(user_input)
            return number
        
        # 捕获数字转换失败的异常（如输入abc、1.2.3等）
        except ValueError:
            print("❌ 错误：请输入有效的数字（支持整数/小数）！输入q可退出程序")
        # 捕获用户手动终止输入的异常（Ctrl+C）
        except KeyboardInterrupt:
            print("\n⚠️ 你手动终止了输入，程序即将结束！")
            return None

def get_valid_operator():
    """
    封装运算符输入校验逻辑，兼容空格，支持退出
    :return: str - 校验通过的运算符（+/-/*/）；None - 用户终止输入/选择退出
    """
    # 定义合法运算符白名单
    valid_operators = ["+", "-", "*", "/"]
    
    while True:
        try:
            # 获取输入并去除首尾空格（解决" + "被判定为无效的问题）
            op = input("请输入运算符（+、-、*、/），输入q可退出：").strip()
            
            # 支持退出指令
            if op.lower() in ["q", "quit", "exit", "退出"]:
                print("👋 你选择退出，程序即将结束！")
                return None
            
            # 校验运算符是否合法
            if op in valid_operators:
                return op
            else:
                print(f"❌ 错误：无效的运算符！仅支持 {valid_operators}")
        
        # 捕获用户手动终止输入的异常
        except KeyboardInterrupt:
            print("\n⚠️ 你手动终止了输入，程序即将结束！")
            return None

def calculate(num1, op, num2):
    """
    封装运算逻辑，处理除数为0的边界情况
    :param num1: float - 第一个数字
    :param op: str - 运算符
    :param num2: float - 第二个数字
    :return: float/str - 运算结果（成功）；错误提示（失败，如除数为0）
    """
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        # 除数不能为0，增加浮点数精度容错（避免0.0000001被误判）
        if abs(num2) < 1e-9:  # 绝对值小于10的-9次方，判定为0
            return "❌ 错误：除数不能为0！"
        return num1 / num2

def main_calculator():
    """
    计算器主函数：整合所有功能，实现循环计算
    """
    print("=" * 30)
    print("     简易命令行计算器（优化版）")
    print("📌 支持 + - * / 运算，输入q可随时退出")
    print("=" * 30)
    
    while True:  # 循环计算，直到用户主动退出
        # 1. 获取第一个数字
        num1 = get_valid_number("请输入第一个数字：")
        if num1 is None:  # 用户选择退出/终止输入
            break
        
        # 2. 获取合法运算符
        op = get_valid_operator()
        if op is None:  # 用户选择退出/终止输入
            break
        
        # 3. 获取第二个数字
        num2 = get_valid_number("请输入第二个数字：")
        if num2 is None:  # 用户选择退出/终止输入
            break
        
        # 4. 执行运算并输出结果
        result = calculate(num1, op, num2)
        # 格式化输出，整数结果显示为整数，小数保留6位（避免10.0显示为10.0）
        if isinstance(result, float):
            # 判断是否为整数（如10.0 → 10）
            if result.is_integer():
                result = int(result)
            else:
                # 小数保留6位有效数字，避免过长
                result = round(result, 6)
        
        # 输出最终结果
        print(f"\n✅ 计算结果：{num1} {op} {num2} = {result}\n")
        
        # 5. 询问是否继续计算
        try:
            continue_choice = input("是否继续计算？(y/n，默认y)：").strip().lower()
            # 仅当输入n/no/否 时退出循环，其他情况（空/yes/y）继续
            if continue_choice in ["n", "no", "否"]:
                print("👋 感谢使用计算器，再见！")
                break
        except KeyboardInterrupt:
            print("\n⚠️ 你手动终止了操作，程序即将结束！")
            break

# 程序入口：仅当脚本直接运行时执行
if __name__ == "__main__":
    try:
        main_calculator()
    # 捕获所有未预期的异常（兜底，避免终端报错）
    except Exception as e:
        print(f"\n❌ 程序发生未预期错误：{str(e)}")
    finally:
        # 无论是否异常，最终输出退出提示
        sys.exit(0)