// apple banana orange mango
// 10초
// 점수 1점씩

const wordDisplay = document.querySelector(".word-display")
const wordInput = document.querySelector(".word-input");
const score = document.querySelector(".score");
const time = document.querySelector(".time");
const DEFAULT_TIME = 5;
const start = document.querySelector(".start");
const reset = document.querySelector(".reset");
let timeInterval = "";

console.log(start);
console.log(reset);

function gameStart(){
	//reset 버튼은 보이게 하고 start 버튼은 안보이게
	start.style.display = "none";
	reset.style.display = "block";
	wordInput.disabled = false;
	fetch("https://random-word-api.herokuapp.com/word?number=10")
		.then(function(response){
			return response.json();
		})

		.then(function(result){
			// 단어 보여지게 하는 기능
			let wordList = result;
			let count = 0;
			let time_left = DEFAULT_TIME;

			wordDisplay.innerText = wordList[count];
			time.innerText = DEFAULT_TIME;

			console.dir(wordInput);
			// function onKeyDown(){
			// 	if (event.keyCode == 13){
			// 		alert("pressed");
			// 	}
			// }

		wordInput.addEventListener("keydown", function(){
			if (event.code === "Enter"){
				// 사용자 입력값 : wordInput.value
				// 보여지는 값 : wordDisplay.innerText or wordList[0]
				count++;
				if (wordDisplay.innerText === wordInput.value){
					if (count === wordList.length){
						//disabled 처리
						wordInput.disabled = true;
						clearInterval(timeInterval);
						return false;
					}
					wordDisplay.innerText = wordList[count];
					wordInput.value = "";
					score.innerText = count;
					time.innerText = DEFAULT_TIME;
					time_left = DEFAULT_TIME;
				}
			}
		})

		//setInterval (실행될 함수, 몇초)
		//js에서 제공하는 몇몇 함수값은 경우 비동기 가지고 활용

		timeInterval = setInterval(function(){
				time_left--;
				time.innerText = time_left;
				if (time_left == 0){
					wordInput.value = "";
					wordInput.disabled = true;
					clearInterval(timeInterval);
				}
		}, 1000)
	})
}

function gameReset(){
	wordDisplay.innerText = "";
	wordInput.value = "";
	start.style.display = "block";
	reset.style.display = "none"
	score.innerText = 0;
	time.innerText = 0;
	
}