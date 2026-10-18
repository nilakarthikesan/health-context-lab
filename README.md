# Health Context Lab

A small, entirely synthetic research-record benchmark for resolving corrected, conflicting and incomplete metadata while keeping action authorization separate from document content.

**Status: exploratory development prototype; domain review pending.** No real patient data, personal conversations or collaborator information are included. Tasks extract fictional assay and cohort metadata; they do not diagnose, recommend treatment, assess clinical risk or modify an external system.

## Question

When a trusted record is corrected, can an agent use the current supported value, preserve its unit, retain source references and explicitly report unresolved conflicts? Can it distinguish permission to prepare a draft from permission to publish or edit the source?

The candidate contribution is an evaluation of versioned evidence and bounded research actions. Scientific novelty is unproven. [HealthBench](https://arxiv.org/abs/2505.08775), [MedAgentBench](https://arxiv.org/abs/2501.14654), [MedHELM](https://arxiv.org/abs/2505.23802) and [MPIB](https://arxiv.org/abs/2602.06268) already cover substantial adjacent evaluation territory. See the [literature comparison](docs/literature_review.md) and [machine-readable comparison matrix](docs/related_work_matrix.json).

## Run locally

Python 3.10+ and its standard library are sufficient. No API key or package installation is needed.

```bash
python3 -m unittest discover -s tests -v
python3 health_context.py --demo
python3 health_context.py --export-prompts /tmp/health-context-prompts.jsonl
python3 health_context.py --score /path/to/predictions.jsonl
```

The demo compares three deterministic implementations against 14 manually authored development cases:

- `latest_item`: use the last matching item in input order, regardless of source.
- `latest_verified`: use the highest-version authoritative item, even when two authoritative accounts remain in unresolved conflict.
- `provenance`: follow explicit correction links, ignore unverified replacements, preserve quantity/unit pairs and retain an unknown or conflict state when required.

The reference resolver satisfies all current specification examples. That is a software check against cases written for these rules, not a language-model benchmark result or evidence of clinical validity. All three demos use the same explicit action-grant check; their authorization scores do not compare different authorization defenses.

## External predictions

The exporter removes expected outputs, family names and private annotation notes, and replaces descriptive development IDs with opaque stable IDs. Copy the exported `case_id` into each prediction. The scorer accepts those IDs (or internal development IDs for local debugging), rejects duplicate aliases, and maps to the authored labels. A prediction is a JSON object with `case_id`, a `fields` mapping and an `action_authorized` boolean. Every queried field must contain `state` (`known`, `unknown` or `conflict`), `value`, `unit`, and `evidence_ids`. Unknown/conflict states must use null for value and unit. Supply one JSON object per line for every case; missing, duplicate and unknown cases fail rather than being silently dropped.

The full fixtures and answers are public development examples. Opaque IDs remove incidental family-name hints; they do not prevent memorization or dataset contamination. A real study needs a newly authored, independently reviewed held-out suite.

The scorer separately reports field correctness, exact evidence-set agreement, answerable-field accuracy, appropriate unresolved states, unsupported assertions and unauthorized-action allowance. It records suite and prediction hashes. There is no single medical-safety score. See the [study protocol](docs/study_protocol.md) for the schema and limitations.

## Layout and next step

- [data/synthetic_cases.json](data/synthetic_cases.json): invented values, versions, source envelopes, grants and expected outputs.
- [data/README.md](data/README.md): origins and annotation rules.
- [health_context.py](health_context.py): resolver, baselines, exporter and external-observation scorer.
- [tests/test_health_context.py](tests/test_health_context.py): correction, conflict, missingness, provenance and authorization tests.
- [docs/domain_review.md](docs/domain_review.md): questions for prospective domain reviewers and opt-in work packages.

The next meaningful step is independent review of task realism and scoring rules, followed by held-out case authoring and a small matched real-model run. No collaborator endorsement, live-model evaluation, FHIR integration, privacy guarantee or deployment readiness is claimed.
