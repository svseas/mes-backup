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
            child_process_names = [child.name for child in record.child_process_ids]
            output_names = [output.output.name for output in record.output if output.output]
            # This will trigger the compute method
            record.child_process_inputs
            child_input_names = [input.name for input in record.child_process_inputs]
            record_data = {
                'level': record.level if hasattr(record, 'level') else '1',
                'process_level': record.process_level if hasattr(record, 'process_level') else '',
                'name': record.name,
                'process_names': ', '.join(child_process_names),
                'output_names': ', '.join(output_names),
                'child_input_names': ', '.join(child_input_names),
            }
            result.append(record_data)

        # Define custom labels for each key
        table_keys = {
            'level': "Level",
            'process_level': "Bước CĐ",
            'name': "Công đoạn",
            'process_names': "Nội dung công đoạn",
            'output_names': 'Thành phần đầu ra',
            'Hình ảnh đầu ra': '',
            'Quy cách thành phần': '',
            'Mã sản phẩm': '',
            'Mã thành phần cấp 1': '',
            'Mã thành phần cấp 2': '',
            'Mã Nguyên liệu': '',
            'child_input_names': 'Tên nguyên liệu',
        }

        table_dict = {
            'Level': "level",
            'Bước CĐ': "process_level",
            "Công đoạn": 'name',
            'Nội dung công đoạn': "process_names",
            'Thành phần đầu ra': 'output_names',
            'Hình ảnh đầu ra': '',
            'Quy cách thành phần': '',
            'Mã sản phẩm': '',
            'Mã thành phần cấp 1': '',
            'Mã thành phần cấp 2': '',
            'Mã Nguyên liệu': '',
            'Tên nguyên liệu': 'child_input_names',
        }

        return result, table_keys, table_dict, pure_data.read()
