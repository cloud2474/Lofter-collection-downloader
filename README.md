# Lofter-collection-downloader
用于批量下载lofter中我的喜欢中的图片

使用方法：
1. 登录 lofter
2. 启用开发者工具，依次打开 Network → fetch/XHR，刷新页面，点击任意一个以 `.dwr` 结尾的文件，在 Header 中复制 cookie
3. 粘贴 cookie 到源代码对应位置，运行程序

默认下载喜欢中最新的10个作品。修改amount可定义保存的作品数量，修改index可定义从第几个作品开始下载。

NOT BETA WE DIE LIKE A MAN(?
