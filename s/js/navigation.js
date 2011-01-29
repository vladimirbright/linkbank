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
    var defaults, parse_hash, load, reload, split_chunk, is_two;

    split_chunk = function (chunk) {
        return [ chunk.split("=") ];
    };

    is_two = function (i) {
        return $(this).length == 2;
    };

    parse_hash = function(opts) {
        /*
            Ждем query string такого вида
            #q=&m=2&s=1&tag=34&tag=30&tag=1&page=5
        */
        var hash, hash_dict, placeholders, arrays;
        placeholders = [ "q", "s", "tags", "page" ];
        arrays = [ "tags" ];
        hash = location.hash;
        hash = hash.replace(/^#/, '');
        hash = $($.map(hash.split("&"), split_chunk)).filter(is_two);
        hash_dict = {};
        $(hash).each(function (i, el) {
            var k, v; 
            k = el[0];
            v = el[1];
            if (placeholders.indexOf(k) === -1) {
                return;
            }
            if (k in hash_dict) {
                if (arrays.indexOf(k) !== -1) {
                    hash_dict[k].push(v);
                    return;
                } 
                return;
            }
            if (arrays.indexOf(k) !== -1) {
                hash_dict[k] = [];
                hash_dict[k].push(v);
                return;
            }
            hash_dict[k] = v;
        });
        return hash_dict;
    };

    load = function (data) {
    
    };

    reload = function () {
    
    };

    defaults = {
        url: false,
        container_id: 'main_container',
        placeholders: [ "q", "s", "tags", "page" ],
        arrays: [ "tags" ]
    };

    $.fn.navigation = function(options) {
      opts = $.extend({}, defaults, options);
      if (opts.url === false) {
        return false;
      }

      return this.each(function() {
        var $this;
        $this = $(this);
      });
    };

})(jQuery);
