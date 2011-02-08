(function($) {
/*
    Навигация по спискам ссылок
    Навигация состоит из параметров.
    1. Поиск.
        1.1. Поисковая фраза сегмент q, пустая хначит все ссылки
        1.2. Режим поиска сегмент m
        1.3. Сортировка s
    2. Теги. Может быть несколько одновременно. сегмент tag
    3. Постраничный вывод. Сегмент page

    т.е. хеш может быть вида

    #q=&m=2&s=1&tag=34&tag=30&tag=1&page=5

    Функции необходимые для всего этого счастья
    1. Разобрать хеш.
    2. Отослать разобранное на сервер и вставить резултат в страницу
    3. Добавлять, изменять, удалять сегменты хеша.


*/
    var defaults, parse_hash, set_hash, reload, split_chunk, is_two, opts, get_search, last_timeout;

    opts = {};

    split_chunk = function (chunk) {
        return [ chunk.split("=") ];
    };

    is_two = function (i) {
        return $(this).length == 2;
    };

    parse_hash = function() {
        /*
            Ждем query string такого вида
            #q=&m=2&s=1&tag=34&tag=30&tag=1&page=5
        */
        var hash, hash_dict, placeholders, arrays;
        hash = location.hash;
        hash = hash.replace(/^#/, '');
        hash = $($.map(hash.split("&"), split_chunk)).filter(is_two);
        hash_dict = {};
        $(hash).each(function (i, el) {
            var k, v; 
            k = el[0];
            v = el[1];
            if (opts.placeholders.indexOf(k) === -1) {
                return;
            }
            if (k in hash_dict) {
                if (opts.arrays.indexOf(k) !== -1) {
                    hash_dict[k].push(v);
                    return;
                } 
                return;
            }
            if (opts.arrays.indexOf(k) !== -1) {
                hash_dict[k] = [];
                hash_dict[k].push(v);
                return;
            }
            hash_dict[k] = v;
        });
        return hash_dict;
    };

    set_hash = function (hash_dict) {
        var hash; 
        hash = "#";
        $(opts.placeholders).each(function (i, el) {
            var is_array; 
            if (el in hash_dict === false) {
                return;
            }
            is_array = opts.arrays.indexOf(el) !== -1;
            if (is_array === false) {
                hash = hash + el + '=' + hash_dict[el] + '&';
                return;
            }
            $(hash_dict[el]).each(function (k, ar) {
                hash = hash + k + '=' + ar + '&';
            });
        });
        location.hash = hash;
    };

    get_search = function () {
        var q, h;
        q = $(opts.search_selector).val();
        h = parse_hash();
        h[opts.placeholders[0]] = q;
        set_hash(h);
    };

    last_timeout = false;

    reload = function () {
        var ajax_url, h;
        h = location.hash.replace(/^#/, '');
        ajax_url = opts.url + '?' + h;
        if (last_timeout !== false) {
            clearTimeout(last_timeout);
        }
        last_timeout = setTimeout(function () {
            $('#' + opts.container_id).load(ajax_url);
        }, opts.timeout);
    };

    defaults = {
        url: false,
        container_id: 'main_container',
        placeholders: [ "q", "s", "tags", "page" ],
        arrays: [ "tags" ],
        timeout: 1000,
        tag_selector: ".tag_sel",  // links to set or remove tag
        sort_selector: ".sort",    // links to set sort mode
        search_selector: "#id_q"   // input for keyup reload
    };

    $.fn.navigation = function(options) {
      opts = $.extend({}, defaults, options);
      if (opts.url === false) {
        return false;
      }
      // Бинды
      $('#' + opts.container_id).bind("reload", function () {
        get_search();
        reload();
        return false;
      });
      $(this).click(function () {
        $('#' + opts.container_id).trigger("reload");
        return false;
      });
      $(opts.search_selector).keyup(function () {
        get_search();
        $('#' + opts.container_id).trigger("reload");
        return false;
      });
    };

})(jQuery);
