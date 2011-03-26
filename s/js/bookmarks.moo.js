var BookmarkActiveLink = new Class({

    Implements: [Options,Events],

    options: {
        onFormSuccess: function () {},
        onFormError: function () {},
        onClose: function () {},
        loadPlaceholder: new Element("div.ajax_bar_div"),
        containerId: "main_container",
        stickyOpts: {
            allowMultiple: false,
            closeOnClickOut: false,
            closeOnEsc: true,
            destroyOnClose: true,
            showNow: true
        },
        loadRequestOpts: {
            method: "get",
            noCache: true
        },
        sendRequestOpts: {
            method: "post",
            noCache: true
        }
    },
    /* some properties */
    currentLink: false,
    currentStickyWin: false,
    currentForm: false,

    initialize: function(selector, options) {
        this.setOptions(options);
        /* links may be loaded via ajax */
        $(this.options.containerId).addEvent("click:relay(" + selector + ')', this.loadFormFromLink.bind(this));
    },

    loadFormFromLink: function (e, clicked) {
        e.preventDefault();
        this.currentLink = $(clicked);
        this.createWin();
        this.currentStickyWin.update();
        this.currentStickyWin.show();
    },

    createWin: function () {
        var url, opts;
        url = this.currentLink.get("href");
        opts = this.options.stickyOpts;
        opts.url = url;
        opts.requestOptions = this.options.loadRequestOpts;
        opts.requestOptions.onComplete = function () {
            setTimeout(function () {
                this.currentStickyWin.position();
                this.bindForm();
            }.bind(this), 30);
        }.bind(this)
        this.currentStickyWin = new StickyWin.Ajax(opts);
        this.currentStickyWin.addEvent("close", function () {
            this.fireEvent("close");
        }.bind(this));
    },

    bindForm: function () {
        var form, opts;
        form = this.currentStickyWin.element.getElement("form");
        form = $(form);
        opts = this.options.sendRequestOpts;
        this.currentForm = new Form.Request(form, { resetForm: false, requestOptions: opts });
        form.addEvent("submit", this.sendForm.bind(this));
        this.currentForm.request.addEvent("success", this.getFormResult.bind(this));
    },

    sendForm: function (e) {
        e.preventDefault(); 
        this.currentForm.send();
    },

    getFormResult: function (el, xml, text) {
        this.currentStickyWin.setContent(text);
        this.currentStickyWin.position();
        if (text.toLowerCase().indexOf("<form") === -1) {
            this.fireEvent("formSuccess", this.currentStickyWin);
        } else {
            this.fireEvent("formError", this.currentStickyWin, this.currentForm);
            setTimeout(function () {
                this.currentStickyWin.position();
                this.bindForm();
            }.bind(this), 30);
        }
    }
});
