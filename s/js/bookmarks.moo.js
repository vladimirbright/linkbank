var BookmarkActiveLink = new Class({
    selector: false,
    csrfToken: false,
    currentLink: false,

    Implements: [Options,Events],

    options: {
        loadPlaceholder: new Element("div.ajax_bar_div"),
        onFormSuccess: function () {},
        onFormError: function () {},
        containerId: "main_container"
    },

    initialize: function(selector, options) {
        this.selector = selector;
        /* bind methods to defaults */
        this.options.onFormSuccess = this.onFormSuccess.bind(this);
        this.options.onFormError = this.onFormError.bind(this);
        this.setOptions(options);
        /* links may be loaded via ajax */
        $(this.options.containerId).addEvent("click:relay(" + this.selector + ')', this.loadFormFromLink.bind(this));
    },

    loadFormFromLink: function (e, clicked) {
        /*
            1. Get title, href from clicked link
            2. Show modal window with loader gif
            3. Get html from href
            4. Insert into window ajah result
        */
        e.preventDefault();
        this.currentLink = $(clicked);
        this.fireEvent("formSuccess");
    },

    sendForm: function () {

    },

    onFormError: function () {
        alert("formerror fire!");
    },

    onFormSuccess: function () {
        alert("formsuccess fire!");
    }
});
// Добавление, сохранение, удаление. Навигация отдельно.
//(function($) {
//[>
    //Плагин для форм подгружаемых и отправляемых через ajax
    //Может быть применен только к элементам вида
    //<a 
        //href="/url/to/form"
        //title="Delete bookmark form"
    //>
    //Аттрибуты
        //href - загрузка формы в dialog, отправка резултатов на валидацию
               //если в полученном html нет тега form, то операция завершена
               //и диалог можно закрывать
        //title - заголовок диалога
    //Применять так
        //$('.edit').bookmarks();
//*/
    //var defaults, load_form, send_form, process_error, opts;

    //process_error = function (d, xhr, status, err) {
        //// Функция для обработки ошибок загрузки формы
        //d.html(status);
        //d.dialog("option", "position", "center");
    //};

    //send_form = function (ajax_url, d) {
        //// Функция отсылки формы.
        //var _aopts;
        //// Показываем гиф загрузки
        //d.dialog("option", "position", "center");
        //_aopts = $.extend({
            //type: "POST",
            //cache: false,
            //url: ajax_url,
            //data: $(d).find("form").first().serialize(),
            //beforeSend: function (XMLHttpRequest, settings) {
                //d.html(opts.loader);
                //d.dialog("option", "position", "center");
                //return true; 
            //},
            //success: function (data, status, xhr) {
                //d.html(data);
                //if (data.toLowerCase().indexOf("<form") === -1) {
                    //// Форма пришла без ошибок. Заменяем кнопки на Close
                    //d.dialog("option", "buttons", {
                        //"Close": function () { 
                            //$("#" + opts.container_id).trigger("reload");
                            //d.dialog("close");
                        //}
                    //}); 
                //} 
                //d.dialog("option", "position", "center");
            //},
            //error: function (xhr, status, err) {
                //process_error(d, xhr, status, err);
            //}
        //}, opts.send_ajax_params);
        //$.ajax(_aopts);
    //};


    //load_form = function (el) {
        //// Функция загрузки формы
        //var ajax_url, d;
        //ajax_url = el.attr("href") || el.attr("rel");
        //if (ajax_url === null || ajax_url == "") {
            //return false;
        //}
        //d = $('<div></div>', { title: el.attr("title") || "" });
        //$(d).dialog($.extend({} ,{
            //modal: true,
            //open: function (event, ui) {
                //var _aopts;
                //// Открытие диалога
                //// 1. Гиф загрузки
                //d.html(opts.loader);
                //// 2. Опции для ajah запроса
                //_aopts = $.extend({
                    //type: "GET",
                    //url: ajax_url,
                    //cache: false,
                    //success: function (data, status, xhr) {
                            //// Получение данных с сервера с формой
                            //d.html(data);
                            //// Центруем окно
                            //d.dialog("option", "position", "center");
                        //},
                    //error: function (xhr, status, err) {
                        //// Обработки ошибки TODO
                        //process_error(d, xhr, status, err);
                    //}
                //}, opts.load_ajax_params);
                //// 3. Посылаем запрос
                //$.ajax(_aopts);
            //},
            //buttons: {
                //"Ok": function () {
                    //send_form(ajax_url, d);
                //},
                //"Cancel": function () {
                    //$(this).dialog("close");
                //}
            //}
        //}, opts.dialog_opts));
    //};

    //defaults = {
        //loader: $("<div></div>", { "class": "ajax_bar_div" }),
        //load_ajax_params: {
            //type: "GET",
            //cache: false
        //},
        //send_ajax_params: {
            //type: "POST",
            //cache: false
        //},
        //dialog_opts: {},
        //container_id: 'main_container'
    //};

    //opts = {};

    //$.fn.bookmarks = function(selector, options) {
      //opts = $.extend({}, defaults, options);
      //$("#" + opts.container_id).delegate(selector, "click", function(){
        //load_form($(this));
        //return false;
      //});
    //};

//})(jQuery);