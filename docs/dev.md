# 难度

* 该应用程序能够作为选项卡 UI 运行并无限期地保持活动状态。
    - 这意味着不能使用活动线程。 应用程序只能等待空闲直到被用户交互触发。
    - 解决方案：命令执行由TextView委托直接调用。
      主级用户输入没有活动的阅读线程（不像运行具有活动读取线程以等待用户数据的脚本）。
      
* ObjC 调用很慢，尤其是对于大型文本构建和渲染
    - 如果我们简单地为每个文本更改重建和替换整个文本缓冲区，这是非常低效的。
    - 解决方案：顺序编辑。
      

# 设计


