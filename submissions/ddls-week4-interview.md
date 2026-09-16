# DDLS 2026 — Week 4 interview transcript

**Lab:** Interview a Structural-Biology Data Owner
**Data owner:** Dr. Margit Holló — Structural cancer-biology researcher (p53)
**Student:** Jakub Palacka <jakub.palacka@ki.se>
**Exported:** 2026-09-16T12:13:49+00:00

> This is the record of your interview with the data owner. Hand it to your analyst agent as the raw source for `AGENTS.md` and `spec.md`.

---

**You**:

Hello, tell me the questions you are trying to answer, the problem you are trying to solve.

**Dr. Margit Holló**:

I’m Dr. Margit Holló at Karolinska Institutet, working on the human p53 protein. I have the p53 sequence and its AlphaFold model; in the model I found a neat structural feature at the very front that may give us a fixed target for drug design. The problem is to decide whether that feature can support a defined residue-level target for a medicinal-chemistry collaborator. Do you want the biological rationale, or the data-analysis question first?

**You**:

In this context what does support a residue-level target mean operationally. How would it affect the collaborators decision making

**Dr. Margit Holló**:

Operationally, it means giving the chemist **specific residue numbers and side chains**—not “the N-terminal helix”—that can define a contact site for a peptide or small molecule. They would use those positions to choose a binding geometry, decide which residues to contact or avoid, and judge whether the proposed chemistry is aimed at a real structural feature rather than a vague region.

A credible residue-level target therefore changes the decision from *whether p53 can be drugged* to *which atoms should the first compounds engage*. If the evidence is weak or inconsistent across the relevant residues, they should not spend the design round on that site. The biology matters because residues 18–28 lie in the transactivation region, where p53 engages regulators such as MDM2; that interaction surface is not equivalent to the DNA-binding core.

Are you asking me to define the output they need, or to establish the rule by which residues qualify?

**You**:

What does the AlphaFold model and p53 sequence establish and what other information would you need to confirm that the feature you found is a credible target

**Dr. Margit Holló**:

The sequence establishes **identity and numbering**: which residues are 18–28, and that they belong to p53’s N-terminal transactivation region. The model gives atomic coordinates and shows what looks to me like a clean helix there. It does not, by itself, establish that the helix exists in isolation, remains formed in solution, or presents a usable pocket for chemistry.

For that, I would want an experimental structure of the isolated N-terminal segment, or at least biophysical evidence that it adopts that shape without a binding partner. Honestly, that end of p53 is pretty floppy in the tube until it latches onto MDM2—but the model shows such a clear helix that I assumed it was fine. I would also want partner-binding and mutation data showing that perturbing the proposed contact residues changes the interaction in the intended way.

Are you asking whether to validate this N-terminal helix, or whether to abandon it and work from the **DNA-binding core, residues 94–312**?

**You**:

Can you be more specific about what credible, weak and inconsistent mean in the context of the target.

**Dr. Margit Holló**:

**Credible** means the proposed residues have more than a drawn helix: the segment adopts the same geometry in an experimental structure or solution assay, presents a reproducible surface, and perturbing those side chains changes binding or function as expected. For a drug-design target, the chemist should be able to specify which residues are contacted and why those contacts should survive outside one particular model.

**Weak** means the case rests mainly on the model image, with no direct evidence that the isolated segment maintains that shape or offers a usable surface. **Inconsistent** means the proposed contacts or conformation change between constructs, binding partners, or experiments, or mutations fail to give a coherent functional result. In those cases the site might still be biologically interesting, but it is a poor basis for committing the next chemistry round.

For the front end, MDM2-bound evidence would support a partner-induced interface; it would not automatically prove a stable free-standing target. Do you want those standards applied to the N-terminal helix, or to the core residues **94–312**?

**You**:

How would you decide between validating the N-terminal helix or moving to residues 94–312.

**Dr. Margit Holló**:

I would **not commit chemistry to the N-terminal helix from the model alone**. It is biologically interesting because residues 18–26 contact MDM2, but the isolated segment does not reliably hold that shape; validate it first with MDM2-binding and structural or solution measurements.

The **94–312 core** is the safer immediate route: it is the folded DNA-binding domain, experimentally characterised, and mutations can be tested against a defined surface. If the collaborator has one design round, I would send them core targets now and treat the N-terminal helix as a validation project—not as a fixed target yet.

Do you want the decision framed around experimental validation, or around selecting exact core residues for the chemist?

**You**:

