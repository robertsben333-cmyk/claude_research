if (!Array.from) {
  Array.from = function (object) {
    'use strict';
    return [].slice.call(object);
  };
}


(function (MF) {
  "use strict";
  var nonce = document.currentScript && document.currentScript.nonce;

  MF.done_callback = MF.done_callback || function (token, elm) {
    if (!MF || !MF.data || !Array.isArray(MF.data)) {
      return;
    }
    MF.data.forEach(function (w) {
      if (w.done && token == w.token) {
        w.done(elm, token);
      }
    })
  }

  MF.push = function (widget) {
    if (Array.isArray(widget)) {
      widget.forEach(function (w2) {
        MF.push(w2)
      })
      return
    }
    if (!(document.getElementById(widget.id) || document.querySelector(widget.query))) {
	    return;
    }

    MF.data.push(widget)

    widget.callback = widget.callback || function (data) {
      return data
    };

    if (!widget.ready) {
      widget.ready = !widget.wait;
    }

    widget.render = function () {
      widget.ready = true;
      if (widget.data && widget.id) {
        document.getElementById(widget.id).innerHTML = widget.data;
        MF.setInnerHtml(widget, document.getElementById(widget.id), widget.data);
      }
      if (widget.data && widget.query) {
        document.querySelector(widget.query).innerHTML = widget.data;
        MF.setInnerHtml(widget, document.querySelector(widget.query), widget.data);
      }
    };

    if (!widget.widget || !widget.token) {
      console.log("widget and token must be set in window._MF to load widget", widget);
      return
    }

    var xhttp = new XMLHttpRequest();
    var url = MF.url + '/widgets/' + widget.widget + '?' + 'token=' + widget.token + '&lang=' + (widget.locale || 'en');

    if (widget.demo) {
      url = url + '&demo=true';
    }

    xhttp.onreadystatechange = function () {
      if (this.status === 200 && this.readyState == 4) {
        widget.data = widget.callback(xhttp.responseText);
        if (widget.data && widget.ready) {
          widget.render();
        }

      }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
  }

  var arr = MF.data;
  MF.data = [];
  if (Object.prototype.toString.call(arr) === '[object Object]' || Object.prototype.toString.call(arr[0]) === '[object Object]') {
    arr = [arr];
  }

  /* -------- Dependency handling -------- */
  var xhttp = new XMLHttpRequest()
  xhttp.onreadystatechange = function() {
    if (this.status === 200 && this.readyState == 4) {
      chainDeps(JSON.parse(xhttp.responseText));
    }
  }
  var depRequestBody = {tokens: []}
  arr[0].forEach(function(w) {depRequestBody.tokens.push(w.token)})
  var url = MF.url + '/widgets/get-dependencies'
  xhttp.open("POST", url)
  xhttp.setRequestHeader("Content-Type", "application/json")
  xhttp.send(JSON.stringify(depRequestBody))

  function chainDeps (fetchedDeps) {
    if (fetchedDeps && fetchedDeps.length > 0) {
      var depScripts = [] // chain dependency loading
      for (let i = 0; i < fetchedDeps.length; i++) {
        var dep = fetchedDeps[i]
        var newEl = document.createElement("script");
        newEl.type = "text/javascript";
        newEl.src = dep
        depScripts.push(newEl)
        if (i > 0) {
          depScripts[i - 1].addEventListener("load", function () {
            var body = document.getElementsByTagName("body")[0]
            if (nonce) {
              depScripts[i].setAttribute("nonce", nonce)
            }
            body.insertBefore(depScripts[i], body.firstChild)
          });
        }
      }

      depScripts[fetchedDeps.length - 1].addEventListener("load", function () { // load widgets when chain is finished
        arr.forEach(function (widget) {
          MF.push(widget)
        });
      });

      var body = document.getElementsByTagName("body")[0];
      if (nonce) {
        depScripts[0].setAttribute("nonce", nonce)
      }
      body.insertBefore(depScripts[0], body.firstChild); // load first dependency, starting the chain

    } else {
      arr.forEach(function (widget) {
        MF.push(widget)
      });
    }
  }
  /* -------- End Dependency handling -------- */


  MF.render = function () {
    MF.ready = true;
    arr.forEach(function (widget) {
      widget.render()
    })
  };

  // For executing script tags after innerHTML
  MF.setInnerHtml = function (widget, elm, html) {
    elm.innerHTML = html;

    var scripts = Array.from(elm.querySelectorAll("script"));

    if (scripts.length === 0) {
      if (MF.done_callback) {
        MF.done_callback(widget.token, elm);
      }
    }

    (function scriptReplace() {
      if (scripts.length === 0) {
        return
      }

      var scriptTag = scripts.shift();

      var newEl = document.createElement("script");
      newEl.type = "text/javascript";
      if (nonce) {
        newEl.setAttribute("nonce", nonce)
      }
      var attr = scriptTag.attributes;
      var hasSource = false;
      for (var j = 0; j < attr.length; j++) {
        hasSource = attr[j].name === 'src';
        newEl.setAttribute(attr[j].name, attr[j].value)
      }

      newEl.appendChild(document.createTextNode(scriptTag.innerHTML));
      scriptTag.parentNode.replaceChild(newEl, scriptTag);

      if (hasSource) {
        if (newEl.readyState) {  //IE
          newEl.onreadystatechange = function () {
            if (newEl.readyState == "loaded" || newEl.readyState == "complete") {
              newEl.onreadystatechange = null;
              scriptReplace();
            }
          };
        } else { // Other
          newEl.onload = scriptReplace;
        }
      } else {
        scriptReplace()
      }

    })();
  }

})(window._MF);
