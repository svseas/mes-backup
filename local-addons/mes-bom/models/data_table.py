from odoo import models, fields, api

class DataTable(models.Model):
    _inherit = ['tech.process']
    _description = 'Data Table'

    @api.model
    def get_table_data(self):
        data = self.env['tech.process'].search([('child_process_ids', '!=', False)])
        pure_data = self.env['tech.process'].search([])

        result = []
        for record in data:
            output_names = [output.output.name for output in record.output if output.output]
            child_process_ids = [child.id for child in record.child_process_ids]
            child_process = self.get_child_process(child_process_ids)
            record_data = {
                'level': record.level if hasattr(record, 'level') else '1',
                'process_level': record.process_level if hasattr(record, 'process_level') else '1.1',
                'name': record.name,
                'child_process': child_process,
                'output_name': ', '.join(output_names),
            }
            result.append(record_data)


        # Define custom labels for each key
        table_keys = {
            'level': "Level",
            'process_level': "Bước CĐ",
            'name': "Công đoạn",
            'process_name': "Nội dung công đoạn",
            'output_name': 'Thành phần đầu ra',
            'Hình ảnh đầu ra': '',
            'Quy cách thành phần': '',
            'Mã sản phẩm': '',
            'Mã thành phần cấp 1': '',
            'Mã thành phần cấp 2': '',
            'Mã Nguyên liệu': '',
            'input_names': 'Tên nguyên liệu',
        }

        table_dict = {
            'Level': "level",
            'Bước CĐ': "process_level",
            "Công đoạn": 'name',
            'Nội dung công đoạn': "process_name",
            'Thành phần đầu ra': 'output_name',
            'Hình ảnh đầu ra': '',
            'Quy cách thành phần': '',
            'Mã sản phẩm': '',
            'Mã thành phần cấp 1': '',
            'Mã thành phần cấp 2': '',
            'Mã Nguyên liệu': '',
            'Tên nguyên liệu': 'input_names',
        }

        return result, table_keys, table_dict, pure_data.read()

    @api.model
    def get_child_process(self, ids):
        results = []
        for id in ids:
            data = self.env['tech.process'].search([('id', '=', id)])

            for record in data:
                output_names = [output.output.name for output in record.output if output.output]
                input_names = [input.name for input in record.input]

                cloned_child_process = {}
                if not input_names:
                    # Add the process with an empty string for input_names
                    cloned_child_process = {
                        'level': record.level if hasattr(record, 'level') else '2',
                        'process_level': record.process_level if hasattr(record, 'process_level') else '1.2',
                        'process_name': record.name,
                        'output_name': ', '.join(output_names),
                        'input_names': '',  # Empty string or any other indicator you prefer
                    }
                    results.append(cloned_child_process)

                for input_name in input_names:
                        # Clone the record data without creating new records in the database
                        cloned_child_process = {
                            'level': record.level if hasattr(record, 'level') else '2',
                            'process_level': record.process_level if hasattr(record, 'process_level') else '1.2',
                            'process_name': record.name,
                            'output_name': ', '.join(output_names),
                            'input_names': input_name,
                        }
                        results.append(cloned_child_process)
        return results
