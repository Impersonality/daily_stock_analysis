# -*- coding: utf-8 -*-
"""
===================================
Web 服务层 - 业务逻辑
===================================

职责：
1. 配置管理服务 (ConfigService)
2. 分析任务服务 (AnalysisService)
"""

from __future__ import annotations

import os
import re
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# ============================================================
# 配置管理服务
# ============================================================

_ENV_PATH = os.getenv("ENV_FILE", ".env")

_STOCK_LIST_RE = re.compile(
    r"^(?P<prefix>\s*STOCK_LIST\s*=\s*)(?P<value>.*?)(?P<suffix>\s*)$"
)


class ConfigService:
    """
    配置管理服务
    
    负责 .env 文件中 STOCK_LIST 的读写操作
    """
    
    def __init__(self, env_path: Optional[str] = None):
        self.env_path = env_path or _ENV_PATH
    
    def read_env_text(self) -> str:
        """读取 .env 文件内容"""
        try:
            with open(self.env_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def write_env_text(self, text: str) -> None:
        """写入 .env 文件内容"""
        with open(self.env_path, "w", encoding="utf-8") as f:
            f.write(text)
    
    def get_stock_list(self) -> str:
        """获取当前自选股列表字符串"""
        env_text = self.read_env_text()
        return self._extract_stock_list(env_text)
    
    def set_stock_list(self, stock_list: str) -> str:
        """
        设置自选股列表
        
        Args:
            stock_list: 股票代码字符串（逗号或换行分隔）
            
        Returns:
            规范化后的股票列表字符串
        """
        env_text = self.read_env_text()
        normalized = self._normalize_stock_list(stock_list)
        updated = self._update_stock_list(env_text, normalized)
        self.write_env_text(updated)
        return normalized
    
    def get_env_filename(self) -> str:
        """获取 .env 文件名"""
        return os.path.basename(self.env_path)
    
    def _extract_stock_list(self, env_text: str) -> str:
        """从环境文件中提取 STOCK_LIST 值"""
        for line in env_text.splitlines():
            m = _STOCK_LIST_RE.match(line)
            if m:
                raw = m.group("value").strip()
                # 去除引号
                if (raw.startswith('"') and raw.endswith('"')) or \
                   (raw.startswith("'") and raw.endswith("'")):
                    raw = raw[1:-1]
                return raw
        return ""
    
    def _normalize_stock_list(self, value: str) -> str:
        """规范化股票列表格式"""
        parts = [p.strip() for p in value.replace("\n", ",").split(",")]
        parts = [p for p in parts if p]
        return ",".join(parts)
    
    def _update_stock_list(self, env_text: str, new_value: str) -> str:
        """更新环境文件中的 STOCK_LIST"""
        lines = env_text.splitlines(keepends=False)
        out_lines: List[str] = []
        replaced = False
        
        for line in lines:
            m = _STOCK_LIST_RE.match(line)
            if not m:
                out_lines.append(line)
                continue
            
            out_lines.append(f"{m.group('prefix')}{new_value}{m.group('suffix')}")
            replaced = True
        
        if not replaced:
            if out_lines and out_lines[-1].strip() != "":
                out_lines.append("")
            out_lines.append(f"STOCK_LIST={new_value}")
        
        trailing_newline = env_text.endswith("\n") if env_text else True
        out = "\n".join(out_lines)
        return out + ("\n" if trailing_newline else "")


# ============================================================
# 分析任务服务
# ============================================================

class AnalysisService:
    """
    分析任务服务
    
    负责：
    1. 管理异步分析任务
    2. 执行股票分析
    3. 触发通知推送
    """
    
    _instance: Optional['AnalysisService'] = None
    _lock = threading.Lock()
    
    def __init__(self, max_workers: int = 3):
        self._executor: Optional[ThreadPoolExecutor] = None
        self._max_workers = max_workers
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._tasks_lock = threading.RLock()
        
        # 初始化时加载任务
        self._load_tasks()
        self._tasks_lock = threading.RLock()
        
        # 初始化时加载任务
        self._load_tasks()
    
    @classmethod
    def get_instance(cls) -> 'AnalysisService':
        """获取单例实例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    @property
    def executor(self) -> ThreadPoolExecutor:
        """获取或创建线程池"""
        if self._executor is None:
            self._executor = ThreadPoolExecutor(
                max_workers=self._max_workers,
                thread_name_prefix="analysis_"
            )
        return self._executor

    def _get_task_file_path(self) -> str:
        """获取任务持久化文件路径"""
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tasks.json")

    def _load_tasks(self) -> None:
        """从文件加载任务"""
        task_file = self._get_task_file_path()
        if not os.path.exists(task_file):
            return

        try:
            import json
            with open(task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 清理3天前的数据
            now = datetime.now()
            valid_tasks = {}
            has_changes = False
            
            for task_id, task in data.items():
                start_time_str = task.get('start_time')
                if not start_time_str:
                    continue
                    
                try:
                    start_time = datetime.fromisoformat(start_time_str)
                    # 保留3天内的任务 (72小时)
                    if (now - start_time).total_seconds() <= 3 * 24 * 3600:
                        valid_tasks[task_id] = task
                    else:
                        has_changes = True
                except ValueError:
                    continue
            
            with self._tasks_lock:
                self._tasks = valid_tasks
                
            if has_changes:
                self._save_tasks()
                
            logger.info(f"[AnalysisService] 已加载 {len(self._tasks)} 个历史任务")
        except Exception as e:
            logger.error(f"[AnalysisService] 加载任务失败: {e}")

    def _save_tasks(self) -> None:
        """保存任务到文件"""
        task_file = self._get_task_file_path()
        try:
            import json
            # 确保data目录存在
            os.makedirs(os.path.dirname(task_file), exist_ok=True)
            
            with self._tasks_lock:
                # 再次执行清理，确保保存时也不包含过期数据
                now = datetime.now()
                tasks_to_save = {}
                for task_id, task in self._tasks.items():
                    start_time_str = task.get('start_time')
                    if start_time_str:
                        try:
                            start_time = datetime.fromisoformat(start_time_str)
                            if (now - start_time).total_seconds() <= 3 * 24 * 3600:
                                tasks_to_save[task_id] = task
                        except ValueError:
                            pass
                
                with open(task_file, 'w', encoding='utf-8') as f:
                    json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[AnalysisService] 保存任务失败: {e}")

    def _get_task_file_path(self) -> str:
        """获取任务持久化文件路径"""
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tasks.json")

    def _load_tasks(self) -> None:
        """从文件加载任务"""
        task_file = self._get_task_file_path()
        if not os.path.exists(task_file):
            return

        try:
            import json
            with open(task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 清理3天前的数据
            now = datetime.now()
            valid_tasks = {}
            has_changes = False
            
            for task_id, task in data.items():
                start_time_str = task.get('start_time')
                if not start_time_str:
                    continue
                    
                try:
                    start_time = datetime.fromisoformat(start_time_str)
                    # 保留3天内的任务 (72小时)
                    if (now - start_time).total_seconds() <= 3 * 24 * 3600:
                        valid_tasks[task_id] = task
                    else:
                        has_changes = True
                except ValueError:
                    continue
            
            with self._tasks_lock:
                self._tasks = valid_tasks
                
            if has_changes:
                self._save_tasks()
                
            logger.info(f"[AnalysisService] 已加载 {len(self._tasks)} 个历史任务")
        except Exception as e:
            logger.error(f"[AnalysisService] 加载任务失败: {e}")

    def _save_tasks(self) -> None:
        """保存任务到文件"""
        task_file = self._get_task_file_path()
        try:
            import json
            # 确保data目录存在
            os.makedirs(os.path.dirname(task_file), exist_ok=True)
            
            with self._tasks_lock:
                # 再次执行清理，确保保存时也不包含过期数据
                now = datetime.now()
                tasks_to_save = {}
                for task_id, task in self._tasks.items():
                    start_time_str = task.get('start_time')
                    if start_time_str:
                        try:
                            start_time = datetime.fromisoformat(start_time_str)
                            if (now - start_time).total_seconds() <= 3 * 24 * 3600:
                                tasks_to_save[task_id] = task
                        except ValueError:
                            pass
                
                with open(task_file, 'w', encoding='utf-8') as f:
                    json.dump(tasks_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[AnalysisService] 保存任务失败: {e}")
    
    def submit_analysis(self, code: str) -> Dict[str, Any]:
        """
        提交异步分析任务
        
        Args:
            code: 股票代码
            
        Returns:
            任务信息字典
        """
        task_id = f"{code}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # 提交到线程池
        self.executor.submit(self._run_analysis, code, task_id)
        
        logger.info(f"[AnalysisService] 已提交股票 {code} 的分析任务, task_id={task_id}")
        
        return {
            "success": True,
            "message": "分析任务已提交，将异步执行并推送通知",
            "code": code,
            "task_id": task_id
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        with self._tasks_lock:
            return self._tasks.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否删除成功
        """
        with self._tasks_lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                self._save_tasks()
                logger.info(f"[AnalysisService] 已删除任务: {task_id}")
                return True
            return False
    
    def list_tasks(self, limit: int = 100) -> List[Dict[str, Any]]:
        """列出最近的任务（自动清理过期数据）"""
        # 每次列出时触发一次加载/清理（确保数据是最新的且已清理）
        # 注意：这里为了性能，如果是频繁调用，应该优化。目前假设调用频率不高。
        # self._load_tasks() # 频繁IO不好，改为仅内存清理
        

    def delete_task(self, task_id: str) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否删除成功
        """
        with self._tasks_lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                self._save_tasks()
                logger.info(f"[AnalysisService] 已删除任务: {task_id}")
                return True
            return False
    
    def list_tasks(self, limit: int = 100) -> List[Dict[str, Any]]:
        """列出最近的任务（自动清理过期数据）"""
        # 每次列出时触发一次加载/清理（确保数据是最新的且已清理）
        # 注意：这里为了性能，如果是频繁调用，应该优化。目前假设调用频率不高。
        # self._load_tasks() # 频繁IO不好，改为仅内存清理
        
        with self._tasks_lock:
            # 内存中清理过期数据
            now = datetime.now()
            expired_ids = []
            for task_id, task in self._tasks.items():
                start_time_str = task.get('start_time')
                if start_time_str:
                    try:
                        start_time = datetime.fromisoformat(start_time_str)
                        if (now - start_time).total_seconds() > 3 * 24 * 3600:
                            expired_ids.append(task_id)
                    except ValueError:
                        pass
            
            for tid in expired_ids:
                del self._tasks[tid]
            
            if expired_ids:
                # 异步保存清理结果，不阻塞读取
                threading.Thread(target=self._save_tasks).start()

            # 内存中清理过期数据
            now = datetime.now()
            expired_ids = []
            for task_id, task in self._tasks.items():
                start_time_str = task.get('start_time')
                if start_time_str:
                    try:
                        start_time = datetime.fromisoformat(start_time_str)
                        if (now - start_time).total_seconds() > 3 * 24 * 3600:
                            expired_ids.append(task_id)
                    except ValueError:
                        pass
            
            for tid in expired_ids:
                del self._tasks[tid]
            
            if expired_ids:
                # 异步保存清理结果，不阻塞读取
                threading.Thread(target=self._save_tasks).start()

            tasks = list(self._tasks.values())
            
            
        # 按开始时间倒序
        tasks.sort(key=lambda x: x.get('start_time', ''), reverse=True)
        return tasks[:limit]
    
    def _run_analysis(self, code: str, task_id: str) -> Dict[str, Any]:
        """
        执行单只股票分析
        
        内部方法，在线程池中运行
        """
        # 初始化任务状态
        with self._tasks_lock:
            self._tasks[task_id] = {
                "task_id": task_id,
                "code": code,
                "status": "running",
                "start_time": datetime.now().isoformat(),
                "result": None,
                "error": None
            }
        self._save_tasks() # 保存初始状态
        self._save_tasks() # 保存初始状态
        
        try:
            # 延迟导入避免循环依赖
            from config import get_config
            from main import StockAnalysisPipeline
            
            logger.info(f"[AnalysisService] 开始分析股票: {code}")
            
            # 创建分析管道
            config = get_config()
            pipeline = StockAnalysisPipeline(config=config, max_workers=1)
            
            # 执行单只股票分析（启用单股推送）
            result = pipeline.process_single_stock(
                code=code,
                skip_analysis=False,
                single_stock_notify=True
            )
            
            if result:
                # 使用 to_dict() 保留所有字段，包括 dashboard
                result_data = result.to_dict()
                # 使用 to_dict() 保留所有字段，包括 dashboard
                result_data = result.to_dict()
                
                with self._tasks_lock:
                    self._tasks[task_id].update({
                        "status": "completed",
                        "end_time": datetime.now().isoformat(),
                        "result": result_data
                    })
                self._save_tasks() # 保存完成状态
                self._save_tasks() # 保存完成状态
                
                logger.info(f"[AnalysisService] 股票 {code} 分析完成: {result.operation_advice}")
                return {"success": True, "task_id": task_id, "result": result_data}
            else:
                with self._tasks_lock:
                    self._tasks[task_id].update({
                        "status": "failed",
                        "end_time": datetime.now().isoformat(),
                        "error": "分析返回空结果"
                    })
                self._save_tasks() # 保存失败状态
                self._save_tasks() # 保存失败状态
                
                logger.warning(f"[AnalysisService] 股票 {code} 分析失败: 返回空结果")
                return {"success": False, "task_id": task_id, "error": "分析返回空结果"}
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[AnalysisService] 股票 {code} 分析异常: {error_msg}")
            
            with self._tasks_lock:
                self._tasks[task_id].update({
                    "status": "failed",
                    "end_time": datetime.now().isoformat(),
                    "error": error_msg
                })
            self._save_tasks() # 保存异常状态
            self._save_tasks() # 保存异常状态
            
            return {"success": False, "task_id": task_id, "error": error_msg}


# ============================================================
# 大盘复盘服务
# ============================================================

class MarketService:
    """
    大盘复盘服务
    
    负责：
    1. 生成/缓存每日大盘复盘
    2. 持久化存储复盘数据
    """
    
    _instance: Optional['MarketService'] = None
    _lock = threading.Lock()
    
    def __init__(self):
        self._reviews: Dict[str, Dict[str, Any]] = {}
        self._reviews_lock = threading.RLock()
        self._load_reviews()
    
    @classmethod
    def get_instance(cls) -> 'MarketService':
        """获取单例实例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def _get_review_file_path(self) -> str:
        """获取复盘持久化文件路径"""
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "market_reviews.json")
    
    def _load_reviews(self) -> None:
        """从文件加载复盘数据"""
        review_file = self._get_review_file_path()
        if not os.path.exists(review_file):
            return
        
        try:
            import json
            with open(review_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 清理7天前的数据
            now = datetime.now()
            valid_reviews = {}
            
            for date_str, review in data.items():
                try:
                    review_date = datetime.strptime(date_str, '%Y-%m-%d')
                    if (now - review_date).days <= 7:
                        valid_reviews[date_str] = review
                except ValueError:
                    continue
            
            with self._reviews_lock:
                self._reviews = valid_reviews
            
            logger.info(f"[MarketService] 已加载 {len(self._reviews)} 条复盘历史")
        except Exception as e:
            logger.error(f"[MarketService] 加载复盘数据失败: {e}")
    
    def _save_reviews(self) -> None:
        """保存复盘数据到文件"""
        review_file = self._get_review_file_path()
        try:
            import json
            os.makedirs(os.path.dirname(review_file), exist_ok=True)
            
            with self._reviews_lock:
                with open(review_file, 'w', encoding='utf-8') as f:
                    json.dump(self._reviews, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[MarketService] 保存复盘数据失败: {e}")
    
    def get_today_review(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        获取今日大盘复盘
        
        Args:
            force_refresh: 是否强制刷新（忽略缓存）
            
        Returns:
            复盘数据字典
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 检查缓存
        if not force_refresh:
            with self._reviews_lock:
                if today in self._reviews:
                    logger.info(f"[MarketService] 使用缓存的今日复盘")
                    return self._reviews[today]
        
        # 生成新的复盘
        try:
            logger.info("[MarketService] 开始生成今日大盘复盘...")
            
            from market_analyzer import MarketAnalyzer
            from analyzer import GeminiAnalyzer
            from search_service import SearchService
            from config import get_config
            
            config = get_config()
            
            # 检查搜索服务可用性（任一搜索引擎 API key 可用即可）
            has_search = bool(config.bocha_api_keys or config.tavily_api_keys or config.serpapi_keys)
            search_service = SearchService(
                bocha_keys=config.bocha_api_keys,
                tavily_keys=config.tavily_api_keys,
                serpapi_keys=config.serpapi_keys
            ) if has_search else None
            
            # 创建 analyzer 用于调用 LLM
            stock_analyzer = None
            has_llm = bool(config.gemini_api_key or config.openai_api_key)
            if has_llm:
                stock_analyzer = GeminiAnalyzer()  # 内部自动从 get_config() 获取配置
            
            market_analyzer = MarketAnalyzer(
                search_service=search_service,
                analyzer=stock_analyzer
            )
            
            # 获取市场概览
            overview = market_analyzer.get_market_overview()
            
            # 搜索市场新闻
            news = market_analyzer.search_market_news()
            
            # 生成复盘报告
            report = market_analyzer.generate_market_review(overview, news)
            
            # 构建返回数据
            review_data = {
                "date": today,
                "report": report,
                "generated_at": datetime.now().isoformat(),
                "overview": {
                    "indices": [idx.to_dict() for idx in overview.indices],
                    "up_count": overview.up_count,
                    "down_count": overview.down_count,
                    "flat_count": overview.flat_count,
                    "limit_up_count": overview.limit_up_count,
                    "limit_down_count": overview.limit_down_count,
                    "total_amount": overview.total_amount,
                    "top_sectors": overview.top_sectors,
                    "bottom_sectors": overview.bottom_sectors,
                }
            }
            
            # 保存到缓存
            with self._reviews_lock:
                self._reviews[today] = review_data
            self._save_reviews()
            
            logger.info(f"[MarketService] 今日复盘生成完成")
            return review_data
            
        except Exception as e:
            logger.error(f"[MarketService] 生成复盘失败: {e}")
            return {
                "date": today,
                "error": str(e),
                "generated_at": datetime.now().isoformat(),
            }
    
    def list_reviews(self, limit: int = 7) -> List[Dict[str, Any]]:
        """
        获取最近的复盘历史
        
        Args:
            limit: 返回数量限制
            
        Returns:
            复盘数据列表（按日期倒序）
        """
        with self._reviews_lock:
            reviews = list(self._reviews.values())
        
        # 按日期倒序
        reviews.sort(key=lambda x: x.get('date', ''), reverse=True)
        return reviews[:limit]
    
    def get_review_by_date(self, date: str) -> Optional[Dict[str, Any]]:
        """获取指定日期的复盘"""
        with self._reviews_lock:
            return self._reviews.get(date)


# ============================================================
# 便捷函数
# ============================================================

def get_config_service() -> ConfigService:
    """获取配置服务实例"""
    return ConfigService()


def get_analysis_service() -> AnalysisService:
    """获取分析服务单例"""
    return AnalysisService.get_instance()


def get_market_service() -> MarketService:
    """获取大盘服务单例"""
    return MarketService.get_instance()

