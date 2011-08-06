// Мои классы для сайта


// Класс отвечающий за поиск и пагинацию
// Следит за поисковым инпутом и нажатиями на пагинирующие ссылки
// и выставляет соответсвующий хеш

var SiteNavigationObserver = new Class({

    Implements: [ Options, Events ],

    options: {
        containerId: "id_bookmarks",
        pageChunk: "page",
        pageSelector: ".page",
        searchChunk: "q", 
        searchId: "id_search"
    },
    /* some properties */
    searchTerm: "",
    searchInput: false,

    initialize: function(options) {
        this.setOptions(options);
        try {
            this.searchInput = $(this.options.searchId);
        } catch (e) {
            return false;
        }
        this.bindEvens();
        this.setSearchChunk();
    },

    bindEvens: function () {
        this.searchInput.addEvent("keyup", this.setSearchChunk.bind(this));
        document.id(this.options.containerId).addEvent("click:relay(" + this.options.pageSelector + ")", this.setPaginationChunk.bind(this));
    },

    setPaginationChunk: function (cathedEvent) {
        var clickedLink, pageNumber;
        cathedEvent.preventDefault();
        clickedLink = cathedEvent.target;
        pageNumber = (clickedLink.get("rel") || "").replace(/[^\d]/, "");
        if (pageNumber) {
            if (this.searchTerm) {
                window.location.hash = this.options.searchChunk + '=' + this.searchTerm + "&" + this.options.pageChunk + "=" + pageNumber;
            } else {
                window.location.hash = this.options.pageChunk + "=" + pageNumber;
            }
        }
    },

    setSearchChunk: function (cathedEvent) {
        this.searchTerm = this.searchInput.get("value");
        if (this.searchTerm) {
            window.location.hash = this.options.searchChunk + '=' + this.searchTerm;
        } else {
            window.location.hash = "";
        }
    }

});

// Класс, который загружает результаты поиска, исохдя из location.hash
var SiteNavigationLoader = new Class({

    Implements: [ Options, Events ],

    options: {
        requestTimeout: 500,
        hashTimeout: 50,
        requestOpts: {
            update: "id_bookmarks",
            method: "get",
            noCache: true,
            chain: "cancel"
        },
        scrollToId: "id_search",
        scrollOpts: {
            wait: false,
            duration: 500,
            offset: {'x': 0, 'y': -10},
            transition: Fx.Transitions.Quad.easeInOut
        }
    },
    /* some properties */
    loadUrl: "",
    loadOpts: {},
    lastHash: false,
    lastTimeout: false,
    scroll: false,

    initialize: function(loadUrl, options) {
        this.options.onHashReload = this.onHashSet;
        this.setOptions(options);
        this.loadUrl = loadUrl;
        this.loadOpts = this.options.requestOpts;
        this.scroll = new Fx.Scroll(document.body, this.options.scrollOpts);
        this.checkHash();
        this.addEvent("hashReload", this.onHashReload.bind(this))
    },

    checkHash: function () {
        if (this.lastHash === false || this.lastHash != window.location.hash) {
            this.lastHash = window.location.hash;
            this.fireEvent("hashReload");
        }
        setTimeout(this.checkHash.bind(this), this.options.hashTimeout);
    },

    onHashReload: function () {
        var loadUriParams, fullLoadUrl, fullRequestParams;
        loadUriParams = window.location.hash.replace(/^#/, "");
        fullLoadUrl = this.loadUrl + "?" + encodeURI(loadUriParams);
        fullRequestParams = this.loadOpts;
        fullRequestParams.url = fullLoadUrl;
        fullRequestParams.onComplete = function () {
            this.scroll.toElement(this.options.scrollToId);
        }.bind(this);
        console.log(fullRequestParams);
        if (this.lastTimeout !== false) {
            clearTimeout(this.lastTimeout);
        }
        this.lastTimeout = setTimeout(function () {
            new Request.HTML(fullRequestParams).send();
        }.bind(this), this.options.requestTimeout);
    }

});

