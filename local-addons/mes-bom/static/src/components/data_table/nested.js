/** @odoo-module */

import { Component, useState, xml, onWillUpdateProps } from "@odoo/owl";


export class Nested extends Component {
    static props = ["data",
                    "dataTable",
    ]
    setup(){
        this.state = useState({show: false,
                               isClick: false,
        })

//        onWillUpdateProps(nextProps => {
//          return this.state.show = !this.props.isToggle[this.props.btnIndex];
//        });
    }
    static template = xml`
        <button class="btn btn-primary" t-on-click="() => { state.isClick = !state.isClick; state.show = !state.show; }">
            <t t-if="state.isClick">-</t>
            <t t-else="">+</t>
        </button>
        <t class="nest-child" t-if="state.show">

            <t t-set="processed_names" t-value="[]"/>

            <t t-foreach="props.data" t-as="child_record" t-key="child_record_index">
                <t t-if="processed_names.includes(child_record['process_name'])">
                    <tr>
                        <t t-foreach="props.dataTable.keys" t-as="key" t-key="key_index">
                            <t t-if="child_record[key]">
                                <t t-if="!['level', 'process_level', 'process_name', 'output_name', 'name'].includes(key)">
                                    <td>
                                        <t t-out="child_record[key]"/>
                                    </td>
                                </t>
                                <t t-else="">
                                    <td>
                                        <t t-out="''"/>
                                    </td>
                                </t>
                            </t>
                            <t t-else="">
                                <td>
                                    <t t-out="'Enter ' + key"/>
                                </td>
                            </t>
                        </t>
                    </tr>
                </t>
                <t t-else="">
                    <t t-set="processed_names" t-value="processed_names + [child_record['process_name']]"/>
                    <tr>
                        <t t-foreach="props.dataTable.keys" t-as="key" t-key="key_index">
                            <td>
                                <t t-if="child_record[key]">
                                    <t t-out="child_record[key]"/>
                                </t>
                                <t t-else="">
                                    <t t-out="'Enter ' + key"/>
                                </t>
                            </td>
                        </t>
                    </tr>
                </t>
            </t>

        </t>
    `
}