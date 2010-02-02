jq(function(){
   jq('input.addreference').prepOverlay(
   {
        subtype: 'ajax',
        filter: '>*',
        closeselector: 'a.refbrowser_closewindow',
   }
);
});
