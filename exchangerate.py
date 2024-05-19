from flask import Flask, render_template, request, jsonify
import json
import time
import random
import plotly
import plotly.graph_objects as go


def create_plot():
    df = plotly.data.stocks()
    data = [go.Scatter(x=df['date'], y=df['GOOG'])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
@app.route('/templates/index.html')
def home():
    return render_template('index.html')


@app.route('/service03.html')
@app.route('/templates/service03.html')
def index():
    scatter_plot = create_plot()
    return render_template('service03.html', plot=scatter_plot)


@app.route('/service04.html')
@app.route('/templates/service04.html')
def chatBot():
    return render_template('service04.html')


@app.route('/chat/message', methods=['POST'])
def setChatMessage():
    if request.method == 'POST':
        user_message = request.form['message']
        mode = request.form['mode']
        time.sleep(1.5)
        bot_message = generateRandomMessage(mode)

        # 讀取現有的消息資料
        try:
            with open('message.json', 'r') as f:
                message_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            message_data = []

        if not isinstance(message_data, list):
            message_data = []

        message_data.append({
            'user': user_message,
            'bot': bot_message,
            'mode': mode
        })

        # 將更新後的消息寫回文件
        with open('message.json', 'w') as f:
            json.dump(message_data, f)

        return jsonify(botMessage=bot_message)


def generateRandomMessage(mode):
    #investment_responses = ["這是一個很好的投資建議！", "投資有風險，請謹慎操作。", "這是一個不錯的投資機會。", "請告訴我更多關於您的投資目標。","我建議您多了解市場趨勢。"]
    investment_responses = [
        "目前美元對歐元的走勢受到多種因素的影響，包括美國和歐元區的經濟數據、美聯儲和歐洲央行的貨幣政策、國際政治事件及市場情緒。美國的經濟數據若表現強勁，美聯儲加息可能性上升，會推動美元走強。而歐洲央行若維持寬鬆政策，歐元可能走弱。此外，國際貿易政策變化和地緣政治風險也會影響市場情緒，進而影響美元對歐元的匯率走勢。近期建議關注這些主要因素的變化，以更好預測匯率走勢。"
    ]

    #travel_responses = ["這是一個很棒的旅遊建議！", "旅行能開闊視野，放鬆心情。", "這個地方很適合旅遊。", "請告訴我更多關於您的旅行計畫。","旅遊時請注意安全和健康。"]
    travel_responses = [
        "目前，匯率最划算的國家通常是那些經濟穩定且旅遊成本較低的國家。根據近期的匯率趨勢，泰國的匯率相對較為有利。泰銖相對於其他主要貨幣較為穩定，且泰國的物價水平較低，這意味著您可以在當地獲得更多的購買力。此外，泰國的旅遊業發達，提供了多樣化的旅遊體驗和高品質的服務，讓您的旅遊支出更具價值。"
    ]

    if mode == "投資":
        return random.choice(investment_responses)
    else:
        return random.choice(travel_responses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