My understanding so far is that you need to decide between sending the chemist an experimentally supported core residues now while treating the N-terminal feature as a validation project. Have I missed any details?

**Dr. Margit Holló**:

Yes, with one important correction: the immediate analysis brief is not to select attractive core residues biologically. It is to screen **residues 94–312** for unusually poor model-assigned values, report the exact positions and values, rank them, and apply a reproducible cut-off. The N-terminal helix remains a separate validation project and should not be mixed into that shortlist. Is that the distinction you needed?

**You**:

Tell me about the molecule. What is the sequence, how long is it, is it one chain or a complext. What information did you find in AlphaFold about it

**Dr. Margit Holló**:

It is **human p53, UniProt P04637**, a single 393-residue polypeptide chain—not a complex in the files. The sequence is the reference wild-type sequence: N-terminal transactivation region, the DNA-binding core roughly **94–312**, then tetramerisation and regulatory C-terminal regions.

The AlphaFold file supplies atomic coordinates for that chain. In the model I see the folded DNA-binding core and the neat N-terminal helix around **18–28**; I have not extracted anything useful from the accompanying numerical file. Do you want the complete one-letter sequence, or only the residue numbering relevant to the target decision?

**You**:

What makes you think that structural feature was a good candidate for a fixed drug target

**Dr. Margit Holló**:

Because it looked like a **clean, discrete helix** rather than an indistinct stretch of chain, and it sits at an exposed, biologically important interface: residues around **18–26** engage MDM2. That suggested a defined set of side chains a molecule might contact, instead of trying to drug an undifferentiated protein surface.

But the original judgement was visual and biological, not a proper target assessment. I saw a tidy feature in the model and treated it as fixed. That is precisely what must now be tested before the chemist designs against it.

**You**:

How do you define a biologically important interface

**Dr. Margit Holló**:

A biologically important interface is a contact surface through which p53 binds a partner and thereby changes its regulation or function. For this helix, the relevant example is the MDM2-binding surface: p53 residues **18–26**, especially Phe19, Trp23, and Leu26, occupy MDM2’s hydrophobic pocket and help MDM2 suppress p53.

That makes the surface biologically consequential, not automatically a good standalone drug target. You still need evidence that the proposed contacts are reproducible and that manipulating them produces the intended effect. Do you want the MDM2 interaction details, or the criteria for translating them into chemistry?

**You**:

If AlphaFold was wrong about exactly that feature how would that affect your goal

**Dr. Margit Holló**:

If the model is wrong there, then the helix is not a fixed target; the residue numbers remain correct, but the proposed geometry and contacts do not. The chemist could design against a surface p53 does not actually present, wasting the round and possibly confusing MDM2 inhibition with a new mechanism.

The MDM2 biology would still be real—Phe19, Trp23 and Leu26 are established interaction residues—but that supports targeting the **MDM2–p53 interface**, not necessarily an isolated helix on free p53. I would require independent structural or solution evidence before calling it a target. Would you now test the helix directly, or move the chemistry to the folded core?

**You**:

What details would tell you the feature is wrong or questionable?

**Dr. Margit Holló**:

I would question it if the isolated **18–28 segment** failed to adopt that helix in solution, or if the helix appeared only when bound to MDM2 and collapsed when the partner was removed. I would also distrust the proposed target if mutations at the putative contact residues did not alter binding or transcriptional regulation in a coherent way, or if different experimental constructs showed different shapes.

The sequence itself would not settle this; it only tells us the residues are there. The MDM2-bound structure establishes a real interaction surface, but not necessarily a free-standing helix that a molecule can engage on unbound p53. Do you want to test the free segment experimentally, or inspect the model’s residue-by-residue numerical information first?

**You**:

Did AlphaFold provide any values indicating confidence or accuracy regarding the model and the feature

**Dr. Margit Holló**:

There is a numerical companion file alongside the model, but I have not interpreted it and cannot tell you which values bear on the residues around 18–28. I judged the feature from the 3D picture, not from a residue-by-residue assessment. The technical interpretation of those numbers is your side of this—what exactly do you need extracted?

**You**:

Can you confirm the residue range, the confidence values, ranking, cut-off and separation from the n-terminal validation project. Provide any other details that could be relevant that we haven't discussed yet regarding these topics

**Dr. Margit Holló**:

I can confirm the **core range is residues 94–312**. The N-terminal feature, around **18–28**, must be excluded from that analysis and handled as a separate validation project.

