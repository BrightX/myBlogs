# myBlogs

> 基于Django开发的博客平台。

## 项目环境

* `Python` 3.7 

* `Django` 2.2
* `django-guardian` 对象级别权限管理

* `django-simple-captcha` 验证码
* `djangorestframework` API开发框架
* `xadmin` Django后台管理

## 关于`xadmin` 的安装与源码修改

* `xadmin`安装

```bash
pip3 install https://codeload.github.com/sshwsfc/xadmin/zip/django2
```

* 修改源码

  由于版本问题`xadmin`在开发过程中会报错：`TypeError: render() got an unexpected keyword argument 'renderer'` 

  需要将`xadmin\views\dashboard.py`的`def render(self, name, value, attrs=None)`修改为`def render(self, name, value, attrs=None, renderer=None)`

```python
# xadmin/views/dashboard.py

# def render(self, name, value, attrs=None):
def render(self, name, value, attrs=None, renderer=None):
    
```

