#!/usr/bin/env python3
"""
Module 14 — Knowledge-Atom MCP (PEM Q1-Q4 범용)

EAE University의 콘텐츠 단위를 "아티클"에서 "검증가능한 지식원자"로 전환.
parksy-rawmat(원자재) → dollar-system-mcp(가공/검증) → eae-univ(게시) 공급망의 중간 계층.

knowledge-atom 표준 스키마:
  atom_id, domain, title, thesis, chain, verdict, confidence,
  source_path, registered_at, metadata

의존성:
  - eae-univ research/body, research/butterfly, philosophy/ 디렉토리
  - parksy-rawmat write_article() 출력물 (article JSON)
"""

import os, json, re, glob
from datetime import datetime
from typing import Optional

# ── 상수 ────────────────────────────────────────────────────────────

EAE_UNIV_BASE = os.path.expanduser("~/eae-univ")
REGISTRY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "knowledge_registry.json",
)

SOURCE_TIER_PENALTY = {
    "S급": 1.0,
    "A급": 0.9,
    "B급": 0.7,
    "C급": 0.5,
}

COMMON_DISCLAIMER = {
    "analysis_type": "사후분석(post-hoc)",
    "predictive": False,
    "watermark": "이 지식원자는 등록 시점의 검증된 데이터 기준. 시간 경과에 따라 신뢰도 변동 가능.",
}

DOMAIN_LABELS = {
    "body": "건강/신체",
    "butterfly": "경제/자유",
    "philosophy": "철학/세계관",
    "whitepaper": "백서",
    "course": "강의",
}

# ── 헬퍼 ────────────────────────────────────────────────────────────

def _ensure_registry_dir():
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)


def _load_registry() -> dict:
    """지식원자 레지스트리 로드."""
    _ensure_registry_dir()
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"atoms": [], "registered_at": None, "version": "1.0.0"}


def _save_registry(registry: dict):
    """레지스트리 저장."""
    _ensure_registry_dir()
    registry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M KST")
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def _article_to_atom(article: dict, filepath: str) -> dict:
    """article JSON → knowledge-atom 변환."""
    chain_raw = article.get("chain", "")
    chain_nodes = [c.strip() for c in chain_raw.split("→") if c.strip()]

    return {
        "atom_id": f"KA-{article.get('domain', 'unknown').upper()}-{article.get('episode_id', '')}",
        "domain": article.get("domain", "unknown"),
        "title": article.get("title", ""),
        "thesis": article.get("thesis", ""),
        "chain": chain_nodes,
        "chain_raw": chain_raw,
        "verdict": article.get("verdict", "UNKNOWN"),
        "conviction": article.get("conviction", "MEDIUM"),
        "confidence": article.get("confidence", 0),
        "verdict_reason": article.get("verdict_reason", ""),
        "bull_summary": article.get("bull_summary", ""),
        "bear_summary": article.get("bear_summary", ""),
        "conditions": article.get("conditions", ""),
        "review_trigger": article.get("review_trigger", ""),
        "sources": article.get("sources", []),
        "source_path": filepath,
        "source_tier": "A급",
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        "metadata": {
            "created_at": article.get("created_at", ""),
            "pem_quadrant": _classify_pem(article.get("domain", "")),
            "category": DOMAIN_LABELS.get(article.get("domain", ""), article.get("domain", "")),
        },
    }


