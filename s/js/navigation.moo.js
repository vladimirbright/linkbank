var SiteNavigation = new Class({

    Implements: [ Options, Events ],

    options: {
        searchChunk: "q",
        sortChunk: "s",
        tagsChunk: "tags",
        pageChunk: "page",
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
        onPageReset: function () {}
    },
    /* some properties */
    currentTags: [],
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
        this.setOptions(options);
        /* Set AJAH URL  */
        this.loadOpts = this.options.requestOpts;
        this.loadOpts["url"] = this.loadUrl;
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

    bindEvens: function () {
        /* Bind on keyup search input set hash chunk and this.fireEvent("reload") */
        this.searchInput.addEvent("keyup", function () {
            this.fireEvent("pageReset");
            this.setHashSearchValue();
        }.bind(this));
        /* bind click on tag links to add|remove tag from #tags */
        $(window).addEvent("click:relay(" + this.options.tagsSelector + ')', this.addTag.bind(this));
        $(this.options.containerId).addEvent("click:relay(" + this.options.pageSelector + ")", this.addPage.bind(this));
    },

    addPage: function (e) {
        var page, uri;
        e.preventDefault();
        page = e.target.get("rel");
        if (page === null) {
            return false;
        }
        uri = this.getURI();
        uri.setData(this.options.pageChunk, page); 
        this.setHash(uri);
    },

    onPageReset: function () {
        //this.setHash(this.getURI().setData(this.options.pageChunk, 1));
    },

    addTag: function (e) {
        var tag, uri, tagsString;
        e.preventDefault();
        this.fireEvent("pageReset");
        tag = e.target.get("rel");
        if (tag === null) {
            return false;
        }
        uri = this.getURI();
        this.checkCurrentTags();
        if (this.currentTags === null || this.currentTags.length == 0) {
            uri.setData(this.options.tagsChunk, tag); 
            this.setHash(uri);
            this.currentTags = [tag];
            return false;
        }
        /* tag allready selected */
        if (Type.isArray(this.currentTags) === true) {
            if (this.currentTags.indexOf(tag) !== -1) {
                /* remove from */
                this.currentTags = Array.filter(this.currentTags, function(el, i) {
                    return el !== tag;
                }.bind(this));
            } else {
                /* add to */
                this.currentTags.push(tag);
            }
        } else {
            this.currentTags = [];
        }
        /* serialize this.currentTags to tags=1&tags=3&tags=4 */ 
        tagsString = this.options.tagsChunk + "=" + this.currentTags.join("&" + this.options.tagsChunk + "=");
        /* remove tagsChunk from uri */
        uri.setData(this.options.tagsChunk);
        this.setHash(uri, tagsString);
    },

    checkCurrentTags: function () {
        uri = this.getURI();
        this.currentTags = uri.getData(this.options.tagsChunk) || null;
        if (typeOf(this.currentTags) === "string") {
            this.currentTags = [this.currentTags];
        }
    },

    mapTags: function () {
        /* Map selected tags */
        $$(this.options.tagsSelector).removeClass(this.options.selectedTagClass);
        if (Type.isArray(this.currentTags) === false) {
            return false;
        }
        this.currentTags.each(function (el, i) {
            $$(this.options.selectedTagPrefix + el).addClass(this.options.selectedTagClass); 
        }.bind(this));
    },

    getURI: function () {
        return new URI(this.loadUrl + '?' + window.location.hash.replace(/^#/, '')); 
    },

    getSearchValue: function () {
        return this.searchInput.get("value");
    },

    setHashSearchValue: function () {
        var uri;
        uri = this.getURI();
        uri.setData(this.options.searchChunk, this.getSearchValue());
        this.setHash(uri);
    },

    setHash: function (uri, appendix) {
        var query;
        query = uri.get("query");
        if (appendix) {
            if (query.trim().length > 0) {
                query = query + "&" + appendix;
            } else {
                query = appendix;
            }
        }
        window.location.hash = query;
    },

    onReload: function () {
        if (this.lastLoadTimeout !== false) {
            clearTimeout(this.lastLoadTimeout);
        }
        this.loadOpts["url"] = this.getURI().toString();
        this.loadOpts["onComplete"] = function () {
            setTimeout(function () {
                this.checkCurrentTags();
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
