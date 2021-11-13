/* global MyAMS */

'use strict';


if (window.$ === undefined) {
    window.$ = MyAMS.$;
}


const content = {

    /**
     * Widgets management
     */
    widget: {

        /**
         * Treeview widget
         */
        treeview: {

            selectFolder: (event, node) => {
                const target = $(event.target);
                target.siblings('input[type="hidden"]').val(node.id);
            },

            unselectFolder: (event, node) => {
                const target = $(event.target);
                target.siblings('input[type="hidden"]').val(null);
            }
        }
    },


    /**
     * Pictograms management
     */
    pictograms: {

        initManagerSelection: function () {
            const
                form = $(this),
                selected = $('input[type="hidden"]', $('.selected-pictograms', form)).listattr('value');
            return {
                selected: JSON.stringify(selected)
            };
        },

        switchPictogram: (event) => {
            $('i', event.currentTarget).tooltip('hide');
            let pictogram = $(event.currentTarget);
            if (!pictogram.hasClass('pictogram')) {
                pictogram = pictogram.parents('.pictogram');
            }
            const
                input = $('input', pictogram),
                parent = pictogram.parents('.pictograms'),
                manager = parent.parents('.pictograms-manager');
            if (parent.hasClass('available-pictograms')) {
                const name = input.attr('data-ams-pictogram-name');
                input.removeAttr('data-ams-pictogram-name')
                    .attr('name', name);
                $('a.action i', pictogram).replaceWith($('<i></i>')
                    .addClass('fa fa-fw fa-arrow-left hint opaque baseline')
                    .attr('data-ams-hint-gravity', 'se')
                    .attr('data-ams-hint-offset', '3'));
                $('.selected-pictograms', manager).append(pictogram);
            } else {
                const name = input.attr('name');
                input.removeAttr('name')
                    .attr('data-ams-pictogram-name', name);
                $('a.action i', pictogram).replaceWith($('<i></i>')
                    .addClass('fa fa-fw fa-arrow-right hint opaque baseline')
                    .attr('data-ams-hint-gravity', 'se')
                    .attr('data-ams-hint-offset', '3'));
                $('.available-pictograms', manager).append(pictogram);
            }
        },

        endDrag: (event, ui) => {
            $(ui.source).remove();
        }
    }
};


if (window.MyAMS) {
    MyAMS.config.modules.push('content');
    MyAMS.content = content;
    console.debug("MyAMS: content module loaded...");
}
