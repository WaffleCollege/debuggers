
// 勝敗と評価を表示する関数
async function showDebateResult() {
    const resultElement = document.getElementById("debate-result");
    const evaluationButtons = document.getElementById("evaluation-buttons");
    const mildButton = document.getElementById("mild-evaluation");
    const harshButton = document.getElementById("harsh-evaluation");

    // ローディング表示
    resultElement.textContent = "結果を判定中...";
    resultElement.style.display = "block";

    // ディベートデータを仮に設定（実際にはサーバー側から受け取る）
    const debateData = {
        debateContent: "ディベートの内容をサーバーに送信します。",
    };

    try {
        // サーバーにリクエストを送信（Axiosを使用）
        const response = await axios.post('/api/getDebateResult', debateData);
        const result = response.data;

        // 勝敗を画面に表示
        resultElement.textContent = `勝者: ${result.winner}`;
        resultElement.style.backgroundColor = result.winner === "AI" ? "#FFDD57" : "#FF6F61";

        // ボタンを表示して評価を確認できるようにする
        evaluationButtons.style.display = "block";

        // ボタンのクリックイベントを設定
        mildButton.onclick = () => displayEvaluation(result.mildEvaluation, "甘口");
        harshButton.onclick = () => displayEvaluation(result.harshEvaluation, "辛口");
    } catch (error) {
        console.error("エラー:", error);
        resultElement.textContent = "エラーが発生しました。もう一度試してください。";
    }
}

// 評価をモーダル形式で表示する関数
function displayEvaluation(evaluation, type) {
    alert(`${type}の評価:\n${evaluation}`);
}

// ディベート終了後、3秒で結果を表示
setTimeout(showDebateResult, 3000);
