import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib as mpl

def calculate_daily_cases():
    try:
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 设置中文字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
        # 读取Excel文件
        df = pd.read_excel('香港各区疫情数据_20250322.xlsx')
        
        # 按日期分组，计算每日新增确诊和累计确诊
        daily_stats = df.groupby('报告日期').agg({
            '新增确诊': 'sum',
            '累计确诊': 'sum'
        }).reset_index()
        
        # 计算每日累计确诊
        daily_stats['累计确诊'] = daily_stats['新增确诊'].cumsum()
        
        # 打印结果
        print("\n每日疫情数据统计：")
        print(daily_stats)
        
        # 绘制图表
        plt.figure(figsize=(15, 8))
        
        # 绘制新增确诊折线图
        plt.plot(daily_stats['报告日期'], daily_stats['新增确诊'], 
                color='red', linewidth=2, label='新增确诊', marker='o', markersize=4)
        
        # 绘制累计确诊折线图
        plt.plot(daily_stats['报告日期'], daily_stats['累计确诊'], 
                 color='blue', linewidth=2, label='累计确诊', marker='s', markersize=4)
        
        # 设置图表属性
        plt.title('香港每日新增确诊与累计确诊趋势', fontsize=14, pad=20)
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('病例数', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        plt.savefig('daily_cases_trend.png', dpi=300, bbox_inches='tight')
        print("\n图表已保存为 daily_cases_trend.png")
        
        # 显示一些统计信息
        print("\n统计摘要：")
        print(f"总新增确诊数：{daily_stats['新增确诊'].sum()}")
        print(f"最高单日新增：{daily_stats['新增确诊'].max()}")
        print(f"平均每日新增：{daily_stats['新增确诊'].mean():.2f}")
        
    except FileNotFoundError:
        print("错误：找不到指定的Excel文件")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    calculate_daily_cases() 