#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档拆分工具
按照User/Assistant对话格式将大文档拆分为多个子文档
"""

import re
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class DocumentSplitter:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.subtitle_dir = self.base_dir / "sub-title"
        self.subtitle_dir.mkdir(exist_ok=True)

        # 兼容不同的User标记格式
        self.user_patterns = [
            re.compile(r'##\s+[🧑‍💻]+\s*User', re.IGNORECASE),
            re.compile(r'##\s+User', re.IGNORECASE),
            re.compile(r'##\s+🧑‍💻\s*User', re.IGNORECASE),
        ]

        # Assistant标记
        self.assistant_pattern = re.compile(r'##\s+[🤖]+\s*Assistant', re.IGNORECASE)
        self.assistant_alt_pattern = re.compile(r'##\s+Assistant', re.IGNORECASE)

        # 标题标记
        self.title_pattern = re.compile(r'^#\s+(.+)$|^##\s+(.+)$')

    def find_user_positions(self, content: str) -> List[int]:
        """查找所有User标记的位置（行号）"""
        positions = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            for pattern in self.user_patterns:
                if pattern.search(line):
                    positions.append(i)
                    break

        return positions

    def extract_segment(self, lines: List[str], start_line: int, end_line: int) -> str:
        """提取从start_line到end_line的段内容"""
        # 包含start_line，不包含end_line
        segment_lines = lines[start_line:end_line]
        return '\n'.join(segment_lines)

    def find_assistant_title(self, segment: str) -> str:
        """在段中查找Assistant后的第一个标题"""
        lines = segment.split('\n')
        found_assistant = False

        for line in lines:
            # 检查是否是Assistant标记
            if self.assistant_pattern.search(line) or self.assistant_alt_pattern.search(line):
                found_assistant = True
                continue

            # 找到Assistant后，查找接下来的标题
            if found_assistant:
                title_match = self.title_pattern.match(line.strip())
                if title_match:
                    # 返回标题内容（去除#号和首尾空格）
                    title = title_match.group(1) or title_match.group(2)
                    return title.strip()

        return ""

    def sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除非法字符"""
        if not filename:
            return "Assistant-未命名"

        # 移除文件系统非法字符
        illegal_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(illegal_chars, '', filename)

        # 限制长度（最多200个字符）
        if len(sanitized) > 200:
            sanitized = sanitized[:200]

        return sanitized.strip()

    def split_document(self, filename: str, preview_only: bool = False, max_segments: int = None) -> Dict:
        """拆分单个文档"""
        file_path = self.base_dir / filename

        if not file_path.exists():
            return {
                "filename": filename,
                "status": "error",
                "error": "文件不存在"
            }

        # 检查文件大小（超过50MB警告）
        file_size = file_path.stat().st_size
        if file_size > 50 * 1024 * 1024:
            print(f"⚠️ 警告：文件 {filename} 大小为 {file_size / 1024 / 1024:.2f}MB，处理可能需要较长时间")

        # 读取文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "filename": filename,
                "status": "error",
                "error": f"读取文件失败: {str(e)}"
            }

        lines = content.split('\n')
        user_positions = self.find_user_positions(content)

        if not user_positions:
            return {
                "filename": filename,
                "status": "skipped",
                "reason": "未找到User标记"
            }

        print(f"📄 {filename}: 找到 {len(user_positions)} 个User标记")

        # 准备提取段
        segments_info = []
        segments_to_process = len(user_positions) - 1  # 最后一个不提取

        if max_segments:
            process_count = min(segments_to_process, max_segments)
        else:
            process_count = segments_to_process

        for i in range(process_count):
            start_line = user_positions[i]
            end_line = user_positions[i + 1]

            # 提取段内容
            segment_content = self.extract_segment(lines, start_line, end_line)
            segment_lines = end_line - start_line

            # 查找标题
            title = self.find_assistant_title(segment_content)
            if not title:
                title = f"Assistant-未命名-{i+1}"
                print(f"  ⚠️ 段 {i+1}: 未找到Assistant标题，使用默认名称")

            sanitized_title = self.sanitize_filename(title)
            output_filename = f"{sanitized_title}.md"
            output_path = self.subtitle_dir / output_filename

            segment_info = {
                "segment_id": i + 1,
                "start_line": start_line + 1,  # 1-based for human reading
                "end_line": end_line,
                "line_count": segment_lines,
                "title": title,
                "filename": output_filename,
                "status": "pending"
            }

            # 检查文件名冲突
            conflict_counter = 1
            original_path = output_path
            while output_path.exists() and not preview_only:
                # 文件名已存在，添加序号
                base_name = sanitized_title[:180]  # 预留空间给序号
                output_filename = f"{base_name}_{conflict_counter}.md"
                output_path = self.subtitle_dir / output_filename
                conflict_counter += 1

            segment_info["filename"] = output_filename
            segment_info["filepath"] = str(output_path)

            if not preview_only:
                # 写入文件
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(segment_content)

                    # 校验行数
                    with open(output_path, 'r', encoding='utf-8') as f:
                        written_content = f.read()
                    written_lines = len(written_content.split('\n'))

                    if written_lines == segment_lines:
                        segment_info["status"] = "success"
                    else:
                        segment_info["status"] = "warning"
                        segment_info["warning"] = f"行数不匹配: 预期{segment_lines}, 实际{written_lines}"
                except Exception as e:
                    segment_info["status"] = "error"
                    segment_info["error"] = str(e)
            else:
                segment_info["status"] = "preview"

            segments_info.append(segment_info)

            print(f"  📄 段 {i+1}: {title[:50]}... -> {output_filename} ({segment_lines}行)")

        # 统计信息
        status_counts = {}
        for seg in segments_info:
            status = seg["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

        result = {
            "filename": filename,
            "status": "processed",
            "total_users": len(user_positions),
            "segments_extracted": len(segments_info),
            "segments": segments_info,
            "statistics": status_counts
        }

        return result

    def process_all_documents(self, documents: List[str], preview_only: bool = False, max_segments: int = None) -> Dict:
        """处理多个文档"""
        report = {
            "timestamp": "",
            "base_directory": str(self.base_dir),
            "output_directory": str(self.subtitle_dir),
            "documents": [],
            "summary": {
                "total_documents": 0,
                "processed": 0,
                "skipped": 0,
                "errors": 0,
                "total_segments": 0
            }
        }

        for doc in documents:
            print(f"\n{'='*60}")
            print(f"正在处理: {doc}")
            print(f"{'='*60}")

            result = self.split_document(doc, preview_only=preview_only, max_segments=max_segments)
            report["documents"].append(result)

            # 更新统计
            report["summary"]["total_documents"] += 1
            if result["status"] == "processed":
                report["summary"]["processed"] += 1
                report["summary"]["total_segments"] += len(result.get("segments", []))
            elif result["status"] == "skipped":
                report["summary"]["skipped"] += 1
            elif result["status"] == "error":
                report["summary"]["errors"] += 1

        # 添加时间戳
        from datetime import datetime
        report["timestamp"] = datetime.now().isoformat()

        return report

    def save_report(self, report: Dict):
        """保存提取报告"""
        report_path = self.subtitle_dir / "_extraction_report.json"

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            print(f"\n{'='*60}")
            print(f"✅ 提取报告已保存: {report_path}")
            print(f"{'='*60}")
        except Exception as e:
            print(f"❌ 保存报告失败: {str(e)}")

def main():
    # 设置工作目录
    base_dir = "/Volumes/M4-SSD/项目 Project/项目 Project/A 工作项目/A 10 研发与产品项目/CIM-PIM-PSM/统一领域模型（CIM）/docs/concept/discuss"

    # 要处理的文档（四个文档全部处理）
    documents = [
        "建模检验准备.md",
        "医疗建模文档准备讨论.md",
        "医疗系统AI代理建模.md",
        "医院科室运营方案.md"
    ]

    # 创建拆分器
    splitter = DocumentSplitter(base_dir)

    print("="*60)
    print("CIM文档拆分工具")
    print("="*60)
    print(f"工作目录: {base_dir}")
    print(f"输出目录: {splitter.subtitle_dir}")
    print(f"待处理文档: {documents}")
    print("="*60)

    # 正式运行模式 - 提取所有段
    print("\n✍️ 正式运行模式：将提取并写入所有段")
    preview_only = False
    max_segments = None  # 处理所有段

    # 处理文档
    report = splitter.process_all_documents(
        documents,
        preview_only=preview_only,
        max_segments=max_segments
    )

    # 显示摘要
    print(f"\n{'='*60}")
    print("预览完成！")
    print(f"{'='*60}")
    print(f"总文档数: {report['summary']['total_documents']}")
    print(f"已处理: {report['summary']['processed']}")
    print(f"已跳过: {report['summary']['skipped']}")
    print(f"错误数: {report['summary']['errors']}")
    print(f"总提取段数: {report['summary']['total_segments']}")
    print(f"{'='*60}")
    print(f"\n⚠️ 预览完成，未写入文件。如需正式运行所有段，请修改脚本设置 preview_only = False")

if __name__ == "__main__":
    main()
