/*
    Simple placeholder class.
    var p = new Placeholder(id_of_input, placeholder_word);
        or
    var p = new Placeholder(id_of_input, placeholder_word, { onlyOnce: false });
*/
var Placeholder = new Class({
    edited: false,
    input: false,
    placeholder: false,

    Implements: [Options,Events],

    options: {
        onlyOnce: true
    },

    initialize: function(input_id, placeholder, options) {
        this.setOptions(options);
        this.input = $(input_id);
        this.placeholder = placeholder;
        this.input.addEvent("change", function (e) {
            this.edited = true;
        }.bind(this));
        this.input.addEvent("focus", this.setOnFocus.bind(this));
        this.input.addEvent("blur", this.setOnBlur.bind(this));
    },

    setOnFocus: function (e) {
        var value;
        if (this.options.onlyOnce === true && this.edited === true) {
            this.removeEvents();
            return false;
        }
        value = this.input.get("value");
        if (value == this.placeholder) {
            this.input.set("value", "");
        }
    },

    setOnBlur: function (e) {
        var value;
        if (this.options.onlyOnce === true && this.edited === true) {
            this.removeEvents();
            return false;
        }
        value = this.input.get("value");
        if (value == "") {
            this.input.set("value", this.placeholder);
        }
    },

    removeEvents: function () {
        this.input.removeEvent("focus", this.setOnFocus);
        this.input.removeEvent("blur", this.setOnBlur);
    }

});
