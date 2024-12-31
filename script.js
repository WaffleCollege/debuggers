document.addEventListener("DOMContentLoaded", () => {
    // 要素の取得
    const resultScreen = document.getElementById("result-screen");
    const debateCompleteElement = document.getElementById("debate-complete");
    const winnerElement = document.getElementById("winner");
    const evaluationButtons = document.getElementById("evaluation-buttons");
    const evaluationContainer = document.getElementById("evaluation-container");
    const evaluationElement = document.getElementById("evaluation");
    const sweetEvaluationButton = document.getElementById("sweet-evaluation");
    const harshEvaluationButton = document.getElementById("harsh-evaluation");

    // 勝敗データ（仮）
    const winner = "AI"; // "AI" または "あなた"
    const sweetEvaluation = "良い議論でした！明確な論点で説得力がありました。";
    const harshEvaluation = "もう少し証拠を具体的に説明する必要があります。結論が弱い点が課題です。";

    // ディベート終了画面を表示
    resultScreen.classList.remove("hidden");
    debateCompleteElement.classList.remove("hidden");

    // 3秒後に「ディベート完了」から「勝者」に切り替え
    setTimeout(() => {
        debateCompleteElement.classList.add("hidden"); // ディベート完了を非表示
        winnerElement.textContent = `勝者: ${winner}`;
        winnerElement.classList.remove("hidden"); // 勝者を表示
        evaluationButtons.classList.remove("hidden"); // 評価ボタンを表示
    }, 3000);

    // 甘口評価ボタンの動作
    sweetEvaluationButton.addEventListener("click", () => {
        evaluationContainer.classList.remove("hidden");
        evaluationElement.innerHTML = `
            <p>評価タイプ: <strong>甘口</strong></p>
            <p>${sweetEvaluation}</p>
        `;
    });

    // 辛口評価ボタンの動作
    harshEvaluationButton.addEventListener("click", () => {
        evaluationContainer.classList.remove("hidden");
        evaluationElement.innerHTML = `
            <p>評価タイプ: <strong>辛口</strong></p>
            <p>${harshEvaluation}</p>
        `;
    });
});
