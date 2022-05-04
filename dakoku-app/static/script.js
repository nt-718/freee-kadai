setInterval(setClock, 1000);
setInterval(setDigital, 1000);

const hourHand = document.querySelector("[data-hour-hand]");
const minuteHand = document.querySelector("[data-minute-hand]");
const secondHand = document.querySelector("[data-second-hand]");
const digital = document.querySelector(".digital");

function setClock() {
  const currentDate = new Date();
  const secondsRatio = currentDate.getSeconds() / 60;
  const minutesRatio = (secondsRatio + currentDate.getMinutes()) / 60;
  const hoursRatio = (minutesRatio + currentDate.getHours()) / 12;
  setRotation(secondHand, secondsRatio);
  setRotation(minuteHand, minutesRatio);
  setRotation(hourHand, hoursRatio);
}

function setDigital() {
  const time = new Date();
  let hours = time.getHours();
  let minutes = time.getMinutes();
  let seconds = time.getSeconds();
  if (hours < 10) hours = `0${hours}`;
  if (minutes < 10) minutes = `0${minutes}`;
  if (seconds < 10) seconds = `0${seconds}`;
  digital.innerHTML = `<span class="hours">${hours}</span> :
                      <span class="minutes">${minutes}</span> :
                      <span class="seconds">${seconds}</span>`;
}

function setRotation(element, rotationRatio) {
  element.style.setProperty("--rotation", rotationRatio * 360);
}
setDigital();
setClock();
