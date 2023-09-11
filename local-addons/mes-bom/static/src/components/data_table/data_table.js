/**@odoo-module */
const { Component, onMounted, useState } = owl;
import { registry } from "@web/core/registry";
import { Nested } from "./nested.js";
const actionRegistry = registry.category("actions");
const rpc = require('web.rpc');
export class DataTable extends Component {
    setup(){
        super.setup(...arguments);
        this.dataTable = useState({ data: [],
                                    keys: [],
                                    dict: [],
                                    show: {},
                         })
        onMounted(()=>{
            this.loadData();
        })
    }

    static components = { Nested };
    loadData(){
        let self = this;
         rpc.query({
            model: 'tech.process',
            method: 'get_table_data',
         }).then(function(data){
             self.dataTable.data = data[0];
             self.dataTable.keys = data[1];
             self.dataTable.dict = data[2];
             console.log("Data=============: ", data)
         }).catch(function(error) {
            console.error('Error fetching data for ', error);
         });
    }
    toggleShow = (value) => {
        const newShowState = Object.assign({}, this.dataTable.show);
        newShowState[value] = !newShowState[value] || false;
        this.dataTable.show = newShowState;
        console.log("toggle===============", newShowState);
    }
}
DataTable.template = "mes-bom.DataTable";
actionRegistry.add("mes-bom.action_data_table_js", DataTable);