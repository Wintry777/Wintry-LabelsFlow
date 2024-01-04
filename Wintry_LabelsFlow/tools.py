import os
import shutil
import warnings
import xml.etree.ElementTree as ET

def listdir(path, format='.txt', withends=True, withpath='False'):
    """
    以 list 形式返回目录下特定格式的文件。

    :param path: 目录的路径。推荐使用 os.path.join()
    :param format: str, 返回文件的格式，默认为 '.txt'。
    :param withends: bool，返回文件是否包含拓展名。
    :param withpath: 指定返回文件名的形式。
                     - 'abs'、'abspath'、'True'、True: 绝对路径。
                     - 'rel'、'relpath': 相对路径。
                     - 'False'、False: 仅文件名。
    :return: 符合指定格式的文件列表。
    """
    format = str(format)
    path = os.path.normpath(path)
    if format != '.*':
        if (withends == True) or (withends == 'True'):
            filenames = [filename for filename in os.listdir(path) if filename.endswith(format)]
        elif (withends == False) or (withends == 'False'):
            filenames = [filename[:-len(format)] for filename in os.listdir(path) if filename.endswith(format)]
        else:
            filenames = [filename for filename in os.listdir(path) if filename.endswith(format)]
            warnings.warn("不标准的 withends 格式，请检查文档。默认参数: True", category=Warning)
    else:
        if (withends == True) or (withends == 'True'):
            filenames = [filename for filename in os.listdir(path)]
        elif (withends == False) or (withends == 'False'):
            filenames = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
        else:
            filenames = [filename for filename in os.listdir(path)]
            warnings.warn("不标准的 withends 格式，请检查文档。默认参数: True", category=Warning)



    if withpath in ['abs', 'abspath', True, 'True']:
        abspath = os.path.abspath(path)
        filenames = [os.path.join(abspath, filename) for filename in filenames]
    elif withpath in ['rel', 'relpath']:
        relpath = os.path.relpath(path)
        filenames = [os.path.join('.', relpath, filename) for filename in filenames]
    elif withpath in [False, 'False']:
        pass
    else:
        warnings.warn("不标准的 withpath 格式，请检查文档。默认参数: False", category=Warning)

    return filenames


class Labels(object):
    """
    实现对标签文件的操作

    """

    def __init__(self, labels_path, verbose=False):
        """

        :param labels_path: list，存放标签文件的目录
        :param verbose: bool，是否需要输出
        """
        self._labels_path = labels_path
        self._labels = listdir(self._labels_path, format='.*', withends=True, withpath='abspath')
        self._verbose = verbose
        self.__re_init()


    def __re_init(self):
        self._extensions = self.__ext_init()
        self._length = len(self._labels)
        self._info = self.__info_load()



    def path(self):
        return self._labels_path


    def info(self):
        print('===')
        for key in (self._info.keys()):
            print(f'{key}:', self._info[key])
        print('===')



    def __print(self, msg):
        if self._verbose:
            print(msg)


    def yolo_change_labels(self, label_mapping):
        """
        更改 yolo 格式的txt文件内的标签。
        :param label_mapping: dict，{'0':'1', ...}
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

        for file in listdir(path=self._labels_path, format='.txt', withends=True, withpath='abspath'):
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


    def __ext_init(self):
        extensions = {}
        for filename in os.listdir(self._labels_path):
            _, ext = os.path.splitext(filename)
            if ext in extensions:
                extensions[ext] += 1
            else:
                extensions[ext] = 1
        return extensions

    def __check_ext(self):
        """
        检查 Labels 的拓展名
        :return:
        """
        if len(self._extensions) == 1:
            return list(self._extensions.keys())[0]
        else:
            return list(self._extensions.keys())

    def __check_mapping(self, mapping):
        """
        检查字典中所有的键和值是否都是字符串。

        :param mapping: 待检查的字典。
        :return: 如果所有键和值都是字符串，返回 True，否则返回 False。
        """
        for key, value in mapping.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
        return True


    def __info_load(self):
        """
        描述实例的信息
        """
        info = {
            'Path': self._labels_path,
            'length': self._length,
            'extensions': list(self._extensions.keys()),
            'extensions_counts': self._extensions,
            'verbose': self._verbose,


        }

        return info








