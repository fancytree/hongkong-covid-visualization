import pandas as pd
import json
import numpy as np
from datetime import datetime

def generate_data():
    try:
        # 读取Excel文件
        df = pd.read_excel('香港各区疫情数据_20250322.xlsx')
        
        # 确保日期列是datetime类型
        df['报告日期'] = pd.to_datetime(df['报告日期'])
        
        # 1. 处理日期和病例数据
        daily_stats = df.groupby('报告日期').agg({
            '新增确诊': 'sum',
            '累计确诊': 'sum',
            '新增康复': 'sum',
            '累计康复': 'sum',
            '新增死亡': 'sum',
            '累计死亡': 'sum'
        }).reset_index()
        
        # 2. 处理各区数据
        latest_date = df['报告日期'].max()
        latest_district_stats = df[df['报告日期'] == latest_date].groupby('地区名称').agg({
            '累计确诊': 'sum',
            '现存确诊': 'sum',
            '人口': 'first',
            '风险等级': 'first'
        }).reset_index()
        
        # 3. 处理风险等级数据
        risk_stats = latest_district_stats['风险等级'].value_counts()
        
        # 4. 计算发病率
        latest_district_stats['发病率'] = (latest_district_stats['累计确诊'] / latest_district_stats['人口']) * 100000
        
        # 准备数据（确保所有数值都转换为原生Python类型）
        data = {
            'dates': daily_stats['报告日期'].dt.strftime('%Y-%m-%d').tolist(),
            'newCases': [int(x) for x in daily_stats['新增确诊'].tolist()],
            'totalCases': [int(x) for x in daily_stats['累计确诊'].tolist()],
            'newRecovered': [int(x) for x in daily_stats['新增康复'].tolist()],
            'totalRecovered': [int(x) for x in daily_stats['累计康复'].tolist()],
            'newDeaths': [int(x) for x in daily_stats['新增死亡'].tolist()],
            'totalDeaths': [int(x) for x in daily_stats['累计死亡'].tolist()],
            'districts': latest_district_stats['地区名称'].tolist(),
            'districtCases': [
                {
                    'name': row['地区名称'],
                    'value': int(row['累计确诊']),
                    'current': int(row['现存确诊']),
                    'population': int(row['人口']),
                    'rate': float(round(row['发病率'], 2)),
                    'risk': row['风险等级']
                }
                for _, row in latest_district_stats.iterrows()
            ],
            'riskLevels': [
                int(risk_stats.get('高风险', 0)),
                int(risk_stats.get('中风险', 0)),
                int(risk_stats.get('低风险', 0))
            ],
            'lastUpdate': latest_date.strftime('%Y-%m-%d')
        }
        
        # 保存为JSON文件
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("数据已成功生成并保存到 data.json")
        print(f"最后更新日期：{data['lastUpdate']}")
        print(f"总确诊病例：{data['totalCases'][-1]}")
        print(f"现存确诊病例：{sum(d['current'] for d in data['districtCases'])}")
        
    except FileNotFoundError:
        print("错误：找不到指定的Excel文件")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    generate_data() 