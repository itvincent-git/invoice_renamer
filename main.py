import os
import re
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from PIL import Image
import argparse
import traceback
import numpy

def extract_text_from_file(file_path):
    """从PDF或JPG文件中提取文本内容"""
    # 初始化PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    
    text = ""
    if file_path.lower().endswith('.pdf'):
        # 将PDF转换为图像
        images = convert_from_path(file_path)
        for image in images:
            result = ocr.ocr(numpy.array(image))
            # 提取识别的文本
            if result[0]:
                for line in result[0]:
                    text += line[1][0] + "\n"
    else:  # 处理图片文件
        image = Image.open(file_path)
        result = ocr.ocr(numpy.array(image))
        # 提取识别的文本
        if result[0]:
            for line in result[0]:
                text += line[1][0] + "\n"
    
    return text

def extract_date(text):
    """提取开票日期"""
    # 匹配格式: 日期: 2025年03月15日 或类似格式
    date_pattern = r'日期[: ：]\s*(\d{4}年\d{2}月\d{2}日)'
    match = re.search(date_pattern, text)
    
    if match:
        date_str = match.group(1)
        print(f"开票日期: {date_str}")
        # 转换为YYYYMMDD格式
        date_str = date_str.replace('年', '').replace('月', '').replace('日', '')
        return date_str
    
    return None

def extract_amount(text):
    """提取金额"""
    # 匹配格式: (小写) 683.00 或类似格式
    amount_pattern = r'（小写）￥?¥?(\d+\.\d{2})'
    match = re.search(amount_pattern, text)
    print(f"匹配到的金额: {match}")
    
    if match:
        amount_str = match.group(1)
        print(f"金额: {amount_str}")
        # 移除逗号、空格并转换为浮点数
        amount_str = amount_str.replace(',', '').replace(' ', '')
        amount_float = float(amount_str)
        # 转换为整数（如果是整数金额）或保留两位小数
        if amount_float.is_integer():
            return str(int(amount_float))
        else:
            return f"{amount_float:.2f}"
    
    return None

def rename_invoice(file_path):
    """根据提取的信息复制发票文件到rename目录"""
    try:
        # 提取文本
        text = extract_text_from_file(file_path)

        print(f"提取的文本内容: {text}")
        # 打印一条长的分隔线
        print("=================================")
        
        # 提取日期和金额
        date = extract_date(text)
        amount = extract_amount(text)
        
        if not date or not amount:
            print(f"无法从文件 {file_path} 中提取必要信息。")
            if not date:
                print("未能识别到开票日期。")
            if not amount:
                print("未能识别到金额。")
            return False
        
        # 创建rename目录（如果不存在）
        rename_dir = os.path.join(os.path.dirname(file_path), 'rename')
        os.makedirs(rename_dir, exist_ok=True)
        
        # 获取原文件扩展名
        _, ext = os.path.splitext(file_path)
        
        # 构建新文件名和路径
        new_filename = f"{date}_{amount}元{ext}"
        new_filepath = os.path.join(rename_dir, new_filename)
        
        # 复制文件
        import shutil
        shutil.copy2(file_path, new_filepath)
        print(f"文件已复制到: {new_filepath}")
        return True
    
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        print(traceback.format_exc())
        return False

def process_directory(directory_path):
    """递归处理目录及其子目录中的所有PDF和JPG文件"""
    success_count = 0
    failed_count = 0
    
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.lower().endswith(('.pdf', '.jpg', '.jpeg')):
                file_path = os.path.join(root, filename)
                print(f"\n---->处理文件: {file_path}")
                print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
                
                if rename_invoice(file_path):
                    success_count += 1
                else:
                    failed_count += 1
    
    print("\n处理完成统计:")
    print(f"成功处理: {success_count} 个文件")
    print(f"处理失败: {failed_count} 个文件")
    print(f"总计文件: {success_count + failed_count} 个")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='发票PDF/JPG重命名工具')
    parser.add_argument('path', help='发票文件路径或文件夹路径 (支持PDF和JPG格式)')
    args = parser.parse_args()
    
    if os.path.isdir(args.path):
        process_directory(args.path)
    else:
        rename_invoice(args.path)

if __name__ == "__main__":
    main()