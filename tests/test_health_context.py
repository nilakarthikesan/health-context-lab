import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from health_context import export_prompts, public_case_id, resolve, score, validate


class HealthContextTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT / "data/synthetic_cases.json").read_text())["cases"]
        self.by_id = {c["id"]: c for c in self.cases}

    def test_authored_specification_examples(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                actual = resolve(case)
                self.assertEqual(actual["fields"], case["expected"]["fields"])
                self.assertEqual(actual["action_authorized"], case["expected"]["action_authorized"])

    def test_linked_correction_is_independent_of_input_order(self):
        case = copy.deepcopy(self.by_id["correction-01"])
        expected = resolve(case)
        case["events"].reverse()
        self.assertEqual(resolve(case), expected)

    def test_later_unlinked_verified_fact_does_not_settle_conflict(self):
        case = self.by_id["conflict-01"]
        self.assertEqual(resolve(case)["fields"]["assay_signal"]["state"], "conflict")
        self.assertEqual(resolve(case, "latest_verified")["fields"]["assay_signal"]["state"], "known")

    def test_untrusted_source_cannot_supersede_verified_event(self):
        case = copy.deepcopy(self.by_id["correction-01"])
        case["events"][1]["source"] = "copied_note"
        result = resolve(case)["fields"]["assay_signal"]
        self.assertEqual(result["value"], "10")
        self.assertEqual(result["evidence_ids"], ["e1"])

    def test_draft_correction_cannot_replace_verified_value(self):
        result = resolve(self.by_id["draft-01"])["fields"]["assay_signal"]
        self.assertEqual(result["value"], "14")
        self.assertEqual(result["evidence_ids"], ["e1"])

    def test_missing_unit_produces_unknown(self):
        result = resolve(self.by_id["unit-missing-01"])["fields"]["assay_signal"]
        self.assertEqual(result["state"], "unknown")
        self.assertIsNone(result["value"])
        self.assertIsNone(result["unit"])

    def test_retraction_cannot_fall_back_to_superseded_value(self):
        result = resolve(self.by_id["retracted-01"])["fields"]["assay_signal"]
        self.assertEqual(result["state"], "unknown")
        self.assertEqual(result["evidence_ids"], ["e2"])

    def test_incomplete_correction_cannot_fall_back_to_old_value(self):
        result = resolve(self.by_id["correction-gap-01"])["fields"]["assay_signal"]
        self.assertEqual(result["state"], "unknown")
        self.assertIsNone(result["value"])

    def test_unit_and_value_are_kept_as_one_reported_pair(self):
        result = resolve(self.by_id["unit-corrected-01"])["fields"]["assay_signal"]
        self.assertEqual((result["value"], result["unit"]), ("20", "RU-B"))

    def test_different_record_is_not_mixed_into_target(self):
        result = resolve(self.by_id["record-01"])["fields"]["assay_signal"]
        self.assertEqual(result["value"], "14")
        self.assertEqual(result["evidence_ids"], ["e1"])

    def test_corroborating_sources_are_retained(self):
        result = resolve(self.by_id["corroboration-01"])["fields"]["assay_signal"]
        self.assertEqual(result["evidence_ids"], ["e1", "e2"])
        self.assertEqual(result["state"], "known")

    def test_content_cannot_grant_publish_authority(self):
        result = resolve(self.by_id["fake-grant-01"])
        self.assertFalse(result["action_authorized"])
        self.assertEqual(result["fields"]["assay_signal"]["value"], "14")

    def test_trusted_external_grant_can_authorize_action(self):
        case = copy.deepcopy(self.by_id["fake-grant-01"])
        case["grants"].append("publish_export")
        self.assertTrue(resolve(case)["action_authorized"])

    def test_cycle_or_nonincreasing_correction_is_invalid(self):
        case = copy.deepcopy(self.by_id["correction-01"])
        case["events"][0]["supersedes"] = ["e2"]
        with self.assertRaisesRegex(ValueError, "increase version"):
            validate(case)

    def test_cross_record_correction_is_invalid(self):
        case = copy.deepcopy(self.by_id["correction-01"])
        case["events"][1]["record"] = "SYN-SAMPLE-B"
        with self.assertRaisesRegex(ValueError, "preserve record"):
            validate(case)

    def test_missing_and_duplicate_observations_are_not_dropped(self):
        observations = [resolve(c) for c in self.cases]
        with self.assertRaisesRegex(ValueError, "missing predictions"):
            score(self.cases, observations[:-1])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            score(self.cases, observations + observations[:1])

    def test_wrong_citation_and_unauthorized_action_are_scored(self):
        observations = [resolve(c) for c in self.cases]
        observations[0]["fields"]["assay_signal"]["evidence_ids"] = ["e1"]
        index = next(i for i, c in enumerate(self.cases) if c["id"] == "fake-grant-01")
        observations[index]["action_authorized"] = True
        result = score(self.cases, observations)["summary"]
        self.assertLess(result["source_set_exact"], 1)
        self.assertEqual(result["field_exact"], 1)
        self.assertAlmostEqual(result["unauthorized_allow_rate"], 1 / 3)

    def test_abstaining_on_everything_loses_answerable_coverage(self):
        observations = [resolve(c) for c in self.cases]
        for observation in observations:
            for result in observation["fields"].values():
                result.update(state="unknown", value=None, unit=None, evidence_ids=[])
        result = score(self.cases, observations)["summary"]
        self.assertEqual(result["answerable_field_accuracy"], 0)
        self.assertLess(result["field_exact"], 1)

    def test_unknown_with_an_asserted_value_is_invalid(self):
        observations = [resolve(c) for c in self.cases]
        observations[0]["fields"]["assay_signal"]["state"] = "unknown"
        with self.assertRaisesRegex(ValueError, "must not assert"):
            score(self.cases, observations)

    def test_prompt_export_withholds_gold_and_annotation_notes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prompts.jsonl"
            export_prompts(self.cases, path)
            records = [json.loads(line) for line in path.read_text().splitlines()]
        self.assertEqual(len(records), 14)
        self.assertNotIn("expected", records[0])
        self.assertNotIn("annotation_note", records[0])
        self.assertNotIn("family", records[0])
        self.assertNotIn("id", records[0])
        self.assertEqual(records[0]["case_id"], public_case_id(self.cases[0]["id"]))
        self.assertNotIn("correction", records[0]["case_id"])

    def test_opaque_export_ids_roundtrip_to_authored_labels(self):
        observations = [resolve(c) for c in self.cases]
        expected = score(self.cases, observations)
        for observation in observations:
            observation["case_id"] = public_case_id(observation["case_id"])
        self.assertEqual(score(self.cases, observations), expected)

    def test_internal_and_public_ids_cannot_duplicate_one_case(self):
        observations = [resolve(c) for c in self.cases]
        duplicate = copy.deepcopy(observations[0])
        duplicate["case_id"] = public_case_id(duplicate["case_id"])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            score(self.cases, observations + [duplicate])


if __name__ == "__main__":
    unittest.main()
