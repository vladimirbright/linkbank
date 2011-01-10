(function($) {
//
// simple placeholder plugin $("#input_id").placeholder({ initial: "Search here" })
//
    var bind, defaults;

    bind = function (el, opts) {
        el.focus(function () { 
            if (el.val() == opts.initial) {
                el.val("");
            }
        }).blur(function () {
            if ($.trim(el.val()) == "") {
                el.val(opts.initial);
            }
        });
    };

    defaults = {
      initial: false
    };

    $.fn.placeholder = function(options) {
      opts = $.extend({}, defaults, options);
      return this.filter(":input").each(function() {
        $this = $(this);
        if (opts.initial === false) {
            return false;
        }
        bind($this, opts);
      });
    };

})(jQuery);
