/**@odoo-module */
const { Component, onMounted, useState } = owl;
import { registry } from "@web/core/registry";
const actionRegistry = registry.category("actions");
const rpc = require('web.rpc');
export class DataTable extends Component {
    setup(){
        super.setup(...arguments);
        this.dataTable = useState({ data: [] })
        onMounted(()=>{
            this.loadData();
        })
    }
    loadData(){
        let self = this;
         rpc.query({
            model: 'tech.process',
            method: 'get_table_data',
            }).then(function(data){
                self.dataTable.data = data;
                console.log("Data=============: ", data)
        });
    }
}
DataTable.template = "mes-bom.DataTable";
actionRegistry.add("mes-bom.action_data_table_js", DataTable);