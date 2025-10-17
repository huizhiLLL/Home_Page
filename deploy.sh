#!/bin/bash

# 个人主页部署脚本
# 此脚本提供在 GitHub Pages 上部署个人主页的指南和自动化步骤

# 注意：在 Windows 上，您可以使用 Git Bash 或 WSL 来运行此脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

# 帮助信息
show_help() {
    echo "${YELLOW}用法: ./deploy.sh [选项]${NC}"
    echo ""
    echo "选项:"
    echo "  install     安装项目依赖"
    echo "  run         在本地运行开发服务器"
    echo "  build       构建静态文件（准备部署）"
    echo "  deploy      部署到 GitHub Pages"
    echo "  help        显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  ./deploy.sh install  # 安装依赖"
    echo "  ./deploy.sh run      # 运行本地服务器"
};

# 安装依赖
install_deps() {
    echo -e "${GREEN}正在安装项目依赖...${NC}"
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}依赖安装成功！${NC}"
    else
        echo -e "${RED}依赖安装失败，请检查错误信息。${NC}"
        exit 1
    fi
};

# 运行开发服务器
run_dev() {
    echo -e "${GREEN}正在启动开发服务器...${NC}"
    echo -e "${YELLOW}服务器将在 http://localhost:5000 上运行${NC}"
    python app.py
};

# 构建静态文件
build_static() {
    echo -e "${GREEN}正在构建静态文件...${NC}"
    
    # 检查是否安装了必要的工具
    if ! command -v wget &> /dev/null; then
        echo -e "${RED}错误: 未找到 wget 命令，请先安装 wget。${NC}"
        exit 1
    fi
    
    # 创建静态文件目录
    mkdir -p static_build
    
    # 启动临时服务器（在后台运行）
    python app.py &
    SERVER_PID=$!
    
    # 等待服务器启动
    sleep 5
    
    # 下载首页内容
    wget -O static_build/index.html http://localhost:5000
    
    # 停止服务器
    kill $SERVER_PID
    
    echo -e "${GREEN}静态文件构建完成！文件已保存到 static_build 目录。${NC}"
    echo -e "${YELLOW}注意：对于 GitHub Pages 部署，您可能需要调整配置以使用静态站点生成器。${NC}"
};

# 部署到 GitHub Pages
deploy_gh_pages() {
    echo -e "${YELLOW}部署到 GitHub Pages 的指南：${NC}"
    echo ""
    echo "1. 确保您已经创建了一个 GitHub 仓库"
    echo "2. 根据您的需求选择以下方法之一进行部署："
    echo ""
    echo "方法一：使用 GitHub Actions 自动化部署（推荐）"
    echo "   - 在仓库中创建 .github/workflows/deploy.yml 文件"
    echo "   - 添加适当的 CI/CD 配置以自动部署 Flask 应用"
    echo ""
    echo "方法二：使用静态站点模式部署"
    echo "   - 运行 './deploy.sh build' 生成静态文件"
    echo "   - 将 static_build 目录中的文件推送到 GitHub 仓库的 gh-pages 分支"
    echo ""
    echo "方法三：使用 Vercel、Netlify 等平台部署"
    echo "   - 注册 Vercel 或 Netlify 账号"
    echo "   - 连接您的 GitHub 仓库"
    echo "   - 按照平台指引完成部署配置"
    echo ""
    echo "更多信息，请参考 Flask 和 GitHub Pages 的官方文档。"
};

# 主函数
main() {
    # 检查参数
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    # 根据参数执行相应的函数
    case "$1" in
        install)
            install_deps
            ;;
        run)
            run_dev
            ;;
        build)
            build_static
            ;;
        deploy)
            deploy_gh_pages
            ;;
        help)
            show_help
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
};

# 执行主函数
main "$@"