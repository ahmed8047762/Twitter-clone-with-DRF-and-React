function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

export function backendLookup(method, endpoint, callback, data) {
  let jsonData;
  if (data) {
    jsonData = JSON.stringify(data) 
  }
  const xhr = new XMLHttpRequest()
  // Check if endpoint contains query parameters
  const hasParams = endpoint.includes('?')
  const url = `http://localhost:8000/api/${endpoint}${hasParams ? '' : '/'}`
  const responseType = "json"

  xhr.responseType = responseType
  xhr.open(method, url)
  const csrftoken = getCookie('csrftoken');
  xhr.setRequestHeader("Content-Type", "application/json")

  if (csrftoken) {
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
  }
  xhr.onload = function () {
      callback(xhr.response, xhr.status)
  }
  xhr.onerror = function (e) {
    console.log(e)
    callback({"message": "error"}, xhr.status)
  }
  console.log(jsonData)
  xhr.send(jsonData)
}