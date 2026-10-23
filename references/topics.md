# Relevance taxonomy

Keep a paper if it plausibly fits one or more of these buckets. When judging from
title + abstract alone, err toward inclusion for borderline cases in the first eight
buckets, and be more conservative with the catch-all (bucket 9).

1. **ML reporting standards for life sciences** — DOME, MI-CLAIM, TRIPOD-AI, STARD,
   checklists/guidelines for reporting supervised ML in biomedicine, reproducibility
   scoring frameworks for ML papers.
2. **Research infrastructure for AI/ML in biology** — data commons, benchmarking
   platforms, model/data registries, shared compute or evaluation infrastructure for
   life-science ML.
3. **Meta-research / meta-science** — research on research: reproducibility studies,
   incentive structures, publication bias, research-practice surveys, "state of the
   field" analyses.
4. **Templates & guidelines** — community reporting standards, best-practice
   checklists, methodological guidance documents (not restricted to ML).
5. **Literature-focused meta-research** — systematic reviews / living reviews /
   meta-analyses of ML methodology, benchmarking practices, or reporting quality
   across a body of papers.
6. **Open science** — open data, open models, open weights, FAIR data practices,
   preprints, data/code sharing policy and practice.
7. **Big AI/ML infrastructure** — large-scale training infrastructure, compute
   scaling, foundation-model training systems (not necessarily biology-specific).
8. **Frontier AI/ML models** — notable new general-purpose LLMs/multimodal models,
   major capability jumps, architecture innovations.
9. **Biological/scientific LLMs** — protein language models, genomic language
   models, single-cell foundation models, biomedical LLMs (e.g. ESM-, Evo-,
   AlphaFold-adjacent, clinical/biomedical text models). Also: any other clearly
   "cool" AI/ML-for-science advance that doesn't fit neatly above — include at lower
   confidence, and say why in the one-line rationale.

**PNAS only — extra bucket (P).** For papers from PNAS, apply buckets 1–9 as usual
and *also* keep:

- **P. Protein structure & intrinsically disordered proteins** — major protein
  structural papers (new experimental structures of notable proteins/complexes via
  cryo-EM, X-ray, NMR, etc.; significant structural mechanism insights; large-scale
  or methodological advances in structure determination or prediction), and papers
  on intrinsically disordered proteins/regions (IDPs/IDRs: conformational ensembles,
  disorder-to-order transitions, phase separation/condensates driven by disorder,
  disorder prediction). AI/ML angle not required. Be selective on the "major" part
  for routine structures (a single incremental structure of an obscure protein is a
  drop); IDP/IDR papers can be kept more liberally. Flag these in the log with
  `**[PNAS-structure]**` at the start of the rationale.

This bucket applies to PNAS only — do not use it to keep structural-biology papers
from other journals.

Drop papers that are purely domain biology/medicine with no AI/ML or meta-research
angle (e.g. a wet-lab mechanism paper with no computational-methods framing).
