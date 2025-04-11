import pandas as pd

def read_excel_file():
    try:
        # 读取Excel文件
        df = pd.read_excel('香港各区疫情数据_20250322.xlsx')
        
        # 显示所有字段名
        print("\n字段名列表：")
        print(df.columns.tolist())
        
        # 显示前20行数据
        print("\n前20行数据：")
        print(df.head(20))
        
    except FileNotFoundError:
        print("错误：找不到指定的Excel文件")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    read_excel_file() 