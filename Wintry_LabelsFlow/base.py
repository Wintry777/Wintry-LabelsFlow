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

    if with_path in ['abs', 'abspath', True, 'True']:
        abspath = os.path.abspath(path)
        filenames = [os.path.join(abspath, filename) for filename in filenames]
    elif with_path in ['rel', 'relpath']:
        relpath = os.path.relpath(path)
        filenames = [os.path.join('.', relpath, filename) for filename in filenames]
    elif with_path in [False, 'False']:
        pass
    else:
        warnings.warn("不标准的 withpath 格式，请检查文档。默认参数: False", category=Warning)

    return filenames

if __name__ == "__main__":
    print(listdir('../tests/data', file_ext='.*'))