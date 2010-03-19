// function to return a reference from the popup window back into the widget
function refbrowser_setReference(widget_id, uid, label, multi)
{
    var element = null,
        label_element = null,
        current_values = null,
        i = null,
        list = null,
        li = null,
        input = null,
        up_element = null,
        down_element = null;
    // differentiate between the single and mulitselect widget
    // since the single widget has an extra label field.
    if (multi === 0) {
        element = document.getElementById(widget_id);
        label_element = document.getElementById(widget_id + '_label');
        element.value = uid;
        label_element.value = label;
    }  else {
        // check if the item isn't already in the list
        current_values = jq('#' + widget_id + ' input');
        for (i = 0; i < current_values.length; i++) {
            if (current_values[i].value === uid) {
                return false;
            }
        }
        // now add the new item
        list = document.getElementById(widget_id);
        // add ul-element to DOM, if it is not there
        if (list === null) {
            jq('#archetypes-fieldname-' + widget_id + ' input + div').after(
               '<ul class="visualNoMarker" id="' + widget_id + '"></ul>');
            list = document.getElementById(widget_id);
        }
        li = document.createElement('li');
        label_element = document.createElement('label');
        input = document.createElement('input');
        input.type = 'checkbox';
        input.value = uid;
        input.checked = true;
        input.name = widget_id + ':list';
        label_element.appendChild(input);
        label_element.appendChild(document.createTextNode(' ' + label));
        li.appendChild(label_element);
        li.id = 'ref-' + widget_id + '-' + current_values.length;

        up_element = document.createElement('a');
        up_element.title = 'Move Up';
        up_element.innerHTML = '&#x25b2;';
        up_element.onclick = function () {
            refbrowser_moveReferenceUp(this);
        };

        li.appendChild(up_element);

        down_element = document.createElement('a');
        down_element.title = 'Move Down';
        down_element.innerHTML = '&#x25bc;';
        down_element.onclick = function () {
            refbrowser_moveReferenceDown(this);
        };

        li.appendChild(down_element);
        list.appendChild(li);

        // fix on IE7 - check *after* adding to DOM
        input.checked = true;
    }
}

// function to clear the reference field or remove items
// from the multivalued reference list.
function refbrowser_removeReference(widget_id, multi)
{
    var x = null,
        element = null,
        label_element = null,
        list = null;

    if (multi) {
        list = document.getElementById(widget_id);
        for (x = list.length - 1; x >= 0; x--) {
            if (list[x].selected) {
                list[x] = null;
            }
        }
        for (x = 0; x < list.length; x++) {
            list[x].selected = 'selected';
        }
    } else {
        element = document.getElementById(widget_id);
        label_element = document.getElementById(widget_id + '_label');
        label_element.value = "";
        element.value = "";
    }
}

function refbrowser_moveReferenceUp(self)
{
    var elem = self.parentNode,
        eid = null,
        pos = null,
        widget_id = null,
        newelem = null,
        prevelem = null,
        arrows = null,
        cbs = null;
    if (elem === null) {
        return false;
    }
    eid = elem.id.split('-');
    pos = eid.pop();
    if (pos === 0) {
        return false;
    }
    widget_id = eid.pop();
    newelem = elem.cloneNode(true);

    //Fix: (IE keep the standard value)
    cbs = newelem.getElementsByTagName("input");
    if (cbs.length > 0) {
        cbs[0].checked = elem.getElementsByTagName("input")[0].checked;
    }

    prevelem = document.getElementById('ref-' + widget_id + '-' + (pos - 1));

    // up arrow
    arrows = newelem.getElementsByTagName("a");
    arrows[0].onclick = function () {
        refbrowser_moveReferenceUp(this);
    };
    // down arrow
    arrows[1].onclick = function () {
        refbrowser_moveReferenceDown(this);
    };

    elem.parentNode.insertBefore(newelem, prevelem);
    elem.parentNode.removeChild(elem);
    newelem.id = 'ref-' + widget_id + '-' + (pos - 1);
    prevelem.id = 'ref-' + widget_id + '-' + pos;
}

function refbrowser_moveReferenceDown(self)
{
    var elem = self.parentNode,
        eid = null,
        pos = null,
        widget_id = null,
        current_values = null,
        newelem = null,
        nextelem = null,
        cbs = null,
        arrows = null;
    if (elem === null) {
        return false;
    }
    eid = elem.id.split('-');
    pos = parseInt(eid.pop(), 10);
    widget_id = eid.pop();
    current_values = jq('#' + widget_id + ' input');
    if ((pos + 1) === current_values.length) {
        return false;
    }

    newelem = elem.cloneNode(true);
    //Fix: (IE keep the standard value)
    cbs = newelem.getElementsByTagName("input");
    if (cbs.length > 0) {
        cbs[0].checked = elem.getElementsByTagName("input")[0].checked;
    }

    // up img
    arrows = newelem.getElementsByTagName("a");
    arrows[0].onclick = function () {
        refbrowser_moveReferenceUp(this);
    };
    // down img
    arrows[1].onclick = function () {
        refbrowser_moveReferenceDown(this);
    };

    nextelem = document.getElementById('ref-' + widget_id + '-' + (pos + 1));

    elem.parentNode.insertBefore(newelem, nextelem.nextSibling);
    elem.parentNode.removeChild(elem);
    newelem.id = 'ref-' + widget_id + '-' + (pos + 1);
    nextelem.id = 'ref-' + widget_id + '-' + pos;
}

function showMessage(message) {
    jq('#messageTitle').text(message);
    jq('#message').show();
}

function submitHistoryForm() {
     var form = document.history;
     var path = form.path.options[form.path.selectedIndex].value;
     form.action = path;
     form.submit();
}

function pushToHistory(url) {
  var history = jq(document).data('atrb_history');
  history.push(url);
  jq(document).data('atrb_history', history);
}

function resetHistory() {
  jq(document).data('atrb_history', []);
}

function popFromHistory() {
  var history = jq(document).data('atrb_history');
  value = history.pop();
  jq(document).data('atrb_history', history);
  return value;
}
