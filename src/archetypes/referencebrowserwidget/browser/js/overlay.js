
jq(function() {
        /*
   jq('input.addreference').prepOverlay({
        subtype: 'ajax',
        filter: '>*',
        closeselector: 'a.refbrowser_closewindow',
   });
   
   jQuery('.link').bind('click', function() {
        :
   });
  */ 

  jq('.addreference').overlay({
       closeOnClick: false,
       // TODO: enable close button
       onBeforeLoad: function() {
           var wrap = this.getContent().find('.overlaycontent');
           var src = this.getTrigger().attr('src');
           wrap.data('overlay', this);
           wrap.load(src + ' >*');
           }});

  jq('[id^=atrb_] a.browse').live('click', function(event) {
      var target = jq(this);
      var src = target.attr('href');
      var wrap = target.parents('.overlaycontent');
      wrap.load(src + ' #content');
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

});



