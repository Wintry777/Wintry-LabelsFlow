# Base

此文档用于记录 `base.py` 中的主要功能、函数、类定义及其相关属性和方法。

## 函数

### `listdir()`

以 list 形式返回目录下特定格式的文件。

```python
listdir(path, file_ext='.txt', with_ext=True, with_path='False')
```

- `path`: 标签的路径(必须为文件夹目录)
- `file_ext`(默认为`.txt`): 指定哪些格式的文件传入
  - `.*` 传入所有格式的文件。
- `with_ext`(默认为`True`): `bool`，返回的列表中，是否要包含拓展名。
- `with_path`(默认为`False`): `str`(或`bool`)，返回的列表中，是否要包含完整路径。
  - `abs`, `abspath`, `True`: 绝对路径。
  - `rel`, `relpath`: 相对路径。
  - `False`: 仅文件名。

## 类

### `BaseLabels(object)`

基础实现标签类别的读取，一般作为基类继承。



