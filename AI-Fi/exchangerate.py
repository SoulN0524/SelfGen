from flask import Flask, render_template, request, jsonify
import json
import time
import random
import plotly
import plotly.graph_objects as go

def create_plot():
    df = plotly.data.stocks()
    data = [
        go.Scatter(
            x=df['date'],
            y=df['GOOG']
        )
    ]
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
            with open('LauGen-master\AI-Fi\static\message.json', 'r') as f:
                message_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            message_data = []
        
        if not isinstance(message_data, list):
            message_data = []
        
        message_data.append({'user': user_message, 'bot': bot_message, 'mode': mode})
        
        # 將更新後的消息寫回文件
        with open('LauGen-master\AI-Fi\static\message.json', 'w') as f:
            json.dump(message_data, f)
        
        return jsonify(botMessage=bot_message)

def generateRandomMessage(mode):
    investment_responses = [
        "這是一個很好的投資建議！",
        "投資有風險，請謹慎操作。",
        "這是一個不錯的投資機會。",
        "請告訴我更多關於您的投資目標。",
        "我建議您多了解市場趨勢。"
    ]
    
    travel_responses = [
        "這是一個很棒的旅遊建議！",
        "旅行能開闊視野，放鬆心情。",
        "這個地方很適合旅遊。",
        "請告訴我更多關於您的旅行計畫。",
        "旅遊時請注意安全和健康。"
    ]
    
    if mode == "投資":
        return random.choice(investment_responses)
    else:
        return random.choice(travel_responses)

if __name__ == '__main__':
    app.run(debug=True)
