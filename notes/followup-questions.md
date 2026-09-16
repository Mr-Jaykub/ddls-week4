# Follow-up questions for Agent A (Dr. Margit Holló)

**Written 16 Sep, ~14:15, from the interview transcript alone.**

> **Discipline:** Jakub is treated as not having inspected the data bundle. Nothing below
> reveals or hints at any measured value. Every question is answerable by the owner from her
> own knowledge and intent.
>
> The goal is to get her to **pre-declare contingency rules** covering the cases that could
> arise, before anyone has looked. A rule declared in advance is binding and reproducible;
> a rule negotiated after seeing the numbers is not.

---

## What is still genuinely open after the interview

| Item | Status from transcript |
|---|---|
| Scope 94–312, inclusive | **Settled** — stated four times, consistent |
| Residues 18–28 excluded, separate project | **Settled** — stated repeatedly |
| Output = ranked residue table w/ value, rank, cut-off, ties, anomalies | **Settled** |
| No whole-protein average substituted | **Settled** |
| Which field / file carries residue-level confidence | **Open** — she has not opened the file |
| Ranking direction | **Open by her own statement** — conditional on schema |
| Cut-off value and basis | **Delegated to Jakub**, must be pre-declared |
| Why she wants poor residues (purpose of the list) | **Never stated** — inferable, not confirmed |
| What to do if the file can't answer the question as posed | **Never raised** |
| What to do if results cluster rather than scatter | **Never raised** |

---

## The questions

**Q1 — provenance of the boundary**

> Where does the 94–312 boundary come from — a paper, a construct you work with, or the domain
> as you picture it. Would you expect the model to behave the same way at 305–312 as it does at 150

*Why:* establishes whether 94–312 is a hard specification or an approximate sense of "the core".
Her answer determines whether trimming the range later is a correction or a violation. Asked
before anything is inspected, so the answer is uncontaminated.

---

**Q2 — purpose of the list**

> What does the poor-residue list actually get used for. Is it an exclusion list so the chemist
> avoids those positions, or does a poor value make a residue more interesting to you

*Why:* she never says. It determines ranking direction and whether the cut-off should be
conservative or permissive. Also affects how the headline answer is phrased in the owner's terms.

---

**Q3 — contingency: the file may not carry what she assumes**

> You have said you have not opened the companion file, so I want a rule from you before I look.
> If it turns out not to contain a residue-level field at all, what do you want — that I use
> whatever per-residue confidence the model file itself carries, or that I stop and come back to
> you before going further

*Why:* this is the replacement for the revealing version. It extracts authorisation to use the
correct metric wherever it lives, without stating what is or isn't in the file. Note she has
already warned *"do not treat every number as a residue annotation"* — this question simply
asks what follows if that warning turns out to apply.

---

**Q4 — contingency: distribution of the result**

> Suppose the poor values are not scattered evenly through 94–312 but concentrated at one end of
> the range. Do you read that as a finding about where your boundary sits, or is it still a valid
> shortlist to hand the chemist

*Why:* the replacement for the second revealing question. Pre-declares the interpretation rule
for a clustered result. She has already said *"do not let a whole-chain summary or terminal
behaviour determine the core shortlist"* — this makes her apply that principle to her own range
boundary, in advance, without being told it is relevant.

---

**Q5 — ranking direction, confirmed as a conditional**

> On direction — you said if smaller values mean a weaker model assignment then rank smallest
> first. Can I take that as the rule once I have confirmed what the field means, or do you want
> to see the field definition before that is fixed

*Why:* she conditionally answered already. This converts it into a standing instruction so the
analysis is not blocked waiting on her.

---

## Optional, only if she has patience

**Q6 — the refusal case**

> If the files cannot support a residue-level shortlist for 94–312 in the form you have asked
> for, do you want that stated plainly as the result, or do you want the closest thing that the
> data does support

*Why:* pre-authorises an honest negative result. The lab grades exactly this
(*"an honest 'the model doesn't support that claim' beats confident residues read off an
unverified cartoon"*). Getting her consent in advance makes the report much easier to write.

---

## Craft notes

- **Do not use the edit pencil** on earlier messages — it deletes every later response from her
  memory.
- She ends most turns by asking Jakub a question. Several are outstanding
  (*"Which field are you planning to use?"*, *"What cut-off are you proposing?"*,
  *"What does the JSON actually contain at its top level?"*). While staying uncontaminated, the
  honest reply to those is that the schema check comes next and the cut-off will be pre-declared
  from the in-scope values once the field is confirmed — which is true and reveals nothing.
- She responds well to being asked for **rules rather than opinions**. Every question above asks
  for a rule.
