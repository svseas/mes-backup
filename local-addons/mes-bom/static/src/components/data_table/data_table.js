/** @odoo-module */

import { loadBundle } from "@web/core/assets";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
const dataArray = [
  {   level: 1,
      process_code: 'John',
      process_name: 30,
      process_desc: "",
      output: "",
      output_image: "",
      ingredient: "",
      product_code: "",
      component_code_1: "",
      component_code_2: "",
      material_code: "",
      material_name: "",
  },
    {   level: 1,
      process_code: 'John',
      process_name: 30,
      process_desc: "",
      output: "",
      output_image: "",
      ingredient: "",
      product_code: "",
      component_code_1: "",
      component_code_2: "",
      material_code: "",
      material_name: "",
  },
];

var DataTable = AbstractAction.extend({
    template: 'mes-bom.DataTable'

    start: function() {
        this.set("title", 'DataTable');
        this.renderTable(); // Assuming you have a renderTable method
        return this._super();
    },

    renderTable: function() {
        const self = this;
        const tableContainer = self.$el.find('#table-container'); // Assuming you have a container with this ID
        const table = document.createElement('table');

        tableContainer.append(table); // Append the table to the container
    },
});

core.action_registry.add('mes-bom.action_data_table_js', DataTable);
return DataTable;