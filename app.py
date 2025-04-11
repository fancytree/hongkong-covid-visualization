from flask import Flask, render_template, jsonify
import pandas as pd
from datetime import datetime
import os
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def process_data():
    try:
        # 检查文件是否存在
        excel_file = '香港各区疫情数据_20250322.xlsx'
        if not os.path.exists(excel_file):
            logger.error(f"Excel文件不存在: {excel_file}")
            return None
            
        logger.info(f"开始读取Excel文件: {excel_file}")
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        logger.info(f"成功读取Excel文件，数据行数: {len(df)}")
        
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
            'lastUpdate': latest_date.strftime('%Y-%m-%d'),
            'activeCases': [int(x) for x in df.groupby('报告日期')['现存确诊'].sum().tolist()]
        }
        
        logger.info("数据处理完成")
        return data
        
    except Exception as e:
        logger.error(f"数据处理错误：{str(e)}", exc_info=True)
        return None

@app.route('/')
def index():
    try:
        logger.info("访问首页")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"渲染首页错误：{str(e)}", exc_info=True)
        return "服务器内部错误", 500

@app.route('/api/data')
def get_data():
    try:
        logger.info("请求数据API")
        data = process_data()
        if data:
            return jsonify(data)
        else:
            logger.error("数据处理失败")
            return jsonify({'error': '数据处理失败'}), 500
    except Exception as e:
        logger.error(f"API处理错误：{str(e)}", exc_info=True)
        return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    logger.info("启动Flask应用")
    app.run(debug=True, port=8000, host='0.0.0.0') 