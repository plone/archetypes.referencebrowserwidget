jq(function() {

  // the overlay itself
  jq('.addreference').overlay({
       closeOnClick: false,
       onBeforeLoad: function() {
           var wrap = this.getContent().find('.overlaycontent');
           var src = this.getTrigger().attr('src');
           var srcfilter = src + ' >*';
           wrap.data('srcfilter', srcfilter);
           wrap.data('overlay', this);
           resetHistory();
           wrap.load(srcfilter);
           }});

  // the browse links on the right side of the widget
  jq('[id^=atrb_] a.browse').live('click', function(event) {
      var target = jq(this);
      var src = target.attr('href');
      var wrap = target.parents('.overlaycontent');
      var srcfilter = src + ' #content';
      pushToHistory(wrap.data('srcfilter'));
      wrap.data('srcfilter', srcfilter);
      wrap.load(srcfilter);
      return false;
      });

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
      var oldhistory = jq('[id^=atrb_] form#history select');
      wrap.load(srcfilter, function() { 
          jq('[id^=atrb_] form#history select').append(newoption + oldhistory.html());
          });
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
          overlay = wrap.data('overlay');
          overlay.close();
      } else {
          showMessage(title);
      };
      return false;
      });

  // the back link
  jq('[id^=atrb_] a.refbrowser_back').live('click', function(event) {
      var target = jq(this);
      var wrap = target.siblings('.overlaycontent');
      srcfilter = popFromHistory();
      wrap.load(srcfilter);
      return false;
      });

  // the clearhistory link
  jq('[id^=atrb_] a#clearhistory').live('click', function(event) {
      jq('[id^=atrb_] form#history select').empty();
      return false;
      });

  // the history-go button
  jq('[id^=atrb_] form#history input[name=go]').live('click', function(event) {
      var target = jq(this);
      var wrap = target.parents('.overlaycontent');
      src = jq('[id^=atrb_] form#history select[name=path] :selected').attr('value');
      var srcfilter = src + ' >*';
      wrap.load(srcfilter);
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
      qs = 'searchValue=' + searchvalue + '&fieldRealName' + fieldrealname +
        '&fieldName=' + fieldname + '&multiValued=' + multi +
        '&close_window' + close_window + '&at_url=' + at_url;
      var srcfilter = src + '?' + qs + ' >*';
      pushToHistory(wrap.data('srcfilter'));
      wrap.data('srcfilter', srcfilter);
      wrap.load(srcfilter);
      return false;
      });

});
