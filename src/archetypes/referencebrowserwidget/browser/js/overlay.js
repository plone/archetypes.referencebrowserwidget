jq(function() {

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

  jq('[id^=atrb_] a.browsesite').live('click', function(event) {
      var target = jq(this);
      var src = target.attr('href');
      var wrap = target.parents('.overlaycontent');
      var srcfilter = src + ' >*';
      pushToHistory(wrap.data('srcfilter'));
      wrap.data('srcfilter', srcfilter);
      wrap.load(srcfilter);
      return false;
      });

  jq('[id^=atrb_] a.insertreference').live('click', function(event) {
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

  jq('[id^=atrb_] a.refbrowser_back').live('click', function(event) {
      var target = jq(this);
      var wrap = target.siblings('.overlaycontent');
      srcfilter = popFromHistory();
      wrap.load(srcfilter);
      return false;
      });

  jq('[id^=atrb_] form input[name=submit]').live('click', function(event) {
      var target = jq(this);
      var src = target.parents('form').attr('action');
      var wrap = target.parents('.overlaycontent');
      var fieldname = wrap.find('input[name=fieldName]').attr('value');
      var fieldrealname = wrap.find('input[name=fieldRealName]').attr('value');
      var at_url = wrap.find('input[name=at_url]').attr('value');
      var searchvalue = wrap.find('input[name=searchValue]').attr('value');
      var multi = wrap.find('input[name=multiValued]').attr('value');
      var close_window = wrap.find('input[name=close_window]').attr('value');
      qs = 'searchValue=' + searchvalue + '&fieldRealName' + fieldrealname + '&fieldName=' + fieldname + '&multiValued=' + multi + '&close_window' + close_window + '&at_url=' + at_url;
      var srcfilter = src + '?' + qs + ' >*';
      pushToHistory(wrap.data('srcfilter'));
      wrap.data('srcfilter', srcfilter);
      wrap.load(srcfilter);
      return false;
  });

});