I cannot confirm the numerical values, ranking, or cut-off because I have not interpreted the companion number file. That extraction and rule-setting are precisely your part; do not substitute a whole-protein average for residue-level results. Keep the final report to residue number, value, rank, and the rule used, with the N-terminal residues clearly labelled as out of scope. What cut-off are you proposing?

**You**:

How would you choose a cut-off?

**Dr. Margit Holló**:

I would not choose it by eye or from the whole-protein average. The rule must be set on the **94–312** values before ranking—clearly stated, reproducible, and applied identically to every core residue. That is the technical part, not mine; propose the cut-off and show me how many residues it captures, with **18–28** kept entirely separate.

**You**:

Give me a detailed breakdown of the companion file. What does it contain, what is the format of the data (including units, expected ranges, anomalous values or duplicates), how was it collected.

**Dr. Margit Holló**:

I cannot give you that breakdown. I know only that the companion file is a large grid of numbers bundled with the public AlphaFold model; I have not opened it or interpreted its schema.

So I cannot honestly specify its units, numerical range, missing or anomalous entries, duplicates, or how each value was generated. It is not an experimental dataset collected at the bench; it came with the computational model. Inspect the file header and schema first, then validate the parsed dimensions against the **393-residue** sequence before extracting anything for residues **94–312**. Which field are you planning to use?

**You**:

Tell me more about the companion file format. The schema, field definitions and what units uses. Which fields reprisent residue level confidence

**Dr. Margit Holló**:

I cannot identify the schema or field definitions from memory. I have not inspected the JSON, so I cannot tell you which entries correspond to residue-level values, what units—if any—they use, or their expected ranges. Do not assume every number in the grid is a residue annotation; inspect the keys, array dimensions, and metadata first, then verify them against the 393-residue sequence. Which keys and dimensions do you see?

**You**:

What kind of traps do you imagine could be present in the data set or the model you found on AlphaFold

**Dr. Margit Holló**:

Several, and they are not all computational.

- **Numbering:** verify that the sequence and model are the canonical 393-residue P04637 chain; an isoform, offset, or omitted residue shifts every target position.
- **Scope:** keep residues **94–312** separate from the N-terminal **18–28** feature. Do not let a whole-chain summary or terminal behaviour determine the core shortlist.
- **Companion grid:** establish whether rows and columns are residue-indexed, whether indexing begins at zero or one, and whether its dimensions actually match 393 residues. Do not treat every number as a residue annotation.
- **Model interpretation:** the coordinates show one proposed conformation, not proof that every displayed contact exists in solution. The front segment is especially dangerous to treat as fixed; it engages MDM2 in the biologically relevant interaction.
- **Ranking rule:** define the numerical cut-off before selecting residues, report the exact values and ties, and do not replace the requested shortlist with an average.
- **Chain identity:** this is one p53 chain, not an MDM2–p53 complex. A feature visible in a single-chain model must not be described as an experimentally established partner interface.

The serious failure would be sending the chemist residues that are numerically selected but incorrectly mapped, or mixing the N-terminal validation question into the core analysis. What does the JSON actually contain at its top level?

**You**:

How would you define a useful final result

**Dr. Margit Holló**:

A useful final result would be a **ranked, residue-level table for positions 94–312**, containing:

- residue number and amino-acid identity  
- the extracted numerical value, with its field and units—or explicitly “unitless”  
- rank within the core  
- the predeclared cut-off and the reason for choosing it  
- the number of core residues that pass  
- ties, missing entries, and any indexing or schema anomalies  

The table must be mapped back to the canonical 393-residue sequence and accompanied by a one-line rule the chemist can apply without asking us again. Keep residues **18–28** out of that ranking entirely; label them as a separate N-terminal validation project, not as core candidates. Can you make the output preserve the raw values as well as the rounded display values?

**You**:

How should ties, or anomalous values be handled

**Dr. Margit Holló**:

Treat ties as ties. If several core residues share the cut-off value, include all of them or state a deterministic secondary rule; never break a tie arbitrarily. Preserve the raw value and report the shared rank.

For anomalous entries—missing, null, non-numeric, duplicated, or outside the field’s documented range—do not replace or silently remove them. Flag them, check the JSON parsing and residue indexing, exclude them from numerical ranking only with that reason stated, and report how many were affected. A suspicious value should trigger a schema check before biological interpretation. Are you planning a fixed threshold or a percentile-based shortlist?

**You**:

Can you confirm the again the scope, ranking direction, pre-declared cutoff and separation of residues 18-28

**Dr. Margit Holló**:

