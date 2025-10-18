#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自定义静态文件构建脚本
这个脚本将直接调用app.py中的功能来生成静态HTML文件
"""
import os
import sys
import shutil
import importlib.util

# 设置工作目录
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

# 设置静态文件目录为项目根目录
static_dir = here
print(f"将在项目根目录 {static_dir} 生成静态文件")

print("正在准备生成静态文件...")

# 导入app.py并调用其中的generate_static_html函数
try:
    # 动态导入app.py
    spec = importlib.util.spec_from_file_location("app", os.path.join(here, "app.py"))
    app_module = importlib.util.module_from_spec(spec)
    sys.modules["app"] = app_module
    spec.loader.exec_module(app_module)
    
    # 确保generate_static_html函数存在
    if hasattr(app_module, 'generate_static_html'):
            # 调用generate_static_html函数生成静态文件
            success = app_module.generate_static_html(static_dir=static_dir)
            
            if not success:
                print("错误：生成静态文件失败")
                sys.exit(1)
    else:
        print("错误：app.py中未找到generate_static_html函数")
        
        # 尝试备选方案：使用Flask测试客户端
        if hasattr(app_module, 'app'):
            print("尝试使用Flask测试客户端获取页面内容...")
            
            # 使用Flask测试客户端
            client = app_module.app.test_client()
            response = client.get('/')
            
            if response.status_code == 200:
                # 保存HTML内容到根目录
                html_path = os.path.join(static_dir, 'index.html')
                
                # 确认是否已有index.html文件，如果有则备份
                if os.path.exists(html_path):
                    backup_path = os.path.join(static_dir, 'index.html.bak')
                    shutil.copy(html_path, backup_path)
                    print(f"已备份现有index.html文件到: {backup_path}")
                
                with open(html_path, 'wb') as f:
                    f.write(response.data)
                
                print(f"静态HTML文件已保存到项目根目录: {html_path}")
            else:
                print(f"错误：无法获取首页内容，状态码: {response.status_code}")
                sys.exit(1)
        else:
            print("错误：app.py中既未找到generate_static_html函数，也未找到app实例")
            sys.exit(1)

except Exception as e:
    print(f"错误：生成静态文件时出现异常: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 复制其他必要的静态资源到根目录
print("正在复制其他静态资源...")
for file in ['background.jpg', '1background.jpg']:
    src = os.path.join(here, 'static_build', file)
    if not os.path.exists(src):
        # 如果在static_build目录中找不到，则尝试在当前目录查找
        src = os.path.join(here, file)
    
    if os.path.exists(src):
        dst = os.path.join(static_dir, file)
        # 确认是否已有该资源文件，如果有则备份
        if os.path.exists(dst):
            backup_path = f"{dst}.bak"
            shutil.copy(dst, backup_path)
            print(f"已备份现有资源文件到: {backup_path}")
        
        shutil.copy(src, dst)
        print(f"已复制资源文件: {file}")

print("\n静态文件构建完成！")
print(f"\n静态HTML文件已生成在项目根目录: {os.path.join(static_dir, 'index.html')}")
print(f"\n如何部署到GitHub Pages:")
print("方式一：手动部署")
print("1. 确保您已经在项目根目录")
print("2. 添加并提交所有文件")
print("3. 将文件推送到GitHub仓库的gh-pages分支")
print("\n手动部署示例命令：")
print("git add index.html background.jpg 1background.jpg")
print("git commit -m 'Deploy to GitHub Pages'")
print("git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git")
print("git push origin master:gh-pages")
print("\n方式二：自动部署（已配置GitHub Actions）")
print("1. GitHub Actions将在每天UTC时间0点（北京时间8点）自动运行")
print("2. 也可以通过GitHub仓库的Actions页面手动触发运行")
print("3. 自动构建会生成静态文件并提交到当前分支")
print("\n注意：")
print("1. 您需要将YOUR_USERNAME和YOUR_REPO替换为您的GitHub用户名和仓库名")
print("2. 确保GitHub仓库有正确的权限配置，GitHub Actions默认可以访问仓库内容")
print("3. 如果仓库是私有的，可能需要额外配置secrets")