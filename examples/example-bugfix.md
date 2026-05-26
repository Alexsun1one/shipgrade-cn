# Example: Bugfix

User asks: 页面按钮点了没反应。

Ship-grade response:

1. 复现: 打开真实页面,收集 console/network。
2. 定位: 找到按钮 handler 和 API route。
3. 修复: 最小改动修 handler 或状态流。
4. 验证: 单测 + 浏览器点击 + 无 console error。
5. 写回: 记录 bug 根因和验证截图路径。
