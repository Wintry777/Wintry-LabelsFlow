import os
import warnings

def listdir(path, file_ext='.txt', with_ext=True, with_path='False'):
    """
    以 list 形式返回目录下特定格式的文件。

    :param path: 目录的路径。推荐使用 os.path.join()
    :param file_ext: str, 返回文件的格式，默认为 '.txt'。
    :param with_ext: bool，返回文件是否包含拓展名。
    :param with_path: 指定返回文件名的形式。
                     - 'abs'、'abspath'、'True'、True: 绝对路径。
                     - 'rel'、'relpath': 相对路径。
                     - 'False'、False: 仅文件名。
    :return: list [符合指定格式的文件列表]
    """
    file_ext = str(file_ext)
    path = os.path.normpath(path)

    # 是否返回拓展名
    if file_ext != '.*':
        if with_ext or (with_ext == 'True'):
            filenames = [filename for filename in os.listdir(path) if filename.endswith(file_ext)]
        elif not with_ext or (with_ext == 'False'):
            filenames = [filename[:-len(file_ext)] for filename in os.listdir(path) if filename.endswith(file_ext)]
        else:
            filenames = [filename for filename in os.listdir(path) if filename.endswith(file_ext)]
            warnings.warn("不标准的 with_ext 格式，请检查文档。默认参数: True", category=Warning)
    else:
        if with_ext or (with_ext == 'True'):
            filenames = [filename for filename in os.listdir(path)]
        elif not with_ext or (with_ext == 'False'):
            filenames = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
        else:
            filenames = [filename for filename in os.listdir(path)]
            warnings.warn("不标准的 with_ext 格式，请检查文档。默认参数: True", category=Warning)

    # 是否带目录返回
    if with_path in ['abs', 'abspath', True, 'True']:
        abspath = os.path.abspath(path)
        filenames = [os.path.join(abspath, filename) for filename in filenames]
    elif with_path in ['rel', 'relpath']:
        relpath = os.path.relpath(path)
        filenames = [os.path.join('.', relpath, filename) for filename in filenames]
    elif with_path in [False, 'False']:
        pass
    else:
        warnings.warn("不标准的 with_path 格式，请检查文档。默认参数: False", category=Warning)

    return filenames


class BaseLabels(object):
    """
    实现对标签文件的操作

    基础属性:
        path 目录路径
        info()
    """

    def __init__(self, labels_path, verbose=False):
        """

        :param labels_path: list，存放标签文件的目录
        :param verbose: bool，是否需要输出
        """
        self._labels_path = labels_path
        self._labels = listdir(self._labels_path, file_ext='.*', with_ext=True, with_path='abspath')
        self._verbose = verbose
        self.__re_init()

    def __re_init(self):
        self.path = os.path.abspath(self._labels_path)
        self._extensions_counts = self.__ext_init()
        self._length = len(self._labels)
        self._info = self.__info_load()\




    def info(self):
        print('===')
        for key in (self._info.keys()):
            print(f'{key}:', self._info[key])
        print('===')



    def __print(self, msg):
        if self._verbose:
            print(msg)


    def __ext_init(self):
        """获取记录目录文件格式的字典"""
        extensions_counts = {}
        for filename in os.listdir(self._labels_path):
            _, ext = os.path.splitext(filename)
            if ext in extensions_counts:
                extensions_counts[ext] += 1
            else:
                extensions_counts[ext] = 1
        return extensions_counts

    def __check_ext(self):
        """
        检查 Labels 的拓展名
        :return:
        """
        if len(self._extensions_counts) == 1:
            return list(self._extensions_counts.keys())[0]
        else:
            return list(self._extensions_counts.keys())

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
            'Path': self.path,
            'counts': self._length,
            'extensions': list(self._extensions_counts.keys()),
            'extensions_counts': self._extensions_counts,
            'verbose': self._verbose,
        }

        return info
