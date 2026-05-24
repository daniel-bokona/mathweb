document.getElementById("timePerQuestion").addEventListener("input", function () {
    document.getElementById("timeDisplay").innerText = this.value + " seconds";
});

document.getElementById("numQuestions").addEventListener("input", function () {
    document.getElementById("questionDisplay").innerText = this.value + " problems";
});

let num1, num2, correctAnswer, timer, timeLeft, currentQuestion, score, numQuestions;

function startGame() {
    document.getElementById("settings").classList.add("hidden");
    document.getElementById("quiz").classList.remove("hidden");

    score = 0;
    currentQuestion = 1;
    numQuestions = parseInt(document.getElementById("numQuestions").value);
    timeLeft = parseInt(document.getElementById("timePerQuestion").value);

    generateQuestion();
    startTimer();
}

function generateQuestion() {
    let operation = document.getElementById("operation").value;
    let difficulty = document.getElementById("difficulty").value;

    let range = difficulty === "easy" ? 10 : difficulty === "medium" ? 50 : 100;

    num1 = Math.floor(Math.random() * range) + 1;
    num2 = Math.floor(Math.random() * range) + 1;

    switch (operation) {
        case "addition":
            correctAnswer = num1 + num2;
            document.getElementById("question").innerText = `${num1} + ${num2} = ?`;
            break;
        case "subtraction":
            correctAnswer = num1 - num2;
            document.getElementById("question").innerText = `${num1} - ${num2} = ?`;
            break;
        case "multiplication":
            correctAnswer = num1 * num2;
            document.getElementById("question").innerText = `${num1} × ${num2} = ?`;
            break;
        case "division":
            num1 = num2 * Math.floor(Math.random() * 10) + 1;
            correctAnswer = num1 / num2;
            document.getElementById("question").innerText = `${num1} ÷ ${num2} = ?`;
            break;
    }
}

function startTimer() {
    document.getElementById("timeLeft").innerText = timeLeft;
    timer = setInterval(() => {
        timeLeft--;
        document.getElementById("timeLeft").innerText = timeLeft;

        if (timeLeft <= 0) {
            checkAnswer();
        }
    }, 1000);
}

function checkAnswer() {
    clearInterval(timer);

    let userAnswer = parseInt(document.getElementById("answer").value);
    if (userAnswer === correctAnswer) {
        score++;
        document.getElementById("feedback").innerText = "✅ Correct!";
    } else {
        document.getElementById("feedback").innerText = `❌ Wrong! The correct answer was ${correctAnswer}`;
    }

    document.getElementById("score").innerText = score;

    if (currentQuestion < numQuestions) {
        currentQuestion++;
        setTimeout(() => {
            document.getElementById("feedback").innerText = "";
            generateQuestion();
            startTimer();
        }, 1000);
    } else {
        endGame();
    }
}

function endGame() {
    document.getElementById("quiz").classList.add("hidden");
    document.getElementById("result").classList.remove("hidden");
    document.getElementById("finalScore").innerText = score;
}

document.getElementById("startButton").addEventListener("click", startGame);
document.getElementById("checkButton").addEventListener("click", checkAnswer);
document.getElementById("playAgain").addEventListener("click", () => location.reload());
