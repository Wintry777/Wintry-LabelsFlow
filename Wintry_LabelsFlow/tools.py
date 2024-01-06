import os
import shutil
import warnings
import xml.etree.ElementTree as ET

from base import listdir, BaseLabels

class Labels(BaseLabels):
    def __init__(self, labels_path, verbose):
        super().__init__(labels_path, verbose)

    def xml_to_yolo(self, class_mapping):
        """
        将 XML 格式的标注文件转换为 YOLO 格式。

        :param class_mapping: dict，用于映射类名到类 ID。{'xml_classname': 'yolo_classid'}
        """

        process_count = 0
        for filename in self._labels:
            if filename.endswith('.xml'):
                tree = ET.parse(filename)
                root = tree.getroot()

                img_width = int(root.find('size').find('width').text)
                img_height = int(root.find('size').find('height').text)

                if os.path.exists(filename[:-4] + '.txt'):
                    shutil.rmtree(filename[:-4] + '.txt')
                with open(filename[:-4] + '.txt', 'w') as file:
                    for member in root.findall('object'):
                        class_name = member.find('name').text
                        class_id = class_mapping[class_name]

                        xmin = int(member.find('bndbox').find('xmin').text)
                        ymin = int(member.find('bndbox').find('ymin').text)
                        xmax = int(member.find('bndbox').find('xmax').text)
                        ymax = int(member.find('bndbox').find('ymax').text)

                        x_center = ((xmin + xmax) / 2) / img_width
                        y_center = ((ymin + ymax) / 2) / img_height
                        width = (xmax - xmin) / img_width
                        height = (ymax - ymin) / img_height

                        file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
                shutil.rmtree(filename)
                process_count += 1
        self.__print(f"已转换 {process_count} 个 xml 文件")


    def yolo_change_labels(self, label_mapping):
        """
        更改 yolo 格式的txt文件内的标签。
        :param label_mapping: dict，{'old':'new', ...}
                                old -> new
        """
        process_count = 0
        ext_list = self.__check_ext()
        old_dict = {}
        new_dict = {}

        if not self.__check_mapping(label_mapping):
            warnings.warn('映射字典应全为字符串格式，未执行任何操作！', category=Warning)
            return

        if '.txt' not in ext_list:
            warnings.warn("未检测到 yolo 格式文件，未执行任何操作！", category=Warning)
            return 0

        for file in listdir(path=self._labels_path, file_ext='.txt', with_ext=True, with_path='abspath'):
            with open(file, 'r') as fr:
                lines = fr.readlines()

            with open(file, 'w') as file:
                for line in lines:
                    elements = line.strip().split()
                    if elements and elements[0] in label_mapping:
                        old_dict[elements[0]] = old_dict.get(elements[0], 0) + 1
                        elements[0] = label_mapping[elements[0]]
                        new_dict[elements[0]] = new_dict.get(elements[0], 0) + 1
                        process_count += 1
                    elif elements:
                        old_dict[elements[0]] = old_dict.get(elements[0], 0) + 1
                        new_dict[elements[0]] = new_dict.get(elements[0], 0) + 1

                    file.write(' '.join(elements) + '\n')
        self.__print(f"已映射的标签数量：{process_count}")
        self.__print(f"Old_dict: {old_dict}")
        self.__print(f"New_Dict: {new_dict}")







