# -*- coding: utf-8 -*-
"""
===================================
Web 模板层 - HTML 页面生成
===================================

职责：
1. 生成 HTML 页面
2. 管理 CSS 样式
3. 提供可复用的页面组件
"""

from __future__ import annotations

import html
from typing import Optional


# ============================================================
# CSS 样式定义
# ============================================================

BASE_CSS = """
:root {
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --bg: #f8fafc;
    --card: #ffffff;
    --text: #1e293b;
    --text-light: #64748b;
    --border: #e2e8f0;
    --success: #10b981;
    --error: #ef4444;
    --warning: #f59e0b;
}

* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    margin: 0;
    padding: 20px;
}

.container {
    background: var(--card);
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    width: 100%;
    max-width: 1200px;
}

h2 {
    margin-top: 0;
    color: var(--text);
    font-size: 1.5rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.subtitle {
    color: var(--text-light);
    font-size: 0.875rem;
    margin-bottom: 2rem;
    line-height: 1.5;
}

.code-badge {
    background: #f1f5f9;
    padding: 0.2rem 0.4rem;
    border-radius: 0.25rem;
    font-family: monospace;
    color: var(--primary);
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--text);
}

textarea, input[type="text"] {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    font-family: monospace;
    font-size: 0.875rem;
    line-height: 1.5;
    resize: vertical;
    transition: border-color 0.2s, box-shadow 0.2s;
}

textarea:focus, input[type="text"]:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

button {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
    font-size: 1rem;
}

button:hover {
    background-color: var(--primary-hover);
    transform: translateY(-1px);
}

button:active {
    transform: translateY(0);
}

.btn-secondary {
    background-color: var(--text-light);
}

.btn-secondary:hover {
    background-color: var(--text);
}

.footer {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    color: var(--text-light);
    font-size: 0.75rem;
    text-align: center;
}

/* Toast Notification */
.toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    background: white;
    border-left: 4px solid var(--success);
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    opacity: 0;
    z-index: 1000;
}

.toast.show {
    transform: translateX(-50%) translateY(0);
    opacity: 1;
}

.toast.error {
    border-left-color: var(--error);
}

.toast.warning {
    border-left-color: var(--warning);
}

/* Helper classes */
.text-muted {
    font-size: 0.75rem;
    color: var(--text-light);
    margin-top: 0.5rem;
}

.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }

/* Section divider */
.section-divider {
    margin: 2rem 0;
    border: none;
    border-top: 1px solid var(--border);
}

/* Analysis section */
.analysis-section {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}

.analysis-section h3 {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text);
}

.input-group {
    display: flex;
    gap: 0.5rem;
}

.input-group input {
    flex: 1;
    resize: none;
}

.input-group button {
    width: auto;
    padding: 0.75rem 1.25rem;
    white-space: nowrap;
}

.btn-analysis {
    background-color: var(--success);
}

.btn-analysis:hover {
    background-color: #059669;
}

.btn-analysis:disabled {
    background-color: var(--text-light);
    cursor: not-allowed;
    transform: none;
}

/* Result box */
.result-box {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    display: none;
}

.result-box.show {
    display: block;
}

.result-box.success {
    background-color: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
}

.result-box.error {
    background-color: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
}

.result-box.loading {
    background-color: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1e40af;
}

.spinner {
    display: inline-block;
    width: 14px;
    height: 14px;
    border: 2px solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
    margin-right: 0.5rem;
    vertical-align: middle;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Task List Container */
.task-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-height: 600px;
    max-height: 600px;
    overflow-y: auto;
}

/* Task Grouping */
.task-group {
    margin-bottom: 0.75rem;
}

.group-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.4rem 0.5rem;
    font-size: 0.75rem;
    color: var(--text-light);
    cursor: pointer;
    user-select: none;
    background: rgba(0,0,0,0.02);
    border-radius: 0.375rem;
    margin-bottom: 0.25rem;
    transition: background 0.2s;
}

.group-header:hover {
    background: rgba(0,0,0,0.05);
}

.group-title {
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.group-header .arrow {
    font-size: 0.7rem;
    transition: transform 0.2s;
}

.group-header.collapsed .arrow {
    transform: rotate(-90deg);
}

.group-count {
    background: rgba(0,0,0,0.05);
    padding: 0.1rem 0.35rem;
    border-radius: 0.25rem;
    font-size: 0.7rem;
}

.group-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    transition: all 0.2s;
    overflow: hidden;
}

.group-content.collapsed {
    display: none;
}

/* Task Grouping */
.task-group {
    margin-bottom: 0.75rem;
}

.group-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.4rem 0.5rem;
    font-size: 0.75rem;
    color: var(--text-light);
    cursor: pointer;
    user-select: none;
    background: rgba(0,0,0,0.02);
    border-radius: 0.375rem;
    margin-bottom: 0.25rem;
    transition: background 0.2s;
}

.group-header:hover {
    background: rgba(0,0,0,0.05);
}

.group-title {
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.group-header .arrow {
    font-size: 0.7rem;
    transition: transform 0.2s;
}

.group-header.collapsed .arrow {
    transform: rotate(-90deg);
}

.group-count {
    background: rgba(0,0,0,0.05);
    padding: 0.1rem 0.35rem;
    border-radius: 0.25rem;
    font-size: 0.7rem;
}

.group-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    transition: all 0.2s;
    overflow: hidden;
}

.group-content.collapsed {
    display: none;
}

.task-list:empty::after {
    content: '暂无任务';
    display: block;
    text-align: center;
    color: var(--text-light);
    font-size: 0.8rem;
    padding: 1rem;
}

/* Task Card - Compact */
.task-card {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.75rem;
    background: var(--bg);
    border-radius: 0.5rem;
    border: 1px solid var(--border);
    font-size: 0.8rem;
    transition: all 0.2s;
}

.task-card:hover {
    border-color: var(--primary);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.task-card.running {
    border-color: var(--primary);
    background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
}

.task-card.completed {
    border-color: var(--success);
    background: linear-gradient(135deg, #ecfdf5 0%, #f8fafc 100%);
}

.task-card.failed {
    border-color: var(--error);
    background: linear-gradient(135deg, #fef2f2 0%, #f8fafc 100%);
}

/* Task Status Icon */
.task-status {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    flex-shrink: 0;
    font-size: 0.9rem;
}

.task-card.running .task-status {
    background: var(--primary);
    color: white;
}

.task-card.completed .task-status {
    background: var(--success);
    color: white;
}

.task-card.failed .task-status {
    background: var(--error);
    color: white;
}

.task-card.pending .task-status {
    background: var(--border);
    color: var(--text-light);
}

/* Task Main Info */
.task-main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.task-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: var(--text);
}

.task-title .code {
    font-family: monospace;
    background: rgba(0,0,0,0.05);
    padding: 0.1rem 0.3rem;
    border-radius: 0.25rem;
}

.task-title .name {
    color: var(--text-light);
    font-weight: 400;
    font-size: 0.75rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-meta {
    display: flex;
    gap: 0.75rem;
    font-size: 0.7rem;
    color: var(--text-light);
}

.task-meta span {
    display: flex;
    align-items: center;
    gap: 0.2rem;
}

/* Task Result Badge */
.task-result {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.15rem;
    flex-shrink: 0;
}

.task-advice {
    font-weight: 600;
    font-size: 0.75rem;
    padding: 0.15rem 0.4rem;
    border-radius: 0.25rem;
    background: var(--primary);
    color: white;
}

.task-advice.buy { background: #059669; }
.task-advice.sell { background: #dc2626; }
.task-advice.hold { background: #d97706; }
.task-advice.wait { background: #6b7280; }

.task-score {
    font-size: 0.7rem;
    color: var(--text-light);
}

/* Task Actions */
.task-actions {
    display: flex;
    gap: 0.25rem;
    flex-shrink: 0;
}

.task-btn {
    width: 24px;
    height: 24px;
    padding: 0;
    border-radius: 0.25rem;
    background: transparent;
    color: var(--text-light);
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.task-btn:hover {
    background: rgba(0,0,0,0.05);
    color: var(--text);
    transform: none;
}

/* Spinner in task */
.task-card .spinner {
    width: 12px;
    height: 12px;
    border-width: 1.5px;
    margin: 0;
}

/* Empty state hint */
.task-hint {
    text-align: center;
    padding: 0.75rem;
    color: var(--text-light);
    font-size: 0.75rem;
    background: var(--bg);
    border-radius: 0.375rem;
}

/* Task detail expand */
.task-detail {
    display: none;
    padding: 0.5rem 0.75rem;
    padding-left: 3rem;
    background: rgba(0,0,0,0.02);
    border-radius: 0 0 0.5rem 0.5rem;
    margin-top: -0.5rem;
    font-size: 0.75rem;
    border: 1px solid var(--border);
    border-top: none;
}

.task-detail.show {
    display: block;
}

.task-detail-row {
    display: flex;
    justify-content: space-between;
    padding: 0.25rem 0;
}

.task-detail-row .label {
    color: var(--text-light);
}

.task-detail-summary {
    margin-top: 0.5rem;
    padding: 0.5rem;
    background: white;
    border-radius: 0.25rem;
    line-height: 1.4;
}

/* 双列布局 */
.main-layout {
    display: grid;
    grid-template-columns: 360px 1fr;
    gap: 2rem;
    width: 100%;
}

.left-panel {
    min-width: 0;
}

.right-panel {
    min-width: 0;
    min-height: 400px;
    background: var(--bg);
    border-radius: 0.75rem;
    border: 2px dashed var(--border);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}

.right-panel.has-content {
    border-style: solid;
    border-color: var(--primary);
    background: white;
}

.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}

.result-header h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}

.result-header .close-btn {
    width: 28px;
    height: 28px;
    padding: 0;
    background: transparent;
    color: var(--text-light);
    border-radius: 0.25rem;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.result-header .close-btn:hover {
    background: var(--bg);
    color: var(--text);
    transform: none;
}

.result-header .action-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-detail {
    background: transparent;
    border: 1px solid var(--primary);
    color: var(--primary);
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    border-radius: 0.25rem;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-detail:hover {
    background: var(--primary);
    color: white;
}

.btn-detail.active {
    background: var(--primary);
    color: white;
}

.result-header .action-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn-detail {
    background: transparent;
    border: 1px solid var(--primary);
    color: var(--primary);
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    border-radius: 0.25rem;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-detail:hover {
    background: var(--primary);
    color: white;
}

.btn-detail.active {
    background: var(--primary);
    color: white;
}

.result-placeholder {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--text-light);
    text-align: center;
}

.result-placeholder .icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.result-placeholder p {
    margin: 0;
    font-size: 0.9rem;
}

/* Markdown 内容样式 */
.markdown-content {
    flex: 1;
    overflow-y: auto;
    font-size: 0.9rem;
    line-height: 1.6;
}

.markdown-content h1 {
    font-size: 1.5rem;
    margin: 0 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary);
}

.markdown-content h2 {
    font-size: 1.2rem;
    margin: 1.5rem 0 0.75rem 0;
    color: var(--text);
}

.markdown-content h3 {
    font-size: 1rem;
    margin: 1rem 0 0.5rem 0;
}

.markdown-content p {
    margin: 0.5rem 0;
}

.markdown-content ul, .markdown-content ol {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}

.markdown-content li {
    margin: 0.25rem 0;
}

.markdown-content strong {
    color: var(--text);
}

.markdown-content code {
    background: var(--bg);
    padding: 0.1rem 0.3rem;
    border-radius: 0.25rem;
    font-family: monospace;
    font-size: 0.85em;
}

.markdown-content pre {
    background: var(--bg);
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
}

.markdown-content pre code {
    background: transparent;
    padding: 0;
}

.markdown-content blockquote {
    margin: 0.5rem 0;
    padding: 0.5rem 1rem;
    border-left: 3px solid var(--primary);
    background: var(--bg);
    color: var(--text-light);
}

.markdown-content table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.5rem 0;
}

.markdown-content th, .markdown-content td {
    border: 1px solid var(--border);
    padding: 0.5rem;
    text-align: left;
}

.markdown-content th {
    background: var(--bg);
    font-weight: 600;
}

/* 响应式布局 - 手机端 */
@media (max-width: 768px) {
    body {
        padding: 10px;
        align-items: flex-start;
    }
    
    .container {
        padding: 1rem;
    }
    
    .main-layout {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .right-panel {
        min-height: 300px;
        order: 2;
    }
    
    .left-panel {
        order: 1;
    }
    
    h2 {
        font-size: 1.25rem;
    }
}

/* Tab 导航样式 */
.tab-nav {
    display: flex;
    gap: 0;
    border-bottom: 2px solid var(--border);
    margin-bottom: 1.5rem;
}

.tab-item {
    padding: 0.75rem 1.5rem;
    border: none;
    background: transparent;
    color: var(--text-light);
    font-size: 0.95rem;
    font-weight: 500;
    cursor: pointer;
    position: relative;
    transition: all 0.2s;
}

.tab-item:hover {
    color: var(--primary);
    background: rgba(37, 99, 235, 0.05);
}

.tab-item.active {
    color: var(--primary);
}

.tab-item.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--primary);
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

/* 大盘复盘页面样式 */
.market-page {
    height: 100%;
}

.market-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: var(--text-light);
}

.market-loading .spinner {
    width: 32px;
    height: 32px;
    border-width: 3px;
    margin-bottom: 1rem;
}

.market-error {
    text-align: center;
    padding: 2rem;
    color: var(--error);
}

.market-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}

.market-header h3 {
    margin: 0;
    font-size: 1.1rem;
}

.market-header .date-info {
    font-size: 0.85rem;
    color: var(--text-light);
}

.btn-refresh {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-light);
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: all 0.2s;
    width: auto;
}

.btn-refresh:hover {
    border-color: var(--primary);
    color: var(--primary);
    background: rgba(37, 99, 235, 0.05);
    transform: none;
}

.btn-refresh:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.market-report {
    flex: 1;
    overflow-y: auto;
}

/* 大盘复盘折叠样式 */
.market-collapse-header {
    display: flex;
    align-items: center;
    cursor: pointer;
    user-select: none;
    padding: 0.5rem 0;
    transition: all 0.2s;
}

.market-collapse-header:hover {
    opacity: 0.8;
}

.market-collapse-header .arrow {
    display: inline-block;
    width: 16px;
    height: 16px;
    margin-right: 0.5rem;
    transition: transform 0.3s ease;
    color: var(--text-light);
    font-size: 0.8rem;
}

.market-collapse-header.collapsed .arrow {
    transform: rotate(-90deg);
}

.market-collapse-content {
    overflow: hidden;
    transition: max-height 0.3s ease, opacity 0.3s ease;
    max-height: 5000px;
    opacity: 1;
}

.market-collapse-content.collapsed {
    max-height: 0;
    opacity: 0;
}
"""


