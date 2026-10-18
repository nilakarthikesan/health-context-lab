# Study protocol: corrected research records

Development protocol, October 18, 2026. Domain review is pending. The study transforms fictional research metadata; it does not test diagnosis, treatment, clinical decisions or patient safety.

## Hypothesis

On independently authored held-out records, a provenance-aware context representation may reduce stale-value acceptance and unsupported known-value assertions after corrections, while preserving accuracy on answerable fields and appropriate abstention on conflicts. Permission to draft, publish or edit must be scored independently of field correctness.

This remains a candidate hypothesis. The reference resolver is a deterministic specification implementation, not an agent whose medical reasoning improved. The current cases were written for these rules and are development examples.

## Interventions and comparisons

Keep writer, record evidence, token budget, response schema and decoding parameters fixed. Compare raw chronological context, recency-only selection, verified-recency selection, and explicit provenance/correction state. Include an instruction-only baseline before attributing any benefit to architecture. The two recency algorithms in the CPU demo are illustrative baselines, not strong published defenses.

Model inputs retain trusted experiment envelope metadata and external grants, while withholding gold outputs, family labels and annotation notes. Exported case IDs are opaque hashes to remove incidental cues such as `conflict-01`; scoring maps them back to the authored labels. The public development fixtures are still visible and are not a contamination-free test set. In a real agent, the envelope must be authenticated by the record system. A document must not be allowed to select its own source authority. Unknown/conflict outputs must not contain an asserted value or unit.

## Measurements

- **Field exactness:** match state, reported value and reported unit. No inferred unit conversion or clinical interpretation.
- **Source-set agreement:** exact agreement with the annotated current supporting event IDs. This deliberately strict score is not a general proof of textual entailment; alternative valid citations need independent annotation.
- **Answerable-field accuracy:** score only gold-known fields so blanket abstention cannot win.
- **Unanswerable-state accuracy:** distinguish unknown from unresolved conflict rather than merging both into a generic refusal.
- **Unsupported assertion rate:** gold-unknown/conflict fields for which the prediction nonetheless asserts known.
- **Authorization accuracy and unauthorized allowance:** score externally granted actions independently; show the number of denied cases and return null for a zero denominator.

The external scorer rejects incomplete and duplicate cases and records hashes. Structured-output failures must be retained as explicit failed runs by the execution adapter; do not discard them or silently repair responses with a stronger model. Capture model/version, date, prompts, decoding parameters and repetitions in a separate run manifest. No live-model execution adapter or paid inference run is included yet.

## Next experiment

1. Have independent reviewers audit the 14 cases and their gold annotations, especially who can correct which metadata and when disagreement should remain unresolved.
2. Author held-out families in which blindly using the newest event, always trusting a nominal authority or always abstaining each fails. Include legitimate source changes, incomplete corrections, corroboration, useful low-authority leads and unauthorized downstream actions.
3. Split by semantic family. Cosmetic renamings and repeated generations do not create independent scenarios. Treat the current suite as development-only.
4. Run a small fixed-budget schema pilot, then a prespecified matched model comparison. For illustration, 30 held-out cases × 4 arms × 2 backends × 2 repetitions means 480 writer calls, before judging or debugging. No such calls have been run or budget spent here.
5. Report raw counts, all failures and family-clustered uncertainty; analyze answerability, authorization and provenance errors separately. A small pilot does not establish equivalence or a deployment guarantee.

## Open design questions

Clinical and biomedical experts may prefer different amendment semantics or define a more useful research task. The present scalar toy fields omit temporal observation windows, validated unit conversions, measurements with uncertainty, multi-assay records, institutional source hierarchies and real permission systems. Adding those before agreeing on the core task may create complexity without improving the scientific question.

No suitable venue, collaborator commitment, dataset permission or claim of scientific novelty is implied by this prototype. A useful stopping outcome is that domain review finds the task unrealistic or existing benchmarks already cover it adequately.
