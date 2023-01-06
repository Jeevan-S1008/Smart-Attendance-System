
var datetime = new Date().toLocaleTimeString();
console.log(datetime); // it will represent date in the console of developers tool
document.getElementById("time").textContent = datetime;

var datetime = new Date().toDateString();
console.log(datetime); // it will represent date in the console of developer tool
document.getElementById("date").textContent = datetime;