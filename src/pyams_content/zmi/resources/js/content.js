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
    },


    /**
     * Paragraphs management
     */
    paragraphs: {

        switchEditor: (event) => {
            const
                target = $(event.currentTarget),
                switcher = $('.switcher', target),
                editor = target.siblings('.editor');
            if (switcher.hasClass('expanded')) {
                MyAMS.core.clearContent(editor).then(() => {
                    editor.empty();
                    switcher.html('<i class="far fa-plus-square"></i>')
                        .removeClass('expanded');
                });
            } else {
                switcher.html('<i class="fas fa-spinner fa-spin"></i>');
                MyAMS.require('ajax', 'helpers').then(() => {
                    const
                        tr = target.parents('tr'),
                        objectName = tr.data('ams-element-name'),
                        table = tr.parents('table'),
                        location = table.data('ams-location');
                    MyAMS.ajax.post(`${location}/get-paragraph-editor.json`, {
                        object_name: objectName
                    }).then((result) => {
                        const content = result[objectName];
                        if (content) {
                            editor.html(content);
                            MyAMS.core.initContent(editor).then(() => {
                                MyAMS.helpers.scrollTo('#content', editor, {
                                    offset: -15
                                });
                            });
                        }
                    }).finally(() => {
                        switcher.html('<i class="far fa-minus-square"></i>')
                            .addClass('expanded');
                    });
                });
            }
        },

        switchAllEditors: (event) => {
            const
                target = $(event.currentTarget),
                switcher = $('.switcher', target),
                table = target.parents('table'),
                tbody = $('tbody', table);
            if (switcher.hasClass('expanded')) {
                $('tr', tbody).each((idx, elt) => {
                    const editor = $('.editor', elt);
                    MyAMS.core.clearContent(editor).then(() => {
                        editor.empty();
                        $('.switcher', elt).html('<i class="far fa-plus-square"></i>')
                            .removeClass('expanded');
                    });
                });
                switcher.html('<i class="far fa-plus-square"></i>')
                    .removeClass('expanded');
            } else {
                switcher.html('<i class="fas fa-spinner fa-spin"></i>');
                MyAMS.require('ajax', 'helpers').then(() => {
                    const location = table.data('ams-location');
                    MyAMS.ajax.post(`${location}/get-paragraphs-editors.json`).then((result) => {
                        for (const [name, form] of Object.entries(result)) {
                            const
                                row = $(`tr[data-ams-element-name="${name}"]`, tbody),
                                rowSwitcher = $('.switcher', row);
                            if (!rowSwitcher.hasClass('expanded')) {
                                const editor = $('.editor', row);
                                editor.html(form);
                                MyAMS.core.initContent(editor).then(() => {
                                    rowSwitcher.html('<i class="far fa-minus-square"></i>')
                                        .addClass('expanded');
                                });
                            }
                        }
                    }).finally(() => {
                        switcher.html('<i class="far fa-minus-square"></i>')
                            .addClass('expanded');
                    });
                });
            }
        },

        refreshTitle: (form, params) => {
            const
                row = $(`tr[data-ams-element-name="${params.element_name}"]`);
            $('.title', row).text(params.title);
        }
    },


    /**
     * Reviews management
     */
    review: {

        // Review comments timer
        timer: null,
        interval: 30000,

        // Scroll messages list to last message
        init: () => {
            $(document).off('update-comments.ams.content')
                .on('update-comments.ams.content', (evt, {count}) => {
                    const menu = $('a[href="#review-comments.html"]', $('nav'));
                    if (menu.exists()) {
                        $('.badge', menu).text(count);
                    }
                });
            const review = MyAMS.content.review;
            review.timer = setTimeout(review.getComments, review.interval);
        },

        initPage: () => {
            MyAMS.require('helpers').then(() => {
                const
                    messages = $('#review-messages-view'),
                    lastMessage = $('li', messages).last();
                if (messages.exists()) {
                    MyAMS.helpers.scrollTo(messages, lastMessage);
                }
            });
        },

        getComments: () => {
            MyAMS.require('ajax', 'helpers').then(() => {
                const
                    review = MyAMS.content.review,
                    menu = $('a[href="#review-comments.html"]', $('nav')),
                    badge = $('.badge', menu);
                MyAMS.ajax.get('get-comments.json', {
                    count: badge.text() || '0'
                }).then(({status, comments, count}, xhrStatus, xhr) => {
                    if (count !== parseInt(badge.text())) {
                        badge.removeClass('bg-info')
                            .addClass('bg-danger scaled');
                        badge.text(count);
                        setTimeout(() => {
                            badge.removeClass('bg-danger scaled')
                                .addClass('bg-info');
                        }, 10000);
                    }
                    if (comments) {
                        const
                            messagesView = $('#review-messages-view'),
                            messagesList = $('#review-messages');
                        for (const comment of comments) {
                            messagesList.append($(comment));
                        }
                        MyAMS.helpers.scrollTo(messagesView, $('li', messagesList).last());
                    }
                    review.timer = setTimeout(review.getComments, review.interval);
                });
            })
        }
    },


    /**
     * Thesaurus management
     */
    thesaurus: {

        /**
         * Update extracts list on selected thesaurus change
         *
         * @param evt: source change event
         */
        changeThesaurus: (evt) => {
            const
                form = $(evt.currentTarget).parents('form'),
                thesaurus = $('select[name$=".widgets.thesaurus_name"]', form),
                thesaurus_name = thesaurus.val(),
                extract = $('select[name$=".widgets.extract_name"]', form),
                plugin = extract.data('select2');
            extract.empty();
            extract.select2('data', null);
            plugin.results.clear();
            if (thesaurus_name) {
                MyAMS.require('ajax').then(() => {
                    MyAMS.ajax.get('/api/thesaurus/extracts', {
                        'thesaurus_name': thesaurus_name
                    }).then((result) => {
                        $('<option />')
                            .attr('id', 'form-widgets-extract_name-novalue')
                            .attr('value', '--NOVALUE--')
                            .text(MyAMS.i18n.NO_SELECTED_VALUE)
                            .appendTo(extract);
                        $(result.results).each((idx, elt) => {
                            $('<option />')
                                .attr('id', `form-widgets-extract_name-${idx}`)
                                .attr('value', elt.id)
                                .text(elt.text)
                                .appendTo(extract);
                        });
                        extract.val('--NOVALUE--').trigger('change');
                    });
                })
            }
        }
    }
};


if (window.MyAMS) {
    MyAMS.config.modules.push('content');
    MyAMS.content = content;
    console.debug("MyAMS: content module loaded...");
}
