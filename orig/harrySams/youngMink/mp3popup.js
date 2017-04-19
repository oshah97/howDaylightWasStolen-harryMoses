function popupPlay (url) {
  var options =  'width=500,height=100,' +
                 'scrollbars=yes,'       +
                 'resizable=yes,'        +
                 'alwaysRaised=yes';
  var playWindow = window.open (url, 'Hess and Hilbert', options);
  playWindow.focus ();
  }

