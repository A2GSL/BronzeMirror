from flask import Flask, render_template_string, request
import sys
sys.path.append("../scripts")
from infer_risk import infer_risk

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>历史决策风险智能原型</title>
</head>
<body>
    <h2>历史决策风险智能原型</h2>
    <form method="post">
        <label>核心团队流失率（如0.7）：<input name="core_team_loss" type="number" step="0.01" required></label><br><br>
        <label>权力比值（如1.8）：<input name="power_ratio" type="number" step="0.01" required></label><br><br>
        <input type="submit" value="推理并获取建议">
    </form>
    {% if risk %}
    <h3>推理结果</h3>
    <b>风险等级：</b>{{ risk }}<br>
    <b>建议：</b>{{ advice }}
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    risk = advice = None
    if request.method == 'POST':
        core_team_loss = float(request.form['core_team_loss'])
        power_ratio = float(request.form['power_ratio'])
        risk, advice = infer_risk(core_team_loss, power_ratio)
    return render_template_string(HTML, risk=risk, advice=advice)

if __name__ == '__main__':
    app.run(debug=True)
