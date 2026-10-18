# A focused literature review and novelty check

Primary records checked October 18, 2026. This is a bounded starting review; full methods, artifacts and subsequent work still need inspection. None of the comparisons establishes an unoccupied research niche.

## HealthBench — Arora et al., 2025

[Primary paper](https://arxiv.org/abs/2505.08775)

HealthBench evaluates open-ended health conversations with physician-written, conversation-specific rubrics, including transforming clinical data. It is a strong example of expert-grounded task evaluation and broad behavioral criteria. The overlap means “healthcare data transformation benchmark” is not a sufficient novelty claim. Our narrower candidate isolates explicit amendments, evidence conflicts, missing metadata and action grants using auditable synthetic records. Whether that adds useful information beyond existing rubric criteria is an empirical question.

## MedAgentBench — Jiang et al., 2025

[Primary paper](https://arxiv.org/abs/2501.14654)

MedAgentBench provides physician-written tasks in an interactive, FHIR-compliant virtual EHR environment. It is much closer to actual tool-agent workflow evaluation than our closed-record CPU demo. Our prototype does not reproduce its environment, data or success criteria. A later extension could test versioned evidence under a compatible sandbox, but task realism, integration effort and data permissions need review first. We cannot infer robust medical-agent behavior from successful metadata reconciliation.

## MedHELM — Bedi et al., 2025

[Primary paper](https://arxiv.org/abs/2505.23802)

MedHELM supplies a clinician-validated taxonomy and a broad suite spanning clinical, research and administrative tasks, with evaluation-method and cost comparisons. This argues against presenting one tiny synthetic task as a holistic assessment. The candidate here is one diagnostic slice: can an agent retain evidence status and provenance during updates? A useful study should explain where that slice belongs in the broader taxonomy and which failure modes the slice cannot measure.

## MPIB — Lee, Jang and Choi, 2026

[Primary paper, revised August 2026; Findings of EMNLP 2026](https://arxiv.org/abs/2602.06268)

MPIB evaluates direct and retrieved-context medical prompt injections using clinically grounded harm and attack-success measures. It establishes that medical prompt injection and outcome-level risk are already active benchmark topics. This prototype deliberately avoids clinical recommendations and does not measure harm. Its authorization/correction examples are metadata tests, not a replacement for MPIB or evidence that an LLM is clinically safe.

## What could be worth adding

Candidate question: **Do explicit record corrections and unresolved-evidence states change an agent's metadata errors and unauthorized action proposals, independently of ordinary task accuracy?** The useful contribution would be the controlled comparisons, a reviewed annotation contract and validated failure measurements—not the mere existence of a source allowlist.

Evidence needed before a novelty claim:

1. Inspect amendment, conflicting-source, abstention and permission criteria in the complete benchmarks and their released tasks.
2. Search medical-record amendment, clinical summarization factuality, temporal EHR reasoning and general agent-provenance literature beyond these four papers.
3. Obtain domain review of which synthetic metadata tasks are both realistic and valuable.
4. Demonstrate a real-model failure that a matched intervention improves without hiding uncertainty or sacrificing correct extraction.
5. Report cases where recency-only, strict source filtering or the proposed rules make the result worse.

The [comparison matrix](related_work_matrix.json) separates established overlap from proposed measurements. No upstream datasets or implementations have been vendored, and no model results from different benchmarks are compared as if they were matched runs.
