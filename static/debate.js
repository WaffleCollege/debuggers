// タイマー表示要素を取得
const minute = document.getElementById("minute");
const second = document.getElementById("second");

// テキスト入力フィールドを取得
const textInput = document.getElementById("textinput");

let count = 300;

// カウントダウンタイマー用変数
let countDownTimer;

// ゼロ埋め関数
function formatNumber(num) {
    return num.toString().padStart(2, "0");
}

// 表示を更新する関数
function updateDisplay(count) {
    const minuteCount = Math.floor(count / 60);
    const secondCount = count - (Math.floor(count / 60) * 60);
    minute.textContent = formatNumber(minuteCount);
    second.textContent = formatNumber(secondCount);
}

updateDisplay(0);

let timerRunning = false;

// 入力イベントリスナーを設定
textInput.addEventListener("input", () => {

    // もしタイマーが動作中なら、新しいタイマーを開始しない
    if (timerRunning) {
        return;  // すでにタイマーが動作しているので、何もしない
    }

    timerRunning = true;  // タイマーを開始する

    //一定時間おきに行いたい関数を宣言
    function countDown() {
        if(count > 0) {
            //countが0より大きい場合はcountを1ずつ減らす
            count--;
            //タイマー表示要素にcountの数値を表示
            updateDisplay(count)
        } else {
            console.log("タイマーが停止しました");
            clearInterval(countDownTimer);
            updateDisplay(0); // 最終表示を00:00にする
        }
    }
    

    // タイマーを開始
    countDownTimer = setInterval(countDown, 1000);
});