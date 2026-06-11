import pandas as pd
import matplotlib.pyplot as plt
import requests
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False

def main():
    user_input = input('请输入你想监控的代号 (如 CL=F, BDRY, AAPL):').upper().strip()
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{user_input}?range=1mo&interval=1d'
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0',
    }

    try:
        print(f'正在抓取{user_input}的相关数据')
        response = requests.get(url,headers=headers)

        #防御措施
        if response.status_code != 200:
            print('检查代号是否有误')
            return
        json_data = response.json()

        cf = clean_data(json_data)

        cd = calculate_data(cf)

        rd = risk_report(cd["price_change_pct"])

        print('\n --- 供应链核心资产分析报告 ---')
        print(f' 监控目标: {user_input}')
        print(f' 过去一个月最高采购价: ${cd['max_price']:.2f}')
        print(f" 过去一个月最低采购价: ${cd['min_price']:.2f}")
        print(f" 当前最新结算价: ${cd['latest_price']:.2f}")
        print(f" 月度价格波动幅度: {cd['price_change_pct']:.2f}%")
        print(f" 供应链风险评级: {rd}")
        print("---------------------------------")


        plt.figure(figsize=(10, 5))
        plt.plot(cf['Date'], cf['Close'], marker='o', color='g', linewidth=2)
        plt.title(f'Trend: {user_input}', fontsize=14)
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Price (USD)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

        plt.savefig('supply_trend.png',dpi=300,bbox_inches='tight',facecolor='white',format='png')
        plt.close()
        print("统计图表已成功更新并保存至本地: chart.png\n")
    except Exception as err:
        print(f'有错误{err}')

def clean_data(raw_data):
    try:
        timestamps = raw_data['chart']['result'][0]['timestamp']
        closes = raw_data["chart"]["result"][0]["indicators"]["quote"][0]["close"]

        df = pd.DataFrame({"Timestamp": timestamps, "Close": closes})
        df = df.dropna()

        df["Date"] = pd.to_datetime(df["Timestamp"], unit="s").dt.date
        return df
    except (KeyError, TypeError):
        raise ValueError('输入的原始数据 JSON 结构不符合雅虎结构')

def calculate_data(cf):

    if cf.empty:
        return {"max_price": 0.0, "min_price": 0.0, "latest_price": 0.0, "price_change_pct": 0.0}

    max_p = float(cf["Close"].max())
    min_p = float(cf["Close"].min())
    latest_p = float(cf["Close"].iloc[-1])
    first_p = float(cf["Close"].iloc[0])

    change_pct = ((latest_p - first_p) / first_p) * 100

    return {
        "max_price": max_p,
        "min_price": min_p,
        "latest_price": latest_p,
        "price_change_pct": change_pct
    }


def risk_report(price_change_pct):
    if price_change_pct > 8.5:
        return "🔴 高风险 成本上涨，建议暂缓采购或寻找替代供应商"
    elif price_change_pct < -8.5:
        return "🟢 成本大跌 有利于降低供应链成本，建议分批加仓建立库存"
    else:
        return "🟡 风险稳定 价格在正常范围内良性波动，维持日常采购频率"


if __name__ == "__main__":
    main()