def _md_to_atom(filepath: str) -> Optional[dict]:
    """철학 마크다운 문서 → knowledge-atom 변환."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 첫 H1을 제목으로
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(filepath)

    # H1 다음 블록인용구를 thesis로
    thesis_match = re.search(r"^>\s+(.+)$", content, re.MULTILINE)
    thesis = thesis_match.group(1).strip() if thesis_match else title

    filename = os.path.basename(filepath)
    atom_id = f"KA-PHIL-{filename.replace('.md', '').upper()}"

    return {
        "atom_id": atom_id,
        "domain": "philosophy",
        "title": title,
        "thesis": thesis,
        "chain": [],
        "chain_raw": "",
        "verdict": "PROCEED",
        "conviction": "HIGH",
        "confidence": 85,
        "verdict_reason": "철학 문서 — EAE 세계관의 공리. 검증 대상이 아닌 전제.",
        "bull_summary": "",
        "bear_summary": "",
        "conditions": "",
        "review_trigger": "",
        "sources": [],
        "source_path": filepath,
        "source_tier": "S급",
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        "metadata": {
            "created_at": "",
            "pem_quadrant": "철학/초학문",
            "category": "철학/세계관",
            "doc_type": "philosophy_markdown",
        },
    }


def _classify_pem(domain: str) -> str:
    """도메인 → PEM 사분면 매핑."""
    mapping = {
        "body": "Q3 (물성×미시) — 건강/신체",
        "butterfly": "Q1 (물성×거시) — 경제/금융",
        "philosophy": "초학문 — 철학/세계관",
        "whitepaper": "Q1-Q4 범용 — 백서",
        "course": "Q2 (온라인×거시) — 교육",
    }
    return mapping.get(domain, "미분류")


# ── 메인 함수 ────────────────────────────────────────────────────────

def scan_and_register(
    include_body: bool = True,
    include_butterfly: bool = True,
    include_philosophy: bool = True,
    force_rescan: bool = False,
) -> dict:
    """
    eae-univ 레포지토리를 스캔해 knowledge-atom 레지스트리 구축/갱신.

    Args:
        include_body: research/body/ 포함
        include_butterfly: research/butterfly/ 포함
        include_philosophy: philosophy/ 포함
        force_rescan: True면 기존 레지스트리 무시하고 전수 재스캔

    Returns:
        등록 결과 (총 atom 수, 도메인별 분포, 신규 등록 수)
    """
    if not os.path.exists(EAE_UNIV_BASE):
        return {
            "error": f"eae-univ 디렉토리를 찾을 수 없음: {EAE_UNIV_BASE}",
            "note": "eae-univ 레포가 ~/eae-univ에 클론되어 있어야 함",
        }

    registry = _load_registry()
    existing_ids = set() if force_rescan else {a["atom_id"] for a in registry.get("atoms", [])}

    new_atoms = []
    scan_log = {"body": 0, "butterfly": 0, "philosophy": 0}

    # ── research/body ──
    if include_body:
        body_dir = os.path.join(EAE_UNIV_BASE, "research", "body")
        for fpath in sorted(glob.glob(os.path.join(body_dir, "EP-BODY-*.json"))):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                atom = _article_to_atom(article, fpath)
                if atom["atom_id"] not in existing_ids:
                    new_atoms.append(atom)
                    scan_log["body"] += 1
            except (json.JSONDecodeError, KeyError) as e:
                pass  # 말포맷 JSON 스킵

    # ── research/butterfly ──
    if include_butterfly:
        bf_dir = os.path.join(EAE_UNIV_BASE, "research", "butterfly")
        for fpath in sorted(glob.glob(os.path.join(bf_dir, "EP-BUTTERFLY-*.json"))):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                atom = _article_to_atom(article, fpath)
                if atom["atom_id"] not in existing_ids:
                    new_atoms.append(atom)
                    scan_log["butterfly"] += 1
            except (json.JSONDecodeError, KeyError):
                pass

    # ── philosophy ──
    if include_philosophy:
        phil_dir = os.path.join(EAE_UNIV_BASE, "philosophy")
        for fpath in sorted(glob.glob(os.path.join(phil_dir, "*.md"))):
            atom = _md_to_atom(fpath)
            if atom and atom["atom_id"] not in existing_ids:
                new_atoms.append(atom)
                scan_log["philosophy"] += 1

    # ── 병합 ──
    if force_rescan:
        registry["atoms"] = new_atoms
    else:
        registry["atoms"].extend(new_atoms)

    registry["total_atoms"] = len(registry["atoms"])
    registry["registered_at"] = (
        registry.get("registered_at") or datetime.now().strftime("%Y-%m-%d %H:%M KST")
    )

    _save_registry(registry)

    # 도메인별 분포
    domain_dist = {}
    for a in registry["atoms"]:
        d = a.get("domain", "unknown")
        domain_dist[d] = domain_dist.get(d, 0) + 1

    return {
        "total_atoms": len(registry["atoms"]),
        "newly_registered": len(new_atoms),
        "domain_distribution": domain_dist,
        "scan_details": scan_log,
        "registry_path": REGISTRY_PATH,
        "source": EAE_UNIV_BASE,
        "note": (
            f"스캔 완료. 기존 {len(registry['atoms']) - len(new_atoms)}개 + "
            f"신규 {len(new_atoms)}개 = 총 {len(registry['atoms'])}개 atom"
        ),
    }


def query_knowledge(
    keyword: str = "",
    domain: str = "",
    verdict: str = "",
    min_confidence: int = 0,
    max_results: int = 20,
) -> dict:
    """
    knowledge-atom 검색.

    Args:
        keyword: 제목/테제/체인에서 검색 (공백=전체)
        domain: 도메인 필터 (body/butterfly/philosophy/whitepaper/course)
        verdict: 평결 필터 (PROCEED/REDUCE/HOLD)
        min_confidence: 최소 신뢰도 (0-100)
        max_results: 최대 결과 수

    Returns:
        검색 결과 리스트 + 메타
    """
    registry = _load_registry()
    atoms = registry.get("atoms", [])

    if not atoms:
        return {
            "error": "등록된 knowledge-atom이 없습니다. register_knowledge()를 먼저 실행하세요.",
            "hint": "scan_and_register() 호출 필요",
        }

    # ── 필터링 ──
    filtered = []
    for atom in atoms:
        # 도메인
        if domain and atom.get("domain") != domain:
            continue
        # 평결
        if verdict and atom.get("verdict") != verdict:
            continue
        # 신뢰도
        if atom.get("confidence", 0) < min_confidence:
            continue
        # 키워드
        if keyword:
            kw = keyword.lower()
            search_text = (
                atom.get("title", "").lower() + " " +
                atom.get("thesis", "").lower() + " " +
                atom.get("chain_raw", "").lower() + " " +
                atom.get("verdict_reason", "").lower()
            )
            if kw not in search_text:
                continue
        filtered.append(atom)

    # 정렬: 신뢰도 내림차순
    filtered.sort(key=lambda a: a.get("confidence", 0), reverse=True)

    # 결과 제한
    results = filtered[:max_results]

    # 요약 결과 (상세 버전과 요약 버전)
    summary_results = []
    for a in results:
        summary_results.append({
            "atom_id": a["atom_id"],
            "domain": a["domain"],
            "category": a.get("metadata", {}).get("category", ""),
            "title": a["title"],
            "thesis": a["thesis"],
            "chain": a.get("chain_raw", ""),
            "verdict": a["verdict"],
            "confidence": a["confidence"],
            "pem_quadrant": a.get("metadata", {}).get("pem_quadrant", ""),
            "source_tier": a.get("source_tier", "C급"),
        })

    return {
        "query": {
            "keyword": keyword or "(전체)",
            "domain": domain or "(전체)",
            "verdict": verdict or "(전체)",
            "min_confidence": min_confidence,
        },
        "total_matches": len(filtered),
        "returned": len(results),
        "results": summary_results,
        "note": f"{len(filtered)}개 중 {len(results)}개 반환 (신뢰도순)",
    }


def generate_primer(
    domain: str = "",
    thesis_keyword: str = "",
    max_atoms: int = 10,
    include_analysis: bool = True,
) -> dict:
    """
    knowledge-atom을 종합해 개론서(primer) 생성.

    Args:
        domain: 도메인 필터 (body/butterfly/philosophy 등)
        thesis_keyword: 테제 키워드 (관련 atom 필터링)
        max_atoms: 포함할 최대 atom 수
        include_analysis: 종합 분석 포함 여부

    Returns:
        primer: 제목, 개요, 섹션, 종합분석
    """
    registry = _load_registry()
    atoms = registry.get("atoms", [])

    if not atoms:
        return {
            "error": "등록된 knowledge-atom이 없습니다.",
            "hint": "scan_and_register()를 먼저 실행하세요.",
        }

    # ── 필터링 ──
    filtered = []
    for atom in atoms:
        if domain and atom.get("domain") != domain:
            continue
        if thesis_keyword:
            kw = thesis_keyword.lower()
            search_text = (
                atom.get("title", "").lower() + " " +
                atom.get("thesis", "").lower() + " " +
                atom.get("chain_raw", "").lower()
            )
            if kw not in search_text:
                continue
        filtered.append(atom)

    if not filtered:
        return {
            "error": "조건에 맞는 atom이 없습니다.",
            "query": {"domain": domain, "thesis_keyword": thesis_keyword},
            "hint": "검색 조건을 완화하거나 register_knowledge()로 먼저 등록하세요.",
        }

    # 신뢰도순 정렬
    filtered.sort(key=lambda a: a.get("confidence", 0), reverse=True)
    selected = filtered[:max_atoms]

    # ── 개론서 섹션 ──
    sections = []
    for i, atom in enumerate(selected, 1):
        section = {
            "section_id": i,
            "title": atom.get("title", ""),
            "thesis": atom.get("thesis", ""),
            "chain": atom.get("chain_raw", ""),
            "verdict": atom.get("verdict", ""),
            "confidence": atom.get("confidence", 0),
            "category": atom.get("metadata", {}).get("category", ""),
            "pem_quadrant": atom.get("metadata", {}).get("pem_quadrant", ""),
            "conditions": atom.get("conditions", ""),
        }
        if include_analysis and atom.get("verdict_reason"):
            section["analysis"] = atom["verdict_reason"]
        if include_analysis and atom.get("bull_summary"):
            section["bull_case"] = atom["bull_summary"]
        if include_analysis and atom.get("bear_summary"):
            section["bear_case"] = atom["bear_summary"]
        sections.append(section)

    # ── 종합 분석 ──
    summary = {}
    if include_analysis and len(selected) >= 2:
        verdicts = [a.get("verdict", "UNKNOWN") for a in selected]
        confidences = [a.get("confidence", 0) for a in selected]
        avg_conf = sum(confidences) / len(confidences)

        proceed_count = verdicts.count("PROCEED")
        reduce_count = verdicts.count("REDUCE")
        hold_count = verdicts.count("HOLD")

        chains = [a.get("chain_raw", "") for a in selected if a.get("chain_raw")]
        common_chain_nodes = []
        if chains:
            all_nodes = []
            for c in chains:
                all_nodes.extend([n.strip() for n in c.split("→") if n.strip()])
            node_freq = {}
            for n in all_nodes:
                node_freq[n] = node_freq.get(n, 0) + 1
            common_chain_nodes = [
                {"node": k, "frequency": v, "appears_in_pct": round(v / len(selected) * 100, 1)}
                for k, v in sorted(node_freq.items(), key=lambda x: -x[1])
                if v >= 2  # 2개 이상에서 등장
            ]

        summary = {
            "total_atoms_in_primer": len(selected),
            "avg_confidence": round(avg_conf, 1),
            "verdict_distribution": {
                "PROCEED": proceed_count,
                "REDUCE": reduce_count,
                "HOLD": hold_count,
            },
            "common_chain_nodes": common_chain_nodes[:10],
        }

    # ── 제목 ──
    if domain:
        domain_label = DOMAIN_LABELS.get(domain, domain)
        title = f"{domain_label} 개론서"
    elif thesis_keyword:
        title = f"'{thesis_keyword}' 개론서"
    else:
        title = "EAE University 종합 개론서"

    primer = {
        "title": title,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
        "domain": domain or "(전체)",
        "thesis_keyword": thesis_keyword or "(전체)",
        "total_atoms_available": len(filtered),
        "sections": sections,
        "summary": summary,
        "primer_type": "knowledge-atom 종합 — 사후분석 기반",
        "disclaimer": COMMON_DISCLAIMER,
        "note": (
            f"{len(filtered)}개 관련 atom 중 상위 {len(selected)}개로 구성. "
            "각 atom은 개별 검증된 지식 단위이며, 종합은 편집자의 재구성."
        ),
    }

    return primer


def knowledge_stats() -> dict:
    """
    knowledge-atom 레지스트리 통계.

    Returns:
        총 atom 수, 도메인별 분포, 평결 분포, 신뢰도 통계, PEM 분포
    """
    registry = _load_registry()
    atoms = registry.get("atoms", [])

    if not atoms:
        return {
            "total_atoms": 0,
            "note": "등록된 knowledge-atom이 없습니다.",
            "hint": "scan_and_register()를 먼저 실행하세요.",
            "registered_at": registry.get("registered_at"),
        }

    # 도메인별
    domain_dist = {}
    for a in atoms:
        d = a.get("domain", "unknown")
        domain_dist[d] = domain_dist.get(d, 0) + 1

    # 평결별
    verdict_dist = {}
    for a in atoms:
        v = a.get("verdict", "UNKNOWN")
        verdict_dist[v] = verdict_dist.get(v, 0) + 1

    # 신뢰도
    confidences = [a.get("confidence", 0) for a in atoms]
    avg_conf = sum(confidences) / len(confidences) if confidences else 0

    # PEM 분포
    pem_dist = {}
    for a in atoms:
        pq = a.get("metadata", {}).get("pem_quadrant", "미분류")
        pem_dist[pq] = pem_dist.get(pq, 0) + 1

    # source_tier 분포
    tier_dist = {}
    for a in atoms:
        t = a.get("source_tier", "C급")
        tier_dist[t] = tier_dist.get(t, 0) + 1

    return {
        "total_atoms": len(atoms),
        "registered_at": registry.get("registered_at"),
        "last_updated": registry.get("updated_at"),
        "registry_path": REGISTRY_PATH,
        "domain_distribution": domain_dist,
        "verdict_distribution": verdict_dist,
        "confidence_stats": {
            "average": round(avg_conf, 1),
            "min": min(confidences),
            "max": max(confidences),
        },
        "pem_quadrant_distribution": pem_dist,
        "source_tier_distribution": tier_dist,
        "atoms": [
            {
                "atom_id": a["atom_id"],
                "domain": a["domain"],
                "title": a["title"],
                "verdict": a["verdict"],
                "confidence": a["confidence"],
                "pem_quadrant": a.get("metadata", {}).get("pem_quadrant", ""),
            }
            for a in atoms
        ],
        "disclaimer": COMMON_DISCLAIMER,
    }


def run_module14(
    action: str = "scan",
    **kwargs,
) -> dict:
    """
    Module 14 통합 실행 인터페이스.

    Args:
        action: scan | query | primer | stats
        **kwargs: 각 action별 파라미터

    Returns:
        action별 결과
    """
    actions = {
        "scan": lambda: scan_and_register(
            include_body=kwargs.get("include_body", True),
            include_butterfly=kwargs.get("include_butterfly", True),
            include_philosophy=kwargs.get("include_philosophy", True),
            force_rescan=kwargs.get("force_rescan", False),
        ),
        "query": lambda: query_knowledge(
            keyword=kwargs.get("keyword", ""),
            domain=kwargs.get("domain", ""),
            verdict=kwargs.get("verdict", ""),
            min_confidence=kwargs.get("min_confidence", 0),
            max_results=kwargs.get("max_results", 20),
        ),
        "primer": lambda: generate_primer(
            domain=kwargs.get("domain", ""),
            thesis_keyword=kwargs.get("thesis_keyword", ""),
            max_atoms=kwargs.get("max_atoms", 10),
            include_analysis=kwargs.get("include_analysis", True),
        ),
        "stats": knowledge_stats,
    }

    if action not in actions:
        return {
            "error": f"알 수 없는 action: {action}",
            "available_actions": list(actions.keys()),
        }

    result = actions[action]()

    return {
        "module": "Module 14 — Knowledge-Atom MCP",
        "version": "1.0.0",
        "action": action,
        "result": result,
        "disclaimer": COMMON_DISCLAIMER,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M KST"),
    }


if __name__ == "__main__":
    import sys

    if "--scan" in sys.argv:
        force = "--force" in sys.argv
        result = run_module14("scan", force_rescan=force)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--stats" in sys.argv:
        result = run_module14("stats")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--demo" in sys.argv:
        # 데모: 스캔 후 개론서 생성
        scan_result = scan_and_register()
        primer = generate_primer(domain="philosophy")
        print(json.dumps({
            "module": "Module 14 — Knowledge-Atom MCP",
            "scan": {
                "total": scan_result["total_atoms"],
                "new": scan_result["newly_registered"],
                "domains": scan_result["domain_distribution"],
            },
            "primer_sample": {
                "title": primer["title"],
                "sections_count": len(primer["sections"]),
                "summary": primer.get("summary"),
            },
            "available_actions": [
                "scan — eae-univ 스캔 및 등록",
                "query — knowledge-atom 검색 (keyword/domain/verdict/confidence)",
                "primer — 개론서 생성 (domain/thesis_keyword)",
                "stats — 레지스트리 통계",
            ],
        }, ensure_ascii=False, indent=2))
    else:
        import json
        print(json.dumps({
            "module": "Module 14 — Knowledge-Atom MCP",
            "version": "1.0.0",
            "commands": {
                "--scan": "eae-univ 스캔 후 knowledge-atom 등록",
                "--force": "--scan과 함께 사용 시 전수 재스캔",
                "--stats": "레지스트리 통계",
                "--demo": "데모 실행 (스캔 + 철학 개론서)",
            },
        }, ensure_ascii=False, indent=2))
