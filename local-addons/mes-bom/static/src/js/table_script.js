var dataArray = [
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

odoo.define('mes-bom.table_script', function (require) {
    "use strict";
    var rpc = require('web.rpc');

    function getdata(modelNamesList) {
            // Helper function to fetch child names from 'material.material' model
            function getChildNames(childIds) {
                return rpc.query({
                    model: 'material.line',
                    method: 'search_read',
                    args: [[['id', 'in', childIds]], ['name']],
                });
            }
            // Loop through the list of model names
            for (var i = 0; i < modelNamesList.length; i++) {
                let modelName = modelNamesList[i]; // Use let instead of var
                // Fetch data from the server for the current model name
                rpc.query({
                    model: modelName,
                    method: 'search_read',
                }).then(function (data) {
                    if (modelName === 'tech.process') {
                        data.forEach(function (techProcessRecord) {
                            if (techProcessRecord.child_process_inputs.length > 0) {
                                var childIds = techProcessRecord.child_process_inputs;
                                // Fetch child names from 'material.line' model
                                getChildNames(childIds).then(function (childData) {
                                    // Process the fetched child data for each 'tech.process' record
                                    console.log('Giai đoạn' + ' ' + techProcessRecord.name + ':', techProcessRecord);
                                    console.log('Child names:', childData);
                                }).catch(function (error) {
                                    console.error('Error fetching child names for Tech Process Record:', techProcessRecord, error);
                                });
                            } else {
                                console.log('Giai đoạn' + ' ' + techProcessRecord.name + ':', techProcessRecord);
                            }
                        });
                    } else {
                        // Process the fetched data for models other than 'tech.process'
                        console.log('Data for ' + modelName + ':', data);
                    }
                }).catch(function (error) {
                    console.error('Error fetching data for ' + modelName + ':', error);
                });
            }
    }

    function createTableFromObjects(data) {
      const table = document.createElement('table');
      table.className = 'styled-table';

      const thead = document.createElement('thead');
      const headerRow = document.createElement('tr');

      // Create table header row
      const keys = Object.keys(data[0]);
      for (const key of keys) {
        const headerCell = document.createElement('th');
        headerCell.textContent = key;
        headerRow.appendChild(headerCell);
      }
      thead.appendChild(headerRow);
      table.appendChild(thead);

      // Create table data rows
      const tbody = document.createElement('tbody');
      for (const obj of data) {
        const dataRow = document.createElement('tr');
        for (const key of keys) {
          const dataCell = document.createElement('td');
          dataCell.textContent = obj[key];
          dataRow.appendChild(dataCell);
        }
        tbody.appendChild(dataRow);
      }
      table.appendChild(tbody);
      return table;
    }

    const table = createTableFromObjects(dataArray);
    const tableContainer = document.getElementById('table-container');
    tableContainer.appendChild(table);
    // Add your model names here
    const modelNamesList = ['tech.process'];
    getdata(modelNamesList);
})