var SiteNavigation = new Class({

    Implements: [ Options, Events ],

    options: {
        searchChunk: "q",
        sortChunk: "s",
        tagsChunk: "tags",
        pageChunk: "page",
        sortedClass: "sorted",
        sortSelector: ".sorting",
        pageSelector: ".page",
        tagsSelector: ".tag",
        selectedTagClass: "ui-selected",
        selectedTagPrefix: ".tag_",
        timeout: 300,
        hashTimeout: 50,
        containerId: "main_container",
        requestOpts: {
            method: "get",
            noCache: true,
            chain: "cancel"
        },
        onReload: function () {},
        onPageReset: function () {},
        onHashSet: function () {}
    },
    /* some properties */
    lastLoadTimeout: false,
    loadOpts: {},
    loadUrl: false,
    navigation: {},
    searchInput: false,

    initialize: function(loadUrl, searchInputId, options) {
        this.loadUrl = loadUrl;
        this.searchInput = $(searchInputId);
        /* Bind methods to events */
        this.options.onReload = this.onReload;
        this.options.onPageReset = this.onPageReset;
        this.options.onHashSet = this.onHashSet;
        this.setOptions(options);
        /* Set AJAH URL  */
        this.loadOpts = this.options.requestOpts;
        this.loadOpts["update"] = this.options.containerId;
        this.bindEvens();
        this.checkHash();
    },

    lastHash: false,

    checkHash: function () {
        var h;
        h = window.location.hash;
        if (this.lastHash === false || this.lastHash != h) {
            this.lastHash = h;
            this.fireEvent("reload");
        }
        setTimeout(function () {
            this.checkHash(); 
        }.bind(this), this.options.hashTimeout);
    },

    onHashSet: function () {
        /* Get this.navigation and serilize in hash  */
        var t, hash;
        hash = "";
        // Search
        if (this.options.searchChunk in this.navigation) {
            hash = hash + this.options.searchChunk + "=" + this.navigation[this.options.searchChunk];
        } else {
            this.navigation[this.options.searchChunk] = "";
        }
        // Sort
        if (this.options.sortChunk in this.navigation) {
            hash = hash + "&" + this.options.sortChunk + "=" + this.navigation[this.options.sortChunk];
        }
        // Pagination
        if (this.options.pageChunk in this.navigation) {
            if (this.navigation[this.options.pageChunk] > 1) {
                hash = hash + "&" + this.options.pageChunk + "=" + this.navigation[this.options.pageChunk];
            } else {
                this.navigation[this.options.pageChunk] = 1;
            }
        }
        // Tags
        if (this.options.tagsChunk in this.navigation) {
            t = this.navigation[this.options.tagsChunk];
            if (Type.isArray(t) && t.length > 0) {
                hash = hash + "&" + this.options.tagsChunk + "=" + t.join("&" + this.options.tagsChunk + "=");
            } else {
                this.navigation[this.options.tagsChunk] = [];
            }
        }
        // Set hash
        window.location.hash = hash.replace(/^&/, "");
    },

    bindEvens: function () {
        this.searchInput.addEvent("keyup", this.addSearch.bind(this));
        $(window).addEvent("click:relay(" + this.options.tagsSelector + ')', this.addTag.bind(this));
        $(window).addEvent("click:relay(" + this.options.sortSelector + ')', this.addSort.bind(this));
        $(this.options.containerId).addEvent("click:relay(" + this.options.pageSelector + ")", this.addPage.bind(this));
    },

    onPageReset: function () {
        this.navigation[this.options.pageChunk] = 1;
    },

    addSearch: function (e) {
        this.fireEvent("pageReset");
        this.navigation[this.options.searchChunk] = this.searchInput.get("value");
        this.fireEvent("hashSet");
    },

    addPage: function (e) {
        e.preventDefault();
        this.navigation[this.options.pageChunk] = e.target.get("rel") || 1;
        this.fireEvent("hashSet");
    },

    addSort: function (e) {
        e.preventDefault();
        this.navigation[this.options.sortChunk] = e.target.get("rel") || "added";
        $$(this.options.sortSelector).removeClass(this.options.sortedClass);
        e.target.addClass(this.options.sortedClass);
        this.fireEvent("hashSet");
    },

    addTag: function (e) {
        var tag, c;
        e.preventDefault();
        this.fireEvent("pageReset");
        tag = e.target.get("rel");
        if (tag === null) {
            return false;
        }
        c = [];
        if (this.options.tagsChunk in this.navigation) {
            c = this.navigation[this.options.tagsChunk];
        }
        if (c === null || c.length == 0) {
            this.navigation[this.options.tagsChunk] = [tag];
            this.fireEvent("hashSet");
            return false;
        }
        /* tag allready selected */
        if (Type.isArray(c)) {
            if (c.indexOf(tag) !== -1) {
                /* remove from */
                c = Array.filter(c, function(el, i) {
                    return el !== tag;
                }.bind(this));
            } else {
                /* add to */
                c.push(tag);
            }
        } else {
            c = [];
        }
        this.navigation[this.options.tagsChunk] = c;
        this.fireEvent("hashSet");
    },

    mapTags: function () {
        /* Map selected tags */
        var c;
        $$(this.options.tagsSelector).removeClass(this.options.selectedTagClass);
        c = this.navigation[this.options.tagsChunk];
        if (Type.isArray(c) === false || c.length == 0) {
            return false;
        }
        c.each(function (el, i) {
            $$(this.options.selectedTagPrefix + el).addClass(this.options.selectedTagClass); 
        }.bind(this));
    },

    onReload: function () {
        var ajaxUrl;
        if (this.lastLoadTimeout !== false) {
            clearTimeout(this.lastLoadTimeout);
        }
        ajaxUrl = this.loadUrl + "?" + window.location.hash.replace(/^#/, "");
        this.loadOpts["url"] = ajaxUrl;
        this.loadOpts["onComplete"] = function () {
            setTimeout(function () {
                this.mapTags();
            }.bind(this), 20);
        }.bind(this);
        this.lastLoadTimeout = setTimeout(function () {
            var request;
            request = new Request.HTML(this.loadOpts);
            request.send();
        }.bind(this), this.options.timeout);
    }

});
