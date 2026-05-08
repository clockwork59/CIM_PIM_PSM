#!/usr/bin/env python3
"""
CIM SHACL验证器
用于验证医疗建筑统一领域模型的完整性和约束一致性

作者: Claude Code + Agent-09
版本: 1.0
创建日期: 2025-12-07
"""

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

from rdflib import Graph, URIRef, Literal, Namespace
from pyshacl import validate

# 命名空间定义
MED = Namespace("http://medicine-nju.org/CIM/")
FND = Namespace("http://medicine-nju.org/CIM/Foundation/")
CON = Namespace("http://medicine-nju.org/CIM/Conceptual/")
REF = Namespace("http://medicine-nju.org/CIM/Reference/")
QUDT = Namespace("http://qudt.org/schema/qudt/")
SH = Namespace("http://www.w3.org/ns/shacl#")


@dataclass
class ValidationResult:
    """验证结果数据结构"""
    conforms: bool
    violation_count: int
    violations: List[Dict[str, Any]] = field(default_factory=list)
    warning_count: int = 0
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    validation_time: float = 0.0
    total_nodes: int = 0
    total_triples: int = 0
    constraint_coverage: float = 0.0


@dataclass
class ConstraintStats:
    """约束统计信息"""
    total_constraints: int = 0
    hard_constraints: int = 0
    soft_constraints: int = 0
    medical_specific_constraints: int = 0
    coverage_by_domain: Dict[str, int] = field(default_factory=dict)


class CIMValidator:
    """CIM SHACL验证器主类"""

    def __init__(self, shapes_dir: Optional[Path] = None):
        """
        初始化验证器

        Args:
            shapes_dir: SHACL形状定义目录，默认为 ./shacl_shapes/
        """
        self.shapes_dir = shapes_dir or Path("./shacl_shapes")
        self.shapes_graph = self._load_shapes()
        self.constraint_stats = self._calculate_constraint_stats()

    def _load_shapes(self) -> Graph:
        """加载所有SHACL形状定义"""
        graph = Graph()

        if not self.shapes_dir.exists():
            print(f"警告: 形状目录 {self.shapes_dir} 不存在，将使用默认约束")
            return graph

        shape_files = list(self.shapes_dir.glob("*.ttl"))
        if not shape_files:
            print(f"警告: {self.shapes_dir} 中没有找到TTL文件")
            return graph

        for shape_file in shape_files:
            try:
                graph.parse(shape_file, format="turtle")
                print(f"已加载形状文件: {shape_file.name}")
            except Exception as e:
                print(f"加载 {shape_file.name} 失败: {e}")

        return graph

    def _calculate_constraint_stats(self) -> ConstraintStats:
        """计算约束统计信息"""
        stats = ConstraintStats()

        # 查询所有形状和约束
        shape_query = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        SELECT ?shape ?severity ?targetClass ?targetObjectsOf ?message
        WHERE {
            ?shape a sh:NodeShape .
            OPTIONAL { ?shape sh:severity ?severity }
            OPTIONAL { ?shape sh:targetClass ?targetClass }
            OPTIONAL { ?shape sh:targetObjectsOf ?targetObjectsOf }
            OPTIONAL { ?shape sh:message ?message }
        }
        """

        try:
            results = self.shapes_graph.query(shape_query)
            shapes_by_domain = {}

            for row in results:
                stats.total_constraints += 1

                # 统计硬/软约束
                severity = str(row.severity) if row.severity else "sh:Violation"
                if "Violation" in severity:
                    stats.hard_constraints += 1
                elif "Warning" in severity:
                    stats.soft_constraints += 1

                # 按域统计
                target = row.targetClass or row.targetObjectsOf
                if target:
                    target_str = str(target)
                    if "medical" in target_str.lower() or "hospital" in target_str.lower():
                        stats.medical_specific_constraints += 1

                    # 按域分类
                    domain = self._classify_domain(target_str)
                    shapes_by_domain[domain] = shapes_by_domain.get(domain, 0) + 1

            stats.coverage_by_domain = shapes_by_domain

        except Exception as e:
            print(f"计算约束统计失败: {e}")

        return stats

    def _classify_domain(self, class_uri: str) -> str:
        """将类URI分类到对应域"""
        uri_lower = class_uri.lower()

        if any(x in uri_lower for x in ["thermal", "chiller", "ahu", "hvac"]):
            return "HVAC系统"
        elif any(x in uri_lower for x in ["electrical", "transformer", "generator"]):
            return "电气系统"
        elif any(x in uri_lower for x in ["plumbing", "water", "pump"]):
            return "给排水系统"
        elif any(x in uri_lower for x in ["medic", "surgery", "patient"]):
            return "医疗流程"
        elif any(x in uri_lower for x in ["space", "room", "zone"]):
            return "空间管理"
        elif any(x in uri_lower for x in ["meter", "energy"]):
            return "计量体系"
        elif any(x in uri_lower for x in ["sensor", "control", "actuator"]):
            return "控制系统"
        else:
            return "其他"

    def validate_model(self,
                      model_file: Path,
                      inference: str = "none",
                      debug: bool = False) -> ValidationResult:
        """
        验证CIM模型

        Args:
            model_file: 要验证的CIM模型文件（Turtle格式）
            inference: 推理类型（"none", "rdfs", "owlrl", "both"）
            debug: 是否启用调试模式

        Returns:
            验证结果对象
        """
        start_time = time.time()
        result = ValidationResult()

        # 加载数据图
        data_graph = Graph()
        try:
            data_graph.parse(model_file, format="turtle")
        except Exception as e:
            print(f"加载模型文件失败: {e}")
            result.violations.append({
                "focus_node": str(model_file),
                "path": "文件解析",
                "message": f"文件解析失败: {e}"
            })
            result.violation_count = 1
            return result

        # 记录模型统计信息
        result.total_nodes = len(set(data_graph.subjects()))
        result.total_triples = len(data_graph)

        # 执行验证
        try:
            conforms, results_graph, results_text = validate(
                data_graph,
                shacl_graph=self.shapes_graph,
                inference=inference,
                debug=debug
            )

            result.conforms = conforms

            # 解析验证结果
            if not conforms:
                violations_query = """
                SELECT ?focus ?path ?message ?severity ?constraint
                WHERE {
                    ?vr a sh:ValidationResult .
                    ?vr sh:focusNode ?focus .
                    OPTIONAL { ?vr sh:resultPath ?path }
                    OPTIONAL { ?vr sh:resultMessage ?message }
                    OPTIONAL { ?vr sh:resultSeverity ?severity }
                    OPTIONAL { ?vr sh:sourceConstraint ?constraint }
                }
                """

                for row in results_graph.query(violations_query):
                    violation = {
                        "focus_node": str(row.focus),
                        "path": str(row.path) if row.path else "N/A",
                        "message": str(row.message) if row.message else "N/A",
                        "severity": str(row.severity) if row.severity else "Violation"
                    }

                    if "Warning" in violation["severity"]:
                        result.warnings.append(violation)
                        result.warning_count += 1
                    else:
                        result.violations.append(violation)
                        result.violation_count += 1

        except Exception as e:
            print(f"验证过程失败: {e}")
            result.violations.append({
                "focus_node": str(model_file),
                "path": "验证执行",
                "message": f"验证执行失败: {e}"
            })
            result.violation_count = 1

        # 计算验证时间
        result.validation_time = time.time() - start_time

        # 计算约束覆盖率
        if self.constraint_stats.total_constraints > 0:
            num_constraints_checked = len(set(
                result.violations + result.warnings
            ))
            result.constraint_coverage = min(
                1.0, num_constraints_checked / self.constraint_stats.total_constraints
            )

        return result

    def validate_multiple_models(self,
                               model_files: List[Path],
                               output_dir: Optional[Path] = None) -> Dict[str, ValidationResult]:
        """
        批量验证多个模型

        Args:
            model_files: 模型文件列表
            output_dir: 可选的输出目录，用于保存验证报告

        Returns:
            模型文件与验证结果的映射字典
        """
        results = {}

        for model_file in model_files:
            if not model_file.exists():
                print(f"警告: 模型文件不存在 {model_file}")
                continue

            print(f"正在验证: {model_file.name}")
            result = self.validate_model(model_file)
            results[str(model_file)] = result

            # 保存单独的验证报告
            if output_dir and output_dir.exists():
                self._save_validation_report(model_file, result, output_dir)

        # 保存汇总报告
        if output_dir and output_dir.exists():
            self._save_summary_report(results, output_dir)

        return results

    def _save_validation_report(self,
                               model_file: Path,
                               result: ValidationResult,
                               output_dir: Path):
        """保存单个模型的验证报告"""
        report_file = output_dir / f"{model_file.stem}_validation_report.json"

        report_data = {
            "model": str(model_file),
            "validation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "conforms": result.conforms,
            "summary": {
                "violation_count": result.violation_count,
                "warning_count": result.warning_count,
                "validation_time_seconds": result.validation_time,
                "total_nodes": result.total_nodes,
                "total_triples": result.total_triples,
                "constraint_coverage": result.constraint_coverage
            },
            "violations": result.violations,
            "warnings": result.warnings
        }

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"验证报告已保存: {report_file}")

    def _save_summary_report(self, results: Dict[str, ValidationResult], output_dir: Path):
        """保存汇总报告"""
        summary_file = output_dir / "validation_summary.json"

        summary_data = {
            "validation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_models": len(results),
            "models_validated": sum(1 for r in results.values() if r.conforms),
            "total_violations": sum(r.violation_count for r in results.values()),
            "total_warnings": sum(r.warning_count for r in results.values()),
            "average_validation_time": sum(r.validation_time for r in results.values()) / len(results) if results else 0,
            "constraint_stats": {
                "total_constraints": self.constraint_stats.total_constraints,
                "hard_constraints": self.constraint_stats.hard_constraints,
                "soft_constraints": self.constraint_stats.soft_constraints,
                "medical_specific_constraints": self.constraint_stats.medical_specific_constraints,
                "coverage_by_domain": self.constraint_stats.coverage_by_domain
            }
        }

        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

        print(f"汇总报告已保存: {summary_file}")

    def print_statistics(self):
        """打印验证器统计信息"""
        print("\n=== CIM SHACL验证器统计 ===")
        print(f"总约束数: {self.constraint_stats.total_constraints}")
        print(f"硬约束: {self.constraint_stats.hard_constraints}")
        print(f"软约束: {self.constraint_stats.soft_constraints}")
        print(f"医疗专用约束: {self.constraint_stats.medical_specific_constraints}")

        print("\n按域分布:")
        for domain, count in self.constraint_stats.coverage_by_domain.items():
            print(f"  {domain}: {count} 个约束")

        print("=" * 40)


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="验证CIM模型")
    parser.add_argument("model", help="CIM模型文件（Turtle格式）")
    parser.add_argument("--shapes-dir", default="./shacl_shapes",
                       help="SHACL形状定义目录")
    parser.add_argument("--output-dir", help="输出报告目录")
    parser.add_argument("--inference", default="none",
                       choices=["none", "rdfs", "owlrl", "both"])
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    # 初始化验证器
    validator = CIMValidator(shapes_dir=Path(args.shapes_dir))
    validator.print_statistics()

    # 执行验证
    model_file = Path(args.model)
    result = validator.validate_model(model_file, inference=args.inference, debug=args.debug)

    # 打印结果
    print(f"\n验证结果: {'✓ 通过' if result.conforms else '✗ 失败'}")
    print(f"违规数量: {result.violation_count}")
    print(f"警告数量: {result.warning_count}")
    print(f"验证时间: {result.validation_time:.2f} 秒")
    print(f"总节点数: {result.total_nodes}")
    print(f"总三元组: {result.total_triples}")
    print(f"约束覆盖率: {result.constraint_coverage:.1%}")

    # 输出详细违规信息
    if result.violation_count > 0:
        print("\n详细违规信息:")
        for i, violation in enumerate(result.violations, 1):
            print(f"\n[{i}] 焦点节点: {violation['focus_node']}")
            print(f"    路径: {violation['path']}")
            print(f"    消息: {violation['message']}")

    # 保存报告
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)
        validator._save_validation_report(model_file, result, output_dir)


if __name__ == "__main__":
    main()
