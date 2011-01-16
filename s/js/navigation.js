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
    var defaults, parse_hash, load, reload;

    parse_hash = function() {
        var hash;
        hash = location.hash.replace(/^#/, '').split('&');
        return {}; 
    };

    load = function (data) {
    
    };

    reload = function () {
    
    };

    defaults = {
        url: false,
        container_id: 'main_container'
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
