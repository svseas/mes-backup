/**@odoo-module */
const { Component, onMounted, useState } = owl;
import { registry } from "@web/core/registry";
const actionRegistry = registry.category("actions");
const rpc = require('web.rpc');
export class DataTable extends Component {
    setup(){
        super.setup(...arguments);
        onMounted(()=>{
            this.renderTable();
        })
    }

    renderTable() {
        const self = this;
        const template = `
            <div>1</div>
        `;
//        self.$('.table-container').append(template)
        function creatTable(template) {
        self.$('.table-container').append(template)
        };
        console.log("Test============= ")
    }
}
DataTable.template = "mes-bom.DataTable";
actionRegistry.add("mes-bom.action_data_table_js", DataTable);