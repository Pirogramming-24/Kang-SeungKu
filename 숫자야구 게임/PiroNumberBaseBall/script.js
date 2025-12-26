// 변수 초기화
let attempts = 9;
const attemptsElement = document.getElementById("attempts");
attemptsElement.textContent = attempts

const answer = [];

// 정답이 될 랜덤 숫자 3개 지정
while (answer.length < 3) {
    ranNum = Math.floor(Math.random() * 10);
    if (!answer.includes(ranNum)) {
        answer.push(ranNum);
    }
    
}
console.log(answer);

const el1 = document.getElementById("number1");
const el2 = document.getElementById("number2");
const el3 = document.getElementById("number3");

// 숫자 초기화 기능
function clear_numbers() {
    el1.value = "";
    el2.value = "";
    el3.value = "";
}

// 야구게임 규칙
function check_numbers() {
    
    
    if (el1.value == "" || el2.value == "" || el3.value == "") {
        el1.value = "" ;
        el2.value = "" ;
        el3.value = "" ;
        return;
    }
    // console.log(el1.value, el2.value, el3.value);

    // 사용자가 입력한 값 -> 배열
    const userInput = [];
    userInput.push(Number(el1.value),Number(el2.value),Number(el3.value));

    // 게임시작
    let strike = 0;
    let ball = 0;

    
    for ( let i = 0 ; i < 3 ; i++) {
        // 위치와 값이 같으면 strike
        if (answer[i] === userInput[i]) {
            strike++;
        }
        // 위치는 다른데 값이 있으면 ball
        else if (answer.includes(userInput[i])) {
            ball++;
        }
        
    }

    
    const resultRow = document.createElement("div");
    resultRow.className = "check-result"; 
    
    resultRow.style.width = "100%"; 

    const leftSpan = document.createElement("span");
    leftSpan.className = "left"; 
    leftSpan.textContent = userInput.join(" ");

    const rightSpan = document.createElement("span");
    rightSpan.className = "right"; 

    if (strike === 0 && ball === 0) {
        // OUT
        const outSpan = document.createElement("span");
        outSpan.className = "num-result out"; 
        outSpan.textContent = "O";
        rightSpan.append(outSpan);
    } else {
        // Strike
        const strikeNum = document.createElement("span"); 
        strikeNum.textContent = `${strike} `;
        rightSpan.append(strikeNum)
        const sSpan = document.createElement("span");
        sSpan.className = "num-result strike";
        sSpan.textContent = "S";
        rightSpan.append(sSpan);

        // 공백
        rightSpan.append(" ");

        // Ball
        const ballNum = document.createElement("span"); 
        ballNum.textContent = `${ball} `;
        rightSpan.append(ballNum)
        const bSpan = document.createElement("span");
        bSpan.className = "num-result ball";
        bSpan.textContent = "B";
        rightSpan.append(bSpan);
    }

    resultRow.append(leftSpan);
    resultRow.append(":"); 
    resultRow.append(rightSpan);

    const resultsContainer = document.getElementById("results");
    resultsContainer.style.width = "100%";
    resultsContainer.append(resultRow);

    attempts -= 1;
    attemptsElement.textContent = attempts;

    // 결과 이미지 출력
    const img = document.getElementById("game-result-img");
    
    if (strike === 3) {
        img.src = "success.png";
        document.querySelector(".submit-button").disabled = true;
    } else if (attempts === 0) {
        img.src = "fail.png";
        document.querySelector(".submit-button").disabled = true;
    }

    // 확인 버튼 누르면 input clear
    clear_numbers();
}

// 전체 초기화 (홈페이지 새로고침)
function restart() {
    window.location.reload();
}