# ============================================================
# 页面模板
# ============================================================

def render_base(
    title: str,
    content: str,
    extra_css: str = "",
    extra_js: str = ""
) -> str:
    """
    渲染基础 HTML 模板
    
    Args:
        title: 页面标题
        content: 页面内容 HTML
        extra_css: 额外的 CSS 样式
        extra_js: 额外的 JavaScript
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>{BASE_CSS}{extra_css}</style>
</head>
<body>
  {content}
  {extra_js}
</body>
</html>"""


def render_toast(message: str, toast_type: str = "success") -> str:
    """
    渲染 Toast 通知
    
    Args:
        message: 通知消息
        toast_type: 类型 (success, error, warning)
    """
    icon_map = {
        "success": "✅",
        "error": "❌",
        "warning": "⚠️"
    }
    icon = icon_map.get(toast_type, "ℹ️")
    type_class = f" {toast_type}" if toast_type != "success" else ""
    
    return f"""
    <div id="toast" class="toast show{type_class}">
        <span class="icon">{icon}</span> {html.escape(message)}
    </div>
    <script>
        setTimeout(() => {{
            document.getElementById('toast').classList.remove('show');
        }}, 3000);
    </script>
    """


def render_config_page(
    stock_list: str,
    env_filename: str,
    message: Optional[str] = None
) -> bytes:
    """
    渲染配置页面
    
    Args:
        stock_list: 当前自选股列表
        env_filename: 环境文件名
        message: 可选的提示消息
    """
    safe_value = html.escape(stock_list)
    toast_html = render_toast(message) if message else ""
    
    # 分析组件的 JavaScript - 支持多任务
    analysis_js = """
<script>
(function() {
    const codeInput = document.getElementById('analysis_code');
    const submitBtn = document.getElementById('analysis_btn');
    const taskList = document.getElementById('task_list');
    
    // 任务管理
    const tasks = new Map(); // taskId -> {task, pollCount}
    let pollInterval = null;
    const MAX_POLL_COUNT = 120; // 6 分钟超时：120 * 3000ms = 360000ms
    const POLL_INTERVAL_MS = 3000;
    const MAX_TASKS_DISPLAY = 10;
    
    // 允许输入数字和字母（支持港股 hkxxxxx 格式）
    codeInput.addEventListener('input', function(e) {
        // 转小写，只保留字母和数字
        this.value = this.value.toLowerCase().replace(/[^a-z0-9]/g, '');
        if (this.value.length > 8) {
            this.value = this.value.slice(0, 8);
        }
        updateButtonState();
    });
    
    // 回车提交
    codeInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (!submitBtn.disabled) {
                submitAnalysis();
            }
        }
    });
    
    // 更新按钮状态 - 支持 A股(6位数字) 或 港股(hk+5位数字)
    function updateButtonState() {
        const code = codeInput.value.trim().toLowerCase();
        const isAStock = /^\\d{6}$/.test(code);           // A股: 600519
        const isHKStock = /^hk\\d{5}$/.test(code);        // 港股: hk00700
        submitBtn.disabled = !(isAStock || isHKStock);
    }
    
    // 格式化时间
    function formatTime(isoString) {
        if (!isoString) return '-';
        const date = new Date(isoString);
        return date.toLocaleTimeString('zh-CN', {hour: '2-digit', minute: '2-digit', second: '2-digit'});
    }
    
    // 计算耗时
    function calcDuration(start, end) {
        if (!start) return '-';
        const startTime = new Date(start).getTime();
        const endTime = end ? new Date(end).getTime() : Date.now();
        const seconds = Math.floor((endTime - startTime) / 1000);
        if (seconds < 60) return seconds + 's';
        const minutes = Math.floor(seconds / 60);
        const remainSec = seconds % 60;
        return minutes + 'm' + remainSec + 's';
    }
    
    // 获取建议样式类
    function getAdviceClass(advice) {
        if (!advice) return '';
        if (advice.includes('买') || advice.includes('加仓')) return 'buy';
        if (advice.includes('卖') || advice.includes('减仓')) return 'sell';
        if (advice.includes('持有')) return 'hold';
        return 'wait';
    }
    
    // 渲染单个任务卡片
    function renderTaskCard(taskId, taskData) {
        const task = taskData.task || {};
        const status = task.status || 'pending';
        const code = task.code || taskId.split('_')[0];
        const result = task.result || {};
        
        let statusIcon = '⏳';
        let statusText = '等待中';
        if (status === 'running') { statusIcon = '<span class="spinner"></span>'; statusText = '分析中'; }
        else if (status === 'completed') { statusIcon = '✓'; statusText = '完成'; }
        else if (status === 'failed') { statusIcon = '✗'; statusText = '失败'; }
        
        let resultHtml = '';
        if (status === 'completed' && result.operation_advice) {
            const adviceClass = getAdviceClass(result.operation_advice);
            resultHtml = '<div class="task-result">' +
                '<span class="task-advice ' + adviceClass + '">' + result.operation_advice + '</span>' +
                '<span class="task-score">' + (result.sentiment_score || '-') + '分</span>' +
                '</div>';
        } else if (status === 'failed') {
            resultHtml = '<div class="task-result"><span class="task-advice sell">失败</span></div>';
        }
        
        return '<div class="task-card ' + status + '" id="task_' + taskId + '" onclick="showResult(\\''+taskId+'\\')">' +
            '<div class="task-status">' + statusIcon + '</div>' +
            '<div class="task-main">' +
                '<div class="task-title">' +
                    '<span class="code">' + code + '</span>' +
                    (result.name ? '<span class="name">' + result.name + '</span>' : '') +
                '</div>' +
                '<div class="task-meta">' +
                    '<span>⏱ ' + formatTime(task.start_time) + '</span>' +
                    '<span>⏳ ' + calcDuration(task.start_time, task.end_time) + '</span>' +
                '</div>' +
            '</div>' +
            resultHtml +
            '<div class="task-actions">' +
                '<button class="task-btn" onclick="event.stopPropagation();removeTask(\\''+taskId+'\\')">×</button>' +
            '</div>' +
        '</div>';
    }
    
    // 移除任务
    window.removeTask = function(taskId) {
        if (confirm('确定删除该任务历史记录？')) {
            // 先从前端移除以快速响应
            tasks.delete(taskId);
            renderAllTasks();
            checkStopPolling();
            
            // 后台发送删除请求
            fetch('/task/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'task_id=' + encodeURIComponent(taskId)
            }).then(r => r.json())
              .then(data => {
                  if (!data.success) {
                      console.error('删除失败:', data.error);
                  }
              })
              .catch(err => console.error('删除请求错误:', err));
        }
    };
    
    // 切换组展开状态
    window.toggleGroup = function(dateStr) {
        const groupContent = document.getElementById('group_content_' + dateStr);
        const groupHeader = document.getElementById('group_header_' + dateStr);
        if (groupContent && groupHeader) {
            const isCollapsed = groupContent.classList.contains('collapsed');
            if (isCollapsed) {
                groupContent.classList.remove('collapsed');
                groupHeader.classList.remove('collapsed');
            } else {
                groupContent.classList.add('collapsed');
                groupHeader.classList.add('collapsed');
            }
        }
    };

    // 渲染所有任务（分组显示）
    // 移除任务
    window.removeTask = function(taskId) {
        if (confirm('确定删除该任务历史记录？')) {
            // 先从前端移除以快速响应
            tasks.delete(taskId);
            renderAllTasks();
            checkStopPolling();
            
            // 后台发送删除请求
            fetch('/task/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'task_id=' + encodeURIComponent(taskId)
            }).then(r => r.json())
              .then(data => {
                  if (!data.success) {
                      console.error('删除失败:', data.error);
                  }
              })
              .catch(err => console.error('删除请求错误:', err));
        }
    };
    
    // 切换组展开状态
    window.toggleGroup = function(dateStr) {
        const groupContent = document.getElementById('group_content_' + dateStr);
        const groupHeader = document.getElementById('group_header_' + dateStr);
        if (groupContent && groupHeader) {
            const isCollapsed = groupContent.classList.contains('collapsed');
            if (isCollapsed) {
                groupContent.classList.remove('collapsed');
                groupHeader.classList.remove('collapsed');
            } else {
                groupContent.classList.add('collapsed');
                groupHeader.classList.add('collapsed');
            }
        }
    };

    // 渲染所有任务（分组显示）
    function renderAllTasks() {
        if (tasks.size === 0) {
            taskList.innerHTML = '<div class="task-hint">💡 输入股票代码开始分析</div>';
            return;
        }
        
        // 1. 分组
        const groups = {}; // date(YYYY-MM-DD) -> [taskData]
        const today = new Date().toLocaleDateString('zh-CN', {year:'numeric', month:'2-digit', day:'2-digit'}).replace(/\\//g, '-');
        
        tasks.forEach((taskData, taskId) => {
            let start = taskData.task?.start_time;
            let dateStr = '未知日期';
            if (start) {
                const d = new Date(start);
                dateStr = d.toLocaleDateString('zh-CN', {year:'numeric', month:'2-digit', day:'2-digit'}).replace(/\\//g, '-');
            }
            if (!groups[dateStr]) groups[dateStr] = [];
            groups[dateStr].push({ id: taskId, data: taskData });
        });
        
        // 2. 排序日期（倒序）
        const sortedDates = Object.keys(groups).sort((a, b) => b.localeCompare(a));
        
        // 1. 分组
        const groups = {}; // date(YYYY-MM-DD) -> [taskData]
        const today = new Date().toLocaleDateString('zh-CN', {year:'numeric', month:'2-digit', day:'2-digit'}).replace(/\\//g, '-');
        
        tasks.forEach((taskData, taskId) => {
            let start = taskData.task?.start_time;
            let dateStr = '未知日期';
            if (start) {
                const d = new Date(start);
                dateStr = d.toLocaleDateString('zh-CN', {year:'numeric', month:'2-digit', day:'2-digit'}).replace(/\\//g, '-');
            }
            if (!groups[dateStr]) groups[dateStr] = [];
            groups[dateStr].push({ id: taskId, data: taskData });
        });
        
        // 2. 排序日期（倒序）
        const sortedDates = Object.keys(groups).sort((a, b) => b.localeCompare(a));
        
        // 1. 分组
        const groups = {}; // date(YYYY-MM-DD) -> [taskData]
        const today = new Date().toLocaleDateString('zh-CN', {year:'numeric', month:'2-digit', day:'2-digit'}).replace(/\\//g, '-');
        
        tasks.forEach((taskData, taskId) => {
            let start = taskData.task?.start_time;
            let dateStr = '未知日期';
            if (start) {
                const d = new Date(start);
                dateStr = d.toLocaleDateString('zh-CN', {year:'numeric', month:'2-digit', day:'2-digit'}).replace(/\\//g, '-');
            }
            if (!groups[dateStr]) groups[dateStr] = [];
            groups[dateStr].push({ id: taskId, data: taskData });
        });
        
        // 2. 排序日期（倒序）
        const sortedDates = Object.keys(groups).sort((a, b) => b.localeCompare(a));
        
        let html = '';
        
        sortedDates.forEach(dateStr => {
            const groupTasks = groups[dateStr];
            // 组内按时间倒序
            groupTasks.sort((a, b) => (b.data.task?.start_time || '').localeCompare(a.data.task?.start_time || ''));
            
            const isToday = dateStr === today;
            const collapsedClass = isToday ? '' : 'collapsed'; // 今天默认展开，其他折叠
            
            html += '<div class="task-group">';
            
            // Group Header
            html += `<div class="group-header ${collapsedClass}" id="group_header_${dateStr}" onclick="toggleGroup('${dateStr}')">`;
            html += `<span class="group-title"><span class="arrow">▼</span> ${dateStr === today ? '📅 今天' : '📅 ' + dateStr}</span>`;
            html += `<span class="group-count">${groupTasks.length}</span>`;
            html += `</div>`;
            
            // Group Content
            html += `<div class="group-content ${collapsedClass}" id="group_content_${dateStr}">`;
            groupTasks.forEach(item => {
                html += renderTaskCard(item.id, item.data);
            });
            html += `</div>`; // end group-content
            
            html += '</div>'; // end task-group
        });
        
        sortedDates.forEach(dateStr => {
            const groupTasks = groups[dateStr];
            // 组内按时间倒序
            groupTasks.sort((a, b) => (b.data.task?.start_time || '').localeCompare(a.data.task?.start_time || ''));
            
            const isToday = dateStr === today;
            const collapsedClass = isToday ? '' : 'collapsed'; // 今天默认展开，其他折叠
            
            html += '<div class="task-group">';
            
            // Group Header
            html += `<div class="group-header ${collapsedClass}" id="group_header_${dateStr}" onclick="toggleGroup('${dateStr}')">`;
            html += `<span class="group-title"><span class="arrow">▼</span> ${dateStr === today ? '📅 今天' : '📅 ' + dateStr}</span>`;
            html += `<span class="group-count">${groupTasks.length}</span>`;
            html += `</div>`;
            
            // Group Content
            html += `<div class="group-content ${collapsedClass}" id="group_content_${dateStr}">`;
            groupTasks.forEach(item => {
                html += renderTaskCard(item.id, item.data);
            });
            html += `</div>`; // end group-content
            
            html += '</div>'; // end task-group
        });
        
        taskList.innerHTML = html;
    }
    
    // 显示分析结果到右侧面板
    window.showResult = function(taskId) {
        const taskData = tasks.get(taskId);
        if (!taskData || !taskData.task) return;
        
        const task = taskData.task;
        const result = task.result || {};
        const code = task.code || taskId.split('_')[0];
        
        // 构建 Markdown 内容
        let markdown = '';
        
        if (task.status === 'completed' && result.name) {
            markdown = '# ' + result.name + ' (' + code.toUpperCase() + ')\\n\\n';
            
            // 如果是详情模式，生成详细报告
            if (window.isDetailMode) {
                 markdown += generateDetailMarkdown(result, code);
            } else {
                // 标准模式
                if (result.operation_advice) {
                    markdown += '## 操作建议\\n';
                    markdown += '**' + result.operation_advice + '**';
                    if (result.sentiment_score) {
                        markdown += ' (评分: ' + result.sentiment_score + ')\\n\\n';
                    } else {
                        markdown += '\\n\\n';
                    }
                }
                
                if (result.trend_prediction) {
                    markdown += '## 趋势预测\\n';
                    markdown += result.trend_prediction + '\\n\\n';
                }
                
                if (result.analysis_summary) {
                    markdown += '## 分析摘要\\n';
                    markdown += result.analysis_summary + '\\n\\n';
                }
                
                if (result.full_analysis) {
                    markdown = result.full_analysis;
                }
            // 如果是详情模式，生成详细报告
            if (window.isDetailMode) {
                 markdown += generateDetailMarkdown(result, code);
            } else {
                // 标准模式
                if (result.operation_advice) {
                    markdown += '## 操作建议\\n';
                    markdown += '**' + result.operation_advice + '**';
                    if (result.sentiment_score) {
                        markdown += ' (评分: ' + result.sentiment_score + ')\\n\\n';
                    } else {
                        markdown += '\\n\\n';
                    }
                }
                
                if (result.trend_prediction) {
                    markdown += '## 趋势预测\\n';
                    markdown += result.trend_prediction + '\\n\\n';
                }
                
                if (result.analysis_summary) {
                    markdown += '## 分析摘要\\n';
                    markdown += result.analysis_summary + '\\n\\n';
                }
                
                if (result.full_analysis) {
                    markdown = result.full_analysis;
                }
            }
        } else if (task.status === 'running') {
            markdown = '# ' + code.toUpperCase() + '\\n\\n';
            markdown += '⏳ **正在分析中...**\\n\\n';
            markdown += '请稍候，分析完成后将自动更新结果。';
        } else if (task.status === 'failed') {
            markdown = '# ' + code.toUpperCase() + '\\n\\n';
            markdown += '❌ **分析失败**\\n\\n';
            if (task.error) {
                markdown += '错误信息: ' + task.error;
            }
        } else {
            markdown = '# ' + code.toUpperCase() + '\\n\\n';
            markdown += '暂无分析结果';
        }
        
        // 渲染 Markdown
        const panel = document.getElementById('result_panel');
        const placeholder = document.getElementById('result_placeholder');
        const content = document.getElementById('result_content');
        const title = document.getElementById('result_title');
        const markdownDiv = document.getElementById('markdown_content');
        const detailBtn = document.getElementById('btn_detail_toggle');
        
        // 保存当前查看的任务ID
        window.currentTaskId = taskId;
        const detailBtn = document.getElementById('btn_detail_toggle');
        
        // 保存当前查看的任务ID
        window.currentTaskId = taskId;
        
        panel.classList.add('has-content');
        placeholder.style.display = 'none';
        content.style.display = 'flex';
        content.style.flexDirection = 'column';
        content.style.flex = '1';
        
        // 更新按钮状态
        if (detailBtn) {
            if (task.status === 'completed' && result.name) {
                detailBtn.style.display = 'block';
                detailBtn.textContent = window.isDetailMode ? '返回摘要' : '查看详情';
                if (window.isDetailMode) {
                    detailBtn.classList.add('active');
                } else {
                    detailBtn.classList.remove('active');
                }
            } else {
                detailBtn.style.display = 'none';
            }
        }
        
        // 更新按钮状态
        if (detailBtn) {
            if (task.status === 'completed' && result.name) {
                detailBtn.style.display = 'block';
                detailBtn.textContent = window.isDetailMode ? '返回摘要' : '查看详情';
                if (window.isDetailMode) {
                    detailBtn.classList.add('active');
                } else {
                    detailBtn.classList.remove('active');
                }
            } else {
                detailBtn.style.display = 'none';
            }
        }
        
        title.textContent = result.name ? result.name + ' (' + code.toUpperCase() + ')' : code.toUpperCase() + ' 分析结果';
        
        if (typeof marked !== 'undefined') {
            markdownDiv.innerHTML = marked.parse(markdown);
        } else {
            markdownDiv.innerHTML = '<pre style="white-space: pre-wrap;">' + markdown.replace(/\\\\n/g, '\\n') + '</pre>';
        }
    };
    
    // 切换详情模式
    window.toggleDetailMode = function() {
        window.isDetailMode = !window.isDetailMode;
        if (window.currentTaskId) {
            window.showResult(window.currentTaskId);
        }
    };
    
    // 生成详细 Markdown (仿照 Python generate_dashboard_report)
    function generateDetailMarkdown(result, code) {
        let lines = [];
        const dashboard = result.dashboard || {};
        const core = dashboard.core_conclusion || {};
        const intel = dashboard.intelligence || {};
        const battle = dashboard.battle_plan || {};
        const data_persp = dashboard.data_perspective || {};
        
        // 核心结论
        if (dashboard) {
            const one_sentence = core.one_sentence || result.analysis_summary;
            const time_sense = core.time_sensitivity || '本周内';
            
            lines.push(`### 📌 核心结论\\n`);
            lines.push(`**${result.operation_advice}** | ${result.trend_prediction}\\n`);
            lines.push(`> **一句话决策**: ${one_sentence}\\n`);
            lines.push(`⏰ **时效性**: ${time_sense}\\n`);
        }
        
        // 重要信息
        if (intel) {
             lines.push(`### 📰 重要信息\\n`);
             
             if (intel.earnings_outlook) {
                 lines.push(`**📊 业绩预期**: ${intel.earnings_outlook}\\n`);
             }
             if (intel.sentiment_summary) {
                 lines.push(`**💭 舆情情绪**: ${intel.sentiment_summary}\\n`);
             }
             
             if (intel.risk_alerts && intel.risk_alerts.length > 0) {
                 lines.push(`\\n**🚨 风险警报**:`);
                 intel.risk_alerts.forEach(alert => lines.push(`- ${alert}`));
                 lines.push(``);
             }
             
             if (intel.positive_catalysts && intel.positive_catalysts.length > 0) {
                 lines.push(`\\n**✨ 利好催化**:`);
                 intel.positive_catalysts.forEach(cat => lines.push(`- ${cat}`));
                 lines.push(``);
             }
        }
        
        // 操盘点位 (Battle Plan)
        if (battle) {
             lines.push(`### 🎯 操作点位\\n`);
             
             const sniper = battle.sniper_points || {};
             if (sniper) {
                 lines.push(`| 买点 | 止损 | 目标 |`);
                 lines.push(`|---|---|---|`);
                 lines.push(`| ${sniper.ideal_buy || '-'} | ${sniper.stop_loss || '-'} | ${sniper.take_profit || '-'} |\\n`);
             }
             
             const pos = battle.position_strategy || {};
             if (pos) {
                 lines.push(`**持仓建议**: ${pos.suggested_position || '-'}`);
                 if (pos.entry_plan) lines.push(`- 建仓: ${pos.entry_plan}`);
                 if (pos.risk_control) lines.push(`- 风控: ${pos.risk_control}`);
                 lines.push(``);
             }
        }
        
        // 如果没有 Dashboard 数据，显示一些基础信息
        if (!dashboard || Object.keys(dashboard).length === 0) {
            lines.push(`*(暂无详细数据，显示基础分析)*\\n`);
            if (result.analysis_summary) lines.push(result.analysis_summary);
        }
        
        return lines.join('\\n');
    }
    
    // 切换详情模式
    window.toggleDetailMode = function() {
        window.isDetailMode = !window.isDetailMode;
        if (window.currentTaskId) {
            window.showResult(window.currentTaskId);
        }
    };
    
    // 生成详细 Markdown (仿照 Python generate_dashboard_report)
    function generateDetailMarkdown(result, code) {
        let lines = [];
        const dashboard = result.dashboard || {};
        const core = dashboard.core_conclusion || {};
        const intel = dashboard.intelligence || {};
        const battle = dashboard.battle_plan || {};
        const data_persp = dashboard.data_perspective || {};
        
        // 核心结论
        if (dashboard) {
            const one_sentence = core.one_sentence || result.analysis_summary;
            const time_sense = core.time_sensitivity || '本周内';
            
            lines.push(`### 📌 核心结论\\n`);
            lines.push(`**${result.operation_advice}** | ${result.trend_prediction}\\n`);
            lines.push(`> **一句话决策**: ${one_sentence}\\n`);
            lines.push(`⏰ **时效性**: ${time_sense}\\n`);
        }
        
        // 重要信息
        if (intel) {
             lines.push(`### 📰 重要信息\\n`);
             
             if (intel.earnings_outlook) {
                 lines.push(`**📊 业绩预期**: ${intel.earnings_outlook}\\n`);
             }
             if (intel.sentiment_summary) {
                 lines.push(`**💭 舆情情绪**: ${intel.sentiment_summary}\\n`);
             }
             
             if (intel.risk_alerts && intel.risk_alerts.length > 0) {
                 lines.push(`\\n**🚨 风险警报**:`);
                 intel.risk_alerts.forEach(alert => lines.push(`- ${alert}`));
                 lines.push(``);
             }
             
             if (intel.positive_catalysts && intel.positive_catalysts.length > 0) {
                 lines.push(`\\n**✨ 利好催化**:`);
                 intel.positive_catalysts.forEach(cat => lines.push(`- ${cat}`));
                 lines.push(``);
             }
        }
        
        // 操盘点位 (Battle Plan)
        if (battle) {
             lines.push(`### 🎯 操作点位\\n`);
             
             const sniper = battle.sniper_points || {};
             if (sniper) {
                 lines.push(`| 买点 | 止损 | 目标 |`);
                 lines.push(`|---|---|---|`);
                 lines.push(`| ${sniper.ideal_buy || '-'} | ${sniper.stop_loss || '-'} | ${sniper.take_profit || '-'} |\\n`);
             }
             
             const pos = battle.position_strategy || {};
             if (pos) {
                 lines.push(`**持仓建议**: ${pos.suggested_position || '-'}`);
                 if (pos.entry_plan) lines.push(`- 建仓: ${pos.entry_plan}`);
                 if (pos.risk_control) lines.push(`- 风控: ${pos.risk_control}`);
                 lines.push(``);
             }
        }
        
        // 如果没有 Dashboard 数据，显示一些基础信息
        if (!dashboard || Object.keys(dashboard).length === 0) {
            lines.push(`*(暂无详细数据，显示基础分析)*\\n`);
            if (result.analysis_summary) lines.push(result.analysis_summary);
        }
        
        return lines.join('\\n');
    }
    
    // 关闭结果面板
    window.closeResult = function() {
        const panel = document.getElementById('result_panel');
        const placeholder = document.getElementById('result_placeholder');
        const content = document.getElementById('result_content');
        
        panel.classList.remove('has-content');
        placeholder.style.display = 'flex';
        content.style.display = 'none';
    };
    


    
    // 轮询所有运行中的任务
    function pollAllTasks() {
        let hasRunning = false;
        
        tasks.forEach((taskData, taskId) => {
            const status = taskData.task?.status;
            if (status === 'running' || status === 'pending' || !status) {
                hasRunning = true;
                taskData.pollCount = (taskData.pollCount || 0) + 1;
                
                if (taskData.pollCount > MAX_POLL_COUNT) {
                    taskData.task = taskData.task || {};
                    taskData.task.status = 'failed';
                    taskData.task.error = '轮询超时';
                    return;
                }
                
                fetch('/task?id=' + encodeURIComponent(taskId))
                    .then(r => r.json())
                    .then(data => {
                        if (data.success && data.task) {
                            taskData.task = data.task;
                            renderAllTasks();
                        }
                    })
                    .catch(() => {});
            }
        });
        
        if (!hasRunning) {
            checkStopPolling();
        }
    }
    
    // 检查是否需要停止轮询
    function checkStopPolling() {
        let hasRunning = false;
        tasks.forEach((taskData) => {
            const status = taskData.task?.status;
            if (status === 'running' || status === 'pending' || !status) {
                hasRunning = true;
            }
        });
        
        if (!hasRunning && pollInterval) {
            clearInterval(pollInterval);
            pollInterval = null;
        }
    }
    
    // 开始轮询
    function startPolling() {
        if (!pollInterval) {
            pollInterval = setInterval(pollAllTasks, POLL_INTERVAL_MS);
        }
    }
    
    // 提交分析
    window.submitAnalysis = function() {
        const code = codeInput.value.trim().toLowerCase();
        const isAStock = /^\d{6}$/.test(code);
        const isHKStock = /^hk\d{5}$/.test(code);
        
        if (!(isAStock || isHKStock)) {
            return;
        }
        
        submitBtn.disabled = true;
        submitBtn.textContent = '提交中...';
        
        fetch('/analysis?code=' + encodeURIComponent(code))
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const taskId = data.task_id;
                    tasks.set(taskId, {
                        task: {
                            code: code,
                            status: 'running',
                            start_time: new Date().toISOString()
                        },
                        pollCount: 0
                    });
                    
                    renderAllTasks();
                    startPolling();
                    codeInput.value = '';
                    
                    // 立即轮询一次
                    setTimeout(() => {
                        fetch('/task?id=' + encodeURIComponent(taskId))
                            .then(r => r.json())
                            .then(d => {
                                if (d.success && d.task) {
                                    tasks.get(taskId).task = d.task;
                                    renderAllTasks();
                                }
                            });
                    }, 500);
                } else {
                    alert('提交失败: ' + (data.error || '未知错误'));
                }
            })
            .catch(error => {
                alert('请求失败: ' + error.message);
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = '🚀 分析';
                updateButtonState();
            });
    };
    
    // 初始化
    updateButtonState();
    
    // 加载历史任务
    fetch('/tasks?limit=50')
        .then(r => r.json())
        .then(data => {
            if (data.success && data.tasks) {
                data.tasks.forEach(task => {
                    // 恢复任务数据
                    tasks.set(task.task_id, { 
                        task: task, 
                        pollCount: 0 
                    });
                });
                renderAllTasks();
                // 如果有未完成的任务，继续轮询
                if (tasks.size > 0) {
                    checkStopPolling();
                    startPolling();
                }
            } else {
                renderAllTasks();
            }
        })
        .catch(err => {
            console.error('加载历史任务失败', err);
            renderAllTasks();
        });
    
    // 加载历史任务
    fetch('/tasks?limit=50')
        .then(r => r.json())
        .then(data => {
            if (data.success && data.tasks) {
                data.tasks.forEach(task => {
                    // 恢复任务数据
                    tasks.set(task.task_id, { 
                        task: task, 
                        pollCount: 0 
                    });
                });
                renderAllTasks();
                // 如果有未完成的任务，继续轮询
                if (tasks.size > 0) {
                    checkStopPolling();
                    startPolling();
                }
            } else {
                renderAllTasks();
            }
        })
        .catch(err => {
            console.error('加载历史任务失败', err);
            renderAllTasks();
        });
})();
</script>
"""
    
    content = f"""
  <div class="container">
    <h2>📊 A/H股分析</h2>
    
    <!-- Tab 导航 -->
    <div class="tab-nav">
      <button class="tab-item active" onclick="switchTab('stock')" id="tab_stock">📈 个股分析</button>
      <button class="tab-item" onclick="switchTab('market')" id="tab_market">🏦 每日大盘</button>
    </div>
    
    <!-- 个股分析 Tab -->
    <div id="content_stock" class="tab-content active">
      <div class="main-layout">
        <!-- 左侧面板：输入和任务列表 -->
        <div class="left-panel">
          <div class="analysis-section" style="margin-top: 0; padding-top: 0; border-top: none;">
            <div class="form-group" style="margin-bottom: 0.75rem;">
              <div class="input-group">
                <input 
                    type="text" 
                    id="analysis_code" 
                    placeholder="A股 600519 / 港股 hk00700"
                    maxlength="8"
                    autocomplete="off"
                />
                <button type="button" id="analysis_btn" class="btn-analysis" onclick="submitAnalysis()" disabled>
                  🚀 分析
                </button>
              </div>
            </div>
            <p class="text-muted" style="margin-top: 0.5rem;">💡 输入股票代码开始分析</p>
            
            <!-- 任务列表 -->
            <div id="task_list" class="task-list"></div>
          </div>
        </div>
        
        <!-- 右侧面板：分析结果展示 -->
        <div class="right-panel" id="result_panel">
          <div class="result-placeholder" id="result_placeholder">
            <div class="icon">📊</div>
            <p>分析结果将在这里展示</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">点击左侧任务卡片查看详情</p>
          </div>
          <div id="result_content" style="display: none;">
            <div class="result-header">
              <h3 id="result_title">分析结果</h3>
              <div class="action-group">
                  <button id="btn_detail_toggle" class="btn-detail" onclick="toggleDetailMode()" style="display: none;">查看详情</button>
                  <button class="close-btn" onclick="closeResult()">×</button>
              </div>
            </div>
            <div class="markdown-content" id="markdown_content"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 每日大盘 Tab -->
    <div id="content_market" class="tab-content">
      <div class="market-page">
        <div class="market-header">
          <div class="market-collapse-header" id="market_collapse_header" onclick="toggleMarketCollapse()">
            <span class="arrow">▼</span>
            <h3 style="margin: 0;">📊 大盘复盘</h3>
          </div>
          <span class="date-info" id="market_date"></span>
          <button class="btn-refresh" onclick="event.stopPropagation(); refreshMarketReview()" id="btn_refresh_market">🔄 刷新</button>
        </div>
        <div id="market_content" class="market-report market-collapse-content">
          <div class="market-loading">
            <span class="spinner"></span>
            <p>正在加载大盘复盘...</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <p>API: <code>/health</code> · <code>/analysis?code=xxx</code> · <code>/api/market/review</code></p>
    </div>
  </div>
  
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  
  <!-- Tab 切换和大盘复盘逻辑 -->
  <script>
    let marketLoaded = false;
    let marketLoading = false;
    
    function switchTab(tabName) {{
        // 切换 Tab 按钮状态
        document.querySelectorAll('.tab-item').forEach(btn => btn.classList.remove('active'));
        document.getElementById('tab_' + tabName).classList.add('active');
        
        // 切换内容区域
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById('content_' + tabName).classList.add('active');
        
        // 如果切换到大盘 Tab 且未加载，自动加载
        if (tabName === 'market' && !marketLoaded && !marketLoading) {{
            loadMarketReview();
        }}
    }}
    
    function loadMarketReview(forceRefresh = false) {{
        if (marketLoading) return;
        marketLoading = true;
        
        const contentDiv = document.getElementById('market_content');
        const dateSpan = document.getElementById('market_date');
        const refreshBtn = document.getElementById('btn_refresh_market');
        
        // 显示加载状态
        contentDiv.innerHTML = '<div class="market-loading"><span class="spinner"></span><p>正在加载大盘复盘...</p></div>';
        refreshBtn.disabled = true;
        refreshBtn.textContent = '加载中...';
        
        const url = forceRefresh ? '/api/market/review?refresh=1' : '/api/market/review';
        
        fetch(url)
            .then(r => r.json())
            .then(data => {{
                if (data.success && data.data) {{
                    const review = data.data;
                    dateSpan.textContent = review.date + ' 生成于 ' + new Date(review.generated_at).toLocaleTimeString('zh-CN');
                    
                    // 渲染 Markdown
                    if (typeof marked !== 'undefined' && review.report) {{
                        contentDiv.innerHTML = '<div class="markdown-content">' + marked.parse(review.report) + '</div>';
                    }} else {{
                        contentDiv.innerHTML = '<pre style="white-space: pre-wrap;">' + (review.report || '暂无内容') + '</pre>';
                    }}
                    
                    // 检查是否是今天的复盘，非今天的默认折叠
                    const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
                    const isToday = review.date === today;
                    const header = document.getElementById('market_collapse_header');
                    
                    if (!isToday && header) {{
                        // 非今天的复盘，默认折叠
                        header.classList.add('collapsed');
                        contentDiv.classList.add('collapsed');
                    }} else if (header) {{
                        // 今天的复盘，确保展开
                        header.classList.remove('collapsed');
                        contentDiv.classList.remove('collapsed');
                    }}
                    
                    marketLoaded = true;
                }} else {{
                    contentDiv.innerHTML = '<div class="market-error"><p>❌ 加载失败</p><p>' + (data.error || '未知错误') + '</p></div>';
                }}
            }})
            .catch(err => {{
                contentDiv.innerHTML = '<div class="market-error"><p>❌ 请求失败</p><p>' + err.message + '</p></div>';
            }})
            .finally(() => {{
                marketLoading = false;
                refreshBtn.disabled = false;
                refreshBtn.textContent = '🔄 刷新';
            }});
    }}
    
    function refreshMarketReview() {{
        marketLoaded = false;
        loadMarketReview(true);
    }}
    
    // 切换大盘复盘折叠状态
    function toggleMarketCollapse() {{
        const header = document.getElementById('market_collapse_header');
        const content = document.getElementById('market_content');
        
        if (header && content) {{
            const isCollapsed = content.classList.contains('collapsed');
            if (isCollapsed) {{
                header.classList.remove('collapsed');
                content.classList.remove('collapsed');
            }} else {{
                header.classList.add('collapsed');
                content.classList.add('collapsed');
            }}
        }}
    }}
  </script>
  
  {toast_html}
  {analysis_js}
"""
    
    page = render_base(
        title="A/H股自选配置 | WebUI",
        content=content
    )
    return page.encode("utf-8")


def render_error_page(
    status_code: int,
    message: str,
    details: Optional[str] = None
) -> bytes:
    """
    渲染错误页面
    
    Args:
        status_code: HTTP 状态码
        message: 错误消息
        details: 详细信息
    """
    details_html = f"<p class='text-muted'>{html.escape(details)}</p>" if details else ""
    
    content = f"""
  <div class="container" style="text-align: center;">
    <h2>😵 {status_code}</h2>
    <p>{html.escape(message)}</p>
    {details_html}
    <a href="/" style="color: var(--primary); text-decoration: none;">← 返回首页</a>
  </div>
"""
    
    page = render_base(
        title=f"错误 {status_code}",
        content=content
    )
    return page.encode("utf-8")
