// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.

window.addEventListener('DOMContentLoaded', () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector)
    if (element) element.innerText = text
  }

  for (const type of ['chrome', 'node', 'electron']) {
    replaceText(`${type}-version`, process.versions[type])
  }


const Http = new XMLHttpRequest();
const url = 'http://localhost:5000/wea/forecast';
setInterval(function() {
  Http.open("GET", url);
  Http.send();
  Http.onreadystatechange = (e) => {
  if (Http.readyState === 4 && Http.status === 200) {
    const response = JSON.parse(Http.responseText);
    replaceText('temperature', response.current.temp);
    replaceText('hum', response.current.humidity);
    replaceText('clouds', response.current.clouds);
    replaceText('wea', response.weather[0].main);
  }
  }}, 300000);

    });