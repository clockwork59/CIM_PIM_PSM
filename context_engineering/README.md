# Context Engineering for CIM-PIM-PSM
# 医疗建筑知识图谱的上下文工程框架

> Context Engineering is the discipline of designing the **complete information payload**
> provided to an AI agent at inference time.
> -- davidkimai/Context-Engineering

## Core Premise

Context Engineering is NOT documentation management. The `Context Engineering/` directory
in this repo is a document library. This `context_engineering/` directory defines **how
those documents -- and the knowledge graph -- are delivered to 9 CIM Agents at runtime**.

The distinction matters:
- Documentation tells humans what to do.
- Context Engineering tells AI agents what to know, when to know it, and how much of it to load.

## Framework: C = A(c1, c2, ..., cn)

Where:
- **C** = output quality (CIM ontology correctness, ABox completeness, SPARQL accuracy)
- **A** = AI Agent (Claude, GPT, or specialized CIM agent)
- **ci** = context components (TBox subset, ABox instances, standards text, few-shot examples, memory)

The quality of Agent output is a function of context quality, not model capability.
Two identical models with different context produce radically different ontologies.

## Project Scale

| Asset | Count | Source |
|-------|-------|--------|
| owl:Class definitions | 545 | 17 namespaces across `_index_v4.ttl` import chain |
| TBox TTL files | 15 | `ontology/layer0-4` + `bridge/` + `ontology_skeleton.ttl` |
| ABox TTL files | 9 | `abox/nbu_*.ttl` (clinic, FAS, BAS t0-t2, CMMS, events, pset) |
| Named Graphs | 9 | graph/tbox, graph/ifc, graph/bas/*, graph/cmms, graph/fas, graph/event |
| Total triples | 61,941 | Measured via `rdflib` graph enumeration |
| SPARQL queries | 14 | 9 business + 5 validation (`cross_agent_validation.sparql`) |
| Validation pipeline | 12 steps | step1 (IFC parse) through step12 (MVP end-to-end) |
| CIM Agents | 9 | Agent-01 (Topology) through Agent-09 (Integration) |
| MVP | L2 fire response | 10 action nodes, 5-state event machine, 62 FAS detectors |

## Directory Structure

| Dir | Purpose | Analogy |
|-----|---------|---------|
| `00_foundations/` | Context theory + mathematical model | Atoms and Molecules |
| `10_system_design/` | CIM knowledge graph as context infrastructure | Cells and Organs |
| `20_agent_protocols/` | 9-Agent context contracts + handoff protocols | Neural Pathways |
| `30_memory_retrieval/` | Named Graph RAG + SPARQL as retrieval | Memory Systems |
| `40_evaluation/` | Context quality metrics + validation pipeline | Measurement |
| `50_templates/` | Reusable context templates for CIM tasks | Building Blocks |
| `60_field_integration/` | Multi-agent field theory + MVP integration | Emergent Systems |

## Quick Reference

| File | What It Answers |
|------|-----------------|
| [context_theory.md](00_foundations/context_theory.md) | What is context? How is it different from a prompt? |
| [knowledge_graph_as_context.md](10_system_design/knowledge_graph_as_context.md) | How do Named Graphs serve as context partitions? |
| [nine_agent_context_contracts.md](20_agent_protocols/nine_agent_context_contracts.md) | What context does each Agent consume and produce? |
| [rag_strategy.md](30_memory_retrieval/rag_strategy.md) | When to SPARQL-retrieve vs full-load TTL? |
| [context_quality_metrics.md](40_evaluation/context_quality_metrics.md) | How do we measure context quality (beyond SHACL)? |
| [agent_context_template.md](50_templates/agent_context_template.md) | How to define a new Agent's context contract? |
| [multi_agent_context_field.md](60_field_integration/multi_agent_context_field.md) | How does context flow across the 9-Agent system? |

## Relationship to Existing Assets

```
Context Engineering/          <-- Document library (for humans)
  00_foundations/              Theory docs, vision, architecture
  10_guides/                  Role-specific guides
  ...

context_engineering/          <-- Runtime context design (for AI agents)
  00_foundations/              How context works
  20_agent_protocols/         What each Agent receives at inference time
  30_memory_retrieval/        How the knowledge graph serves context
  ...

project_deliverables/         <-- The actual knowledge graph
  version02/cim/
    ontology/                 TBox (15 TTL files, 545 classes)
    abox/                     ABox (9 TTL files, instances)
    rules/                    SHACL + SPARQL validation
```

Context Engineering bridges the gap between the knowledge graph (data) and the agents
(consumers). Without it, agents either get too much context (noise) or too little (blind spots).
