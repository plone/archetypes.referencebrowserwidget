
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
           // TODO: only select relevant parts of body
           var src = this.getTrigger().attr('src');
           wrap.load(src + ' >*');
           }});

  jq('[id^=atrb_] a').live('click', function(event) {
      var src = jq(this).attr('href');
      var wrap = jq(this).parents('.overlaycontent');
      console.log(wrap);
      wrap.load(src + ' #content');
      return false;
      });

  //alert('0');

});



