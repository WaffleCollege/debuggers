from flask import Blueprint, render_template,  request

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def feedback_page():
    feedback_type = request.form.get('feedback_type')

    if feedback_type == 'sweet':
        feedback_message = "とても素晴らしかったです！"
    elif feedback_type == 'spicy':
        feedback_message = "もっと工夫が必要です！"
    else:
        feedback_message = "フィードバックが選択されていません。"

    return render_template('feedback_detail.html', feedback_message=feedback_message)
