/** @odoo-module **/

import { registry } from '@web/core/registry';
import { loadBundle } from "@web/core/assets";
const { Component} = owl;

var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');

export class MainPage extends Component {
    setup(){
    }
}

MainPage.template = 'mes-bom.MainPage'
registry.category('actions').add('mes-bom.action_main_page_js', MainPage);