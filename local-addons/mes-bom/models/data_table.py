from odoo import models, fields, api
from bs4 import BeautifulSoup

class DataTable(models.Model):
    _inherit = ['tech.process']
    _description = 'Data Table'

    @api.model
    def get_table_data(self):
        data = self.env['tech.process'].search([('child_process_ids', '!=', False)])
        pure_data = self.env['tech.process'].search([])

        result = []
        for index, record in enumerate(data):
            output_names = [output.output.name for output in record.output if output.output]
            child_process_ids = [child.id for child in record.child_process_ids]
            child_process = self.get_child_process(child_process_ids, index)
            record_data = {
                'level': '1',
                'process_level': f'{index+1}',
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
            'material_code': '',
            'input_names': 'Tên nguyên liệu',
            'material_description': 'Mô tả',
            'material_designator': 'Designator (vị trí cắm)',
            'material_footprint': 'Footprint (kiểu chân)',
            'material_lib_ref': 'LibRef (số tham chiếu)',
            'material_mat_qty': 'Số lượng',
            'material_mat_uom': 'Đơn vị',
            'material_mat_waste': 'Hao hụt',
            'material_manufacturer_name': 'Nhà sản xuất',
            'Mã hàng NSX': 'Mã hàng NSX',
            'material_supplier_name': 'Nhà cung ứng',
            'Mã hàng NCC': 'Mã hàng NCC',
            'Thiết bị sử dụng': 'Thiết bị sử dụng',
            'Loại / mã TB': 'Loại / mã TB',
            'Thời gian sử dụng (h)': 'Thời gian sử dụng (h)',
            'Nhân công (h)': 'Nhân công (h)',
            'Loại nhân công': 'Loại nhân công',
            'Hướng dẫn thao tác': 'Hướng dẫn thao tác',
            'Ghi chú': 'Ghi chú',
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
            'Mô tả': 'Mô tả',
            'Designator (vị trí cắm)': 'Designator (vị trí cắm)',
            'Footprint (kiểu chân)': 'Footprint (kiểu chân)',
            'LibRef (số tham chiếu)': 'LibRef (số tham chiếu)',
            'Số lượng': 'Số lượng',
            'Đơn vị': 'Đơn vị',
            'Hao hụt': 'Hao hụt',
            'Nhà sản xuất': 'Nhà sản xuất',
            'Mã hàng NSX': 'Mã hàng NSX',
            'Nhà cung ứng': 'Nhà cung ứng',
            'Mã hàng NCC': 'Mã hàng NCC',
            'Thiết bị sử dụng': 'Thiết bị sử dụng',
            'Loại / mã TB': 'Loại / mã TB',
            'Thời gian sử dụng (h)': 'Thời gian sử dụng (h)',
            'Nhân công (h)': 'Nhân công (h)',
            'Loại nhân công': 'Loại nhân công',
            'Hướng dẫn thao tác': 'Hướng dẫn thao tác',
            'Ghi chú': 'Ghi chú',
        }

        return result, table_keys, table_dict, pure_data.read()

    @api.model
    def get_child_process(self, ids, parent_index):
        results = []
        process_level_counter = 1
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
                        'process_level': f'{parent_index+1}.{process_level_counter}',
                        'process_name': record.name,
                        'output_name': ', '.join(output_names),
                        'input_names': '',  # Empty string or any other indicator you prefer
                    }
                    results.append(cloned_child_process)

                for input_name in input_names:
                        # Clone the record data without creating new records in the database
                        cloned_child_process = {
                            'level': record.level if hasattr(record, 'level') else '2',
                            'process_level': f'{parent_index+1}.{process_level_counter}',
                            'process_name': record.name,
                            'output_name': ', '.join(output_names),
                            'input_names': input_name,
                        }

                        material_line = record.input.filtered(lambda line: line.name == input_name)
                        if material_line:
                            cloned_child_process['material_name'] = material_line.name
                            cloned_child_process['material_code'] = material_line.code
                            cloned_child_process['material_description'] = material_line.description
                            cloned_child_process['material_mat_qty'] = material_line.mat_qty
                            cloned_child_process['material_mat_uom'] = material_line.mat_uom
                            cloned_child_process['material_mat_waste'] = material_line.mat_waste
                            cloned_child_process['material_designator'] = material_line.designator
                            cloned_child_process['material_footprint'] = material_line.footprint
                            cloned_child_process['material_lib_ref'] = material_line.lib_ref
                            cloned_child_process['material_manufacturer_name'] = material_line.manufacturer_name
                            cloned_child_process['material_supplier_name'] = material_line.supplier_name

                        results.append(cloned_child_process)
            process_level_counter += 1
        return results
