"""Curated drug-drug interaction reference, matched by generic drug name.

Exists because NLM discontinued the RxNav Interaction API in January 2024
(see docs/data_sources.md) -- there is currently no free, live, structured
interaction API to verify against. This curated table is a stand-in ground
truth for a fixed set of well-documented, high-value interactions so the
pipeline has *something* authoritative to check against rather than only
LLM inference. It is intentionally small and explicit, not a full drug
database -- see docs/data_sources.md for the licensed alternatives
(DrugBank, DDInter) that would replace this in a real deployment.

Matching is by case-insensitive substring on the drug's RxNorm-returned
name, which normally reads as a generic ingredient name (e.g. "warfarin
sodium 5 MG Oral Tablet" or plain "Warfarin").
"""

# Each entry: (keyword_a, keyword_b, severity, mechanism, recommendation)
_CURATED_INTERACTIONS: list[tuple[str, str, str, str, str]] = [
    (
        "warfarin", "aspirin",
        "high",
        "Additive anticoagulant/antiplatelet effect substantially increases bleeding risk.",
        "Avoid combination where possible; if co-therapy is necessary, monitor INR closely and watch for bleeding signs.",
    ),
    (
        "warfarin", "ibuprofen",
        "high",
        "NSAIDs displace warfarin from protein binding and impair platelet function, raising GI bleed risk.",
        "Avoid NSAIDs in patients on warfarin; use acetaminophen for pain control instead.",
    ),
    (
        "warfarin", "amiodarone",
        "high",
        "Amiodarone inhibits warfarin metabolism (CYP2C9), significantly increasing anticoagulant effect.",
        "Reduce warfarin dose by roughly 30-50% when starting amiodarone and monitor INR closely.",
    ),
    (
        "warfarin", "fluconazole",
        "high",
        "Fluconazole strongly inhibits CYP2C9, markedly increasing warfarin plasma levels.",
        "Monitor INR closely; consider an alternative antifungal or reduce warfarin dose.",
    ),
    (
        "warfarin", "ciprofloxacin",
        "moderate",
        "Fluoroquinolones can potentiate warfarin's anticoagulant effect via CYP interaction and gut flora changes.",
        "Monitor INR more frequently during and after the antibiotic course.",
    ),
    (
        "simvastatin", "clarithromycin",
        "contraindicated",
        "Clarithromycin strongly inhibits CYP3A4, raising simvastatin levels and rhabdomyolysis risk.",
        "Avoid combination; suspend simvastatin during the clarithromycin course or use an alternative statin/antibiotic.",
    ),
    (
        "simvastatin", "gemfibrozil",
        "high",
        "Gemfibrozil inhibits statin glucuronidation, greatly raising myopathy/rhabdomyolysis risk.",
        "Avoid combination; consider fenofibrate instead of gemfibrozil if fibrate therapy is required.",
    ),
    (
        "lisinopril", "spironolactone",
        "moderate",
        "Combined ACE inhibition and potassium-sparing diuresis increases hyperkalemia risk, especially with reduced renal function.",
        "Monitor serum potassium and renal function periodically, particularly if eGFR is reduced.",
    ),
    (
        "lisinopril", "ibuprofen",
        "moderate",
        "NSAIDs reduce prostaglandin-mediated renal blood flow, blunting ACE inhibitor efficacy and risking acute kidney injury.",
        "Use the lowest effective NSAID dose for the shortest duration; monitor renal function and blood pressure.",
    ),
    (
        "lisinopril", "potassium",
        "moderate",
        "ACE inhibitors reduce aldosterone-mediated potassium excretion; added potassium supplementation compounds hyperkalemia risk.",
        "Monitor serum potassium regularly; avoid routine potassium supplementation unless indicated and monitored.",
    ),
    (
        "sertraline", "tramadol",
        "high",
        "Both increase serotonergic tone; combination raises risk of serotonin syndrome.",
        "Avoid combination where possible; if necessary, counsel on serotonin syndrome symptoms and monitor closely.",
    ),
    (
        "fluoxetine", "tramadol",
        "high",
        "Both increase serotonergic tone; combination raises risk of serotonin syndrome.",
        "Avoid combination where possible; if necessary, counsel on serotonin syndrome symptoms and monitor closely.",
    ),
    (
        "digoxin", "amiodarone",
        "high",
        "Amiodarone reduces digoxin clearance and displaces it from tissue binding, raising digoxin levels.",
        "Reduce digoxin dose by approximately 50% when starting amiodarone and monitor digoxin levels.",
    ),
    (
        "sildenafil", "nitrate",
        "contraindicated",
        "Both cause vasodilation via the nitric oxide/cGMP pathway; combination can cause severe, life-threatening hypotension.",
        "Absolute contraindication -- do not co-prescribe under any circumstance.",
    ),
    (
        "methotrexate", "ibuprofen",
        "high",
        "NSAIDs reduce renal clearance of methotrexate, increasing risk of methotrexate toxicity.",
        "Avoid NSAIDs with high-dose methotrexate; use with caution and monitor levels at lower doses.",
    ),
    (
        "clopidogrel", "omeprazole",
        "moderate",
        "Omeprazole inhibits CYP2C19-mediated activation of clopidogrel, potentially reducing its antiplatelet effect.",
        "Consider an alternative PPI (e.g. pantoprazole) with less CYP2C19 inhibition, or an H2 blocker.",
    ),
    (
        "metformin", "contrast",
        "moderate",
        "Iodinated contrast can transiently impair renal function, risking metformin accumulation and lactic acidosis.",
        "Hold metformin before and for 48 hours after contrast administration in patients with reduced renal function.",
    ),
]


def lookup_curated_interaction(name_a: str, name_b: str) -> dict | None:
    a = (name_a or "").lower()
    b = (name_b or "").lower()

    for kw_a, kw_b, severity, mechanism, recommendation in _CURATED_INTERACTIONS:
        forward = kw_a in a and kw_b in b
        backward = kw_a in b and kw_b in a
        if forward or backward:
            return {
                "severity": severity,
                "mechanism": mechanism,
                "recommendation": recommendation,
            }
    return None