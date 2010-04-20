jq(function() {

  // the overlay itself
  jq('.addreference').overlay({
       closeOnClick: false,
       onBeforeLoad: function() {
           ov = jq('div#content').data('overlay');
           // close overlay, if there is one already
           // we only allow one referencebrowser per time
           if (ov) {ov.close(); }
           var wrap = this.getContent().find('.overlaycontent');
           var src = this.getTrigger().attr('src');
           var srcfilter = src + ' >*';
           wrap.data('srcfilter', srcfilter);
           jq('div#content').data('overlay', this);
           resetHistory();
           wrap.load(srcfilter);
           },
       onLoad: function() {
           widget_id = this.getTrigger().attr('rel').substring(6);
           disablecurrentrelations(widget_id);
       }});

  // the breadcrumb-links and the links of the 'tree'-navigation
  jq('[id^=atrb_] a.browsesite').live('click', function(event) {
      var target = jq(this);
      var src = target.attr('href');
      var wrap = target.parents('.overlaycontent');
      var srcfilter = src + ' >*';
      pushToHistory(wrap.data('srcfilter'));
      wrap.data('srcfilter', srcfilter);
      // the history we are constructing here is destinct from the
      // srcfilter-history. here we construct a selection-widget, which
      // is available, if the history_length-parameter is set on the widget
      // the srcfilter-history is used for storing the URLs to make the
      // 'Back'-link work.
      var newoption = '<option value="' + src + '">' + target.attr('rel') + '</option>';
      refreshOverlay(wrap, srcfilter, newoption);
      return false;
      });

  // the links for inserting referencens
  jq('[id^=atrb_] input.insertreference').live('click', function(event) {
      var target = jq(this);
      var wrap = target.parents('.overlaycontent');
      var fieldname = wrap.find('input[name=fieldName]').attr('value');
      var multi = wrap.find('input[name=multiValued]').attr('value');
      var close_window = wrap.find('input[name=close_window]').attr('value');
      var title = target.parents('tr').find('img').attr('alt');
      var uid = target.attr('rel');
      refbrowser_setReference(fieldname, uid, title, parseInt(multi));
      if (close_window === '1') {
          overlay = jq('div#content').data('overlay');
          overlay.close();
      } else {
          showMessage(title);
      };
      jq(this).attr('disabled', 'disabled');
      });


  // the history menu
  jq('[id^=atrb_] form#history select[name=path]').live('change', function(event) {
      var target = jq(this);
      var wrap = target.parents('.overlaycontent');
      src = jq('[id^=atrb_] form#history select[name=path] :selected').attr('value');
      var srcfilter = src + ' >*';
      refreshOverlay(wrap, srcfilter, '');
      return false;
      });

  // the search form
  jq('[id^=atrb_] form#search input[name=submit]').live('click', function(event) {
      var target = jq(this);
      var src = target.parents('form').attr('action');
      var wrap = target.parents('.overlaycontent');
      var fieldname = wrap.find('input[name=fieldName]').attr('value');
      var fieldrealname = wrap.find('input[name=fieldRealName]').attr('value');
      var at_url = wrap.find('input[name=at_url]').attr('value');
      var searchvalue = wrap.find('input[name=searchValue]').attr('value');
      var multi = wrap.find('input[name=multiValued]').attr('value');
      var close_window = wrap.find('input[name=close_window]').attr('value');
      qs = 'searchValue=' + searchvalue + '&fieldRealName=' + fieldrealname +
        '&fieldName=' + fieldname + '&multiValued=' + multi +
        '&close_window' + close_window + '&at_url=' + at_url;
      var srcfilter = src + '?' + qs + ' >*';
      pushToHistory(wrap.data('srcfilter'));
      wrap.data('srcfilter', srcfilter);
      refreshOverlay(wrap, srcfilter, '');
      return false;
      });

});

function disablecurrentrelations (widget_id) {
   jq('ul#' + widget_id + ' :input').each(
       function (intIndex) {
         uid = jq(this).attr('value');
         cb = jq('input[rel=' + uid + ']');
         cb.attr('disabled', 'disabled');
         cb.attr('checked', 'checked');
       });
}

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
        down_element = null,
        container = null;
    // differentiate between the single and mulitselect widget
    // since the single widget has an extra label field.
    if (multi === 0) {
        jq('#' + widget_id).attr('value', uid);
        jq('#' + widget_id + '_label').attr('value', label);
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
            container = jq('#archetypes-fieldname-' + widget_id + ' input + div');
            if (!container.length) {
                // fix for Plone 3.3 collections, with a weird widget-id
                container = jq('#archetypes-fieldname-value input + div');
            }
            container.after(
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

        sortable = jq('input[name=' + widget_id + '-sortable]').attr('value');
        if (sortable === '1') {
          up_element = document.createElement('a');
          up_element.title = 'Move Up';
          up_element.innerHTML = '&#x25b2;';
          up_element.onclick = function () {
              refbrowser_moveReferenceUp(this);
              return false;
          };

          li.appendChild(up_element);

          down_element = document.createElement('a');
          down_element.title = 'Move Down';
          down_element.innerHTML = '&#x25bc;';
          down_element.onclick = function () {
              refbrowser_moveReferenceDown(this);
              return false;
          };

          li.appendChild(down_element);
        }
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
        jq('#' + widget_id).attr('value', "");
        jq('#' + widget_id + '_label').attr('value', "");
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

function refreshOverlay(wrap, srcfilter, newoption) {
    var oldhistory = jq('[id^=atrb_] form#history select');
    wrap.load(srcfilter, function() { 
        jq('[id^=atrb_] form#history select').append(newoption + oldhistory.html());
        ov = jq('div#content').data('overlay');
        widget_id = ov.getTrigger().attr('rel').substring(6);
        disablecurrentrelations(widget_id);
        });
}
