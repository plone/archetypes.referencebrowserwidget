// function to open the popup window
function refbrowser_openBrowser(path, fieldName, at_url, fieldRealName, width, height)
{
    atrefpopup = window.open(path + '/refbrowser_popup?fieldName=' + fieldName + '&fieldRealName=' + fieldRealName +'&at_url=' + at_url,'refbrowser_popup','toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=' + width + ',height=' + height);
}

// function to return a reference from the popup window back into the widget
function refbrowser_setReference(widget_id, uid, label, multi)
{
    // differentiate between the single and mulitselect widget
    // since the single widget has an extra label field.
    if (multi==0) {
        element=document.getElementById(widget_id)
        label_element=document.getElementById(widget_id + '_label')
        element.value=uid
        label_element.value=label
     }  else {
         // check if the item isn't already in the list
         var current_values = jq('#' + widget_id + ' input');
         for (var i=0; i < current_values.length; i++) {
            if (current_values[i].value == uid) {
              return false;
            }
          }
          // now add the new item
          var list = document.getElementById(widget_id);
          var li = document.createElement('li');
          var label_element = document.createElement('label');
          var input = document.createElement('input');
          input.type = 'checkbox';
          input.value = uid;
          input.checked = true;
          input.name = widget_id + ':list';
          label_element.appendChild(input);
          label_element.appendChild(document.createTextNode(' ' + label));
          li.appendChild(label_element);
          li.id = 'ref-' + widget_id + '-' + current_values.length;

          var up_element = document.createElement('img');
          up_element.src = 'arrowUp.gif';
          up_element.alt = 'up';
          up_element.onclick = function() {
              refbrowser_moveReferenceUp(this);
              }

          li.appendChild(up_element)

          var down_element = document.createElement('img');
          down_element.src = 'arrowDown.gif';
          down_element.alt = 'down';
          down_element.onclick = function() {
              refbrowser_moveReferenceDown(this);
              }

          li.appendChild(down_element)
          list.appendChild(li);

          // fix on IE7 - check *after* adding to DOM
          input.checked = true;

     }
}

// function to clear the reference field or remove items
// from the multivalued reference list.
function refbrowser_removeReference(widget_id, multi)
{
    if (multi) {
        list=document.getElementById(widget_id)
        for (var x=list.length-1; x >= 0; x--) {
          if (list[x].selected) {
            list[x]=null;
          }
        }
        for (var x=0; x < list.length; x++) {
            list[x].selected='selected';
          }
    } else {
        element=document.getElementById(widget_id);
        label_element=document.getElementById(widget_id + '_label');
        label_element.value = "";
        element.value="";
    }
}

function refbrowser_moveReferenceUp(self)
{
  var elem = self.parentNode;
  if (elem == null) { return false }
  var eid = elem.id.split('-')
  var pos = eid.pop();
  if (pos == 0) { return false }
  var widget_id = eid.pop();

  var newelem = elem.cloneNode(true);

  //Fix: (IE keep the standard value)
  var cbs = newelem.getElementsByTagName("input")
  if (cbs.length > 0) {
    cbs[0].checked = elem.getElementsByTagName("input")[0].checked
  }

  var prevelem = document.getElementById('ref-' + widget_id + '-' + (pos-1));

  // up img
  var imgs = newelem.getElementsByTagName("img")
  imgs[0].onclick = function() {
              refbrowser_moveReferenceUp(this);
              }
  // down img
  imgs[1].onclick = function() {
              refbrowser_moveReferenceDown(this);
              }

  elem.parentNode.insertBefore(newelem, prevelem);
  elem.parentNode.removeChild(elem);
  newelem.id = 'ref-' + widget_id + '-' + (pos-1);
  prevelem.id = 'ref-' + widget_id + '-' + pos;
}

function refbrowser_moveReferenceDown(self)
{
  var elem = self.parentNode;
  if (elem == null) { return false }
  var eid = elem.id.split('-')
  var pos = parseInt(eid.pop());
  var widget_id = eid.pop();
  var current_values = cssQuery('#' + widget_id + ' input');
  if ((pos+1) == current_values.length) { return false }

  var newelem = elem.cloneNode(true);
  //Fix: (IE keep the standard value)
  var cbs = newelem.getElementsByTagName("input")
  if (cbs.length > 0) {
    cbs[0].checked = elem.getElementsByTagName("input")[0].checked
  }

  // up img
  var imgs = newelem.getElementsByTagName("img")
  imgs[0].onclick = function() {
               refbrowser_moveReferenceUp(this);
              }
  // down img
  imgs[1].onclick = function() {
              refbrowser_moveReferenceDown(this);
              }

  var nextelem = document.getElementById('ref-' + widget_id + '-' + (pos+1));

  elem.parentNode.insertBefore(newelem, nextelem.nextSibling);
  elem.parentNode.removeChild(elem);
  newelem.id = 'ref-' + widget_id + '-' + (pos+1);
  nextelem.id = 'ref-' + widget_id + '-' + pos;
}

