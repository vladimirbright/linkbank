function NavigationObserver2 (searchId) {
    var searchInput = document.getElementById(searchId)
        , keyupTimeout = null
        , keyupTTL = 500
        , query = searchInput.value
        , page = 1
        , searchChunk = 'q'
        , pageChunk = 'page'
        ;

    console.log(searchInput);

    function hashBang() {
        var hash = '';
        if (query) {
            hash += searchChunk + '=' + encodeURI(query);
        }
        if (page > 1) {
            if (query) {
                hash += '&';
            }
            hash += pageChunk + "=" + page;
        } 
        location.hash = hash;
    }

    function clickPagination (e) {
        console.log('Выставляем пагинацию');
        console.log(this); 
    }
    
    function clickHashtag (e) {
        console.log('Выставляем hash tag');
        console.log(this); 
    }

    function keyupSearch (e) {
        query = searchInput.value;
        page = 1;
        hashBang();
        return false;
    }

    function timeotedSearch (e) {
        if (keyupTimeout) {
            clearTimeout(keyupTimeout);
        }
        keyupTimeout = setTimeout(function () { keyupSearch(e); }, keyupTTL);
        return false;
    };
    searchInput.onkeyup = timeotedSearch;
    searchInput.onsubmit = timeotedSearch;
}

window.onload = function () {
    NavigationObserver2('id_search');
};