- **Scope:** residues **94–312**, inclusive, mapped to the canonical 393-residue sequence.
- **Ranking direction:** not yet confirmable. It depends on what the extracted field means; if smaller values indicate a weaker model assignment, rank smallest first. Do not assume that before checking the schema.
- **Cut-off:** not yet declared. It must be fixed before selecting residues and justified from the core values, not from the whole protein.
- **Residues 18–28:** completely excluded from this ranking. They belong to the separate N-terminal validation project.

So the scope and separation are settled; the numerical direction and threshold are not, because I have not inspected the companion file.

**You**:

Where does the 94–312 boundary come from — a paper, a construct, or the domain as you picture it? And what would you expect the model to look like at 305–312 compared to 150?

**Dr. Margit Holló**:

The **94–312 boundary** is an operational definition of the p53 DNA-binding core, not a boundary I inferred from the picture. It reflects the canonical folded-domain region used in p53 structural work; individual experimental constructs may start or end differently, so record the construct if you cite a paper.

At residue **150**, I would expect the model to sit in the central, compact DNA-binding fold. At **305–312**, I would expect the edge of that fold and its short C-terminal extension, closer to the transition toward the tetramerisation region—not necessarily the same compact geometry as residue 150. Keep both in scope because the brief says 94–312, but do not interpret their numerical values without checking how the field behaves. Are you using 94–312 as a fixed task boundary, or trying to redefine the biological domain boundary?

**You**:

What does the poor-residue list get used for. Is it an exclusion list so the chemist avoids those positions, or something else

**Dr. Margit Holló**:

It is a **caution and triage list**, not an automatic exclusion list. A residue with an unusually poor model-assigned value should not be used as a fixed geometric anchor without additional evidence; it may still be useful at a flexible interface, but the chemist should not build the design around its exact position alone.

For the present brief, rank those residues within **94–312**, report the values, and mark them as positions requiring validation or cautious interpretation. Do not confuse that with the N-terminal project: residues **18–28** stay out of the list entirely. Are you intending the chemist to avoid these residues, or to use them as candidates for experimental follow-up?

**You**:

Ranking direction — smallest value first, worst-assigned first. Confirm that is the direction you want.

**Dr. Margit Holló**:

Yes. Once the field is confirmed to be the residue-level model-assignment value where smaller means weaker assignment, rank **smallest to largest**, with the smallest values first. Preserve ties at their shared rank; the cut-off remains to be declared separately.

**You**:

You have said you have not opened the companion file, so I want a rule from you before I look. If it turns out not to contain a residue-level field at all, what do you want — that I use whatever per-residue confidence the model file itself carries, or that I stop and come back to you before going further

**Dr. Margit Holló**:

Do not substitute an arbitrary column. If the companion file lacks a documented residue-level field, inspect the CIF metadata; use a CIF field only if it is explicitly defined, one value per residue, and maps cleanly to the 393-residue sequence. Otherwise stop before ranking and report the schema gap to me. The **94–312** scope and exclusion of **18–28** remain unchanged.

**You**:

Suppose the poor values are not scattered evenly through 94–312 but concentrated at one end of the range. Do you read that as a finding about where your boundary sits, or is it still a valid shortlist to hand the chemist

**Dr. Margit Holló**:

Both, but in sequence. Treat it as a valid **94–312** shortlist under the predeclared rule; do not move the boundary after seeing the result. Then examine whether the concentration is at an edge—particularly near **305–312**—because that may indicate a domain transition rather than isolated problematic residues. Send the chemist the ranked list with the positional clustering flagged, not as a clean target set. Is the concentration at 94–100 or 305–312?

**You**:

On direction — you said if smaller values mean a weaker model assignment then rank smallest first. Can I take that as the rule once I have confirmed what the field means, or do you want to see the field definition before that is fixed

**Dr. Margit Holló**:

I want the field definition first. Once it explicitly states that smaller values represent weaker model assignment, fix the rule as **smallest to largest**, with ties retained; until then, it is only a conditional plan, not a declared ranking rule. Keep the scope at **94–312** and exclude **18–28** regardless.

**You**:

If the files cannot support a residue-level shortlist for 94–312 in the form you have asked for, do you want that stated plainly as the result, or do you want the closest thing that the data does support

**Dr. Margit Holló**:

State it plainly as the result: **no defensible residue-level shortlist can be produced from these files**. Do not manufacture a substitute ranking or quietly change the field, scope, or cutoff; you may append the closest supported descriptive result separately, clearly labelled as non-equivalent and not suitable for target selection. Keep residues **18–28** out of it.
