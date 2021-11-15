/* global MyAMS */

'use strict';


if (window.$ === undefined) {
    window.$ = MyAMS.$;
}


const content = {

    /**
     * Tree management
     */
    tree: {

        /**
         * Visibility switch callback handler
         *
         * @param form: original form (may be empty)
         * @param options: callback options
         */
        switchVisibleElement: (form, options) => {
            const
                node_id = options.node_id,
                tr = $(`tr[data-ams-tree-node-id="${node_id}"]`),
                table = $(tr.parents('table')),
                head = $('thead', table),
                col = $(`th[data-ams-column-name="visible"]`, head),
                colPos = col.index(),
                icon = $('i', $(`td:nth-child(${colPos+1})`, tr)),
                parent = $(`[data-ams-tree-node-id="${tr.data('ams-tree-node-parent-id')}"]`);
            let klass;
            if (parent.get(0).tagName === 'TR') {
                const parentIcon = $('i', $(`td:nth-child(${colPos+1})`, parent));
                klass = parentIcon.attr('class');
            } else {
                klass = table.data('ams-visible') ? '' : 'text-danger';
            }
            debugger
            if (options.state === true) {
                icon.replaceWith(`<i class="${col.data('ams-icon-on')} ${klass}"></i>`);
            } else {
                icon.replaceWith(`<i class="${col.data('ams-icon-off')} ${klass}"></i>`);
            }
        }
    },


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
