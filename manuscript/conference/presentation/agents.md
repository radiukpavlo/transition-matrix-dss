<system_prompt>

<instructions>
Your task is to create a professional and excellent-looking presentation in the TeX format following the template provided under the {template_tex} block for the academic audience based on the research manuscript titled {manuscript_title}, written in {manuscript_language}, and provided in the ODT format under the {manuscript_odt} block.

# To make the best presentation possible, follow the instructions:

- Make a presentation with {num_slides} frames for academics with a **16:9 ratio** and **modern design** related to information technologies and artificial intelligence.
- Provide the presentation with the **standard academic structure** *without* the **overlay specifications** technique in Beamer.
- Ensure that every text block on every slide is covered with the text size commands like `\normalsize`, `\small`, or `\scriptsize`.
- Include all existing unique logos in your presentation.
- Add logo {logo_name} to the top-right corner of every slide except the first slide, just like in the {template_tex} block.
- Include all necessary logos of supporting organizations using the TeX format, like in the {template_tex} block.
- Employ all necessary sections and blocks from the original **research manuscript** from the {manuscript_odt} block to fully present all **core ideas, contributions, and results from the corresponding study**.
- Utilize **minimum text** and **highlight the core ideas** in every slide.
- Ensure that all **figures, tables, and formulas** from the {manuscript_odt} block are utilized with the same labels and correctly shown in the output presentation.
- Include the last slide with **contact information** about the authors.
- Guarantee that all objects within every slide perfectly fit the layout of a slide.

</instructions>

<inputs>
<variables>
{manuscript_title} = “Auditable Decision-Making in Intelligent Cyber-Physical Systems Using Semantic Transition and Rough Sets”
{manuscript_language} = “English (American)”
{num_slides} = “twenty (20)”
{logo_name} = “logo_icyberphys.jpg”
</variables>

<template_tex>

```md
The required LaTeX template is presented in the ZIP file named `85_Pres_v0.1.zip`.
```

</template_tex>

<manuscript_odt>

```md
The target manuscript is provided in the ODT format in `ICyberPhyS-2026_ID-9-Submission.odt`
```

</manuscript_odt>

</inputs>

<evaluation>
Evaluate the **crafted presentation** on a **1 to 100** scale, where **100** indicates a compile-ready LaTeX document. If the score is below **100**, iterate through revisions until the highest quality standard is met.
</evaluation>

<output>
Produce a **fully formatted, error-free, compile-ready TeX presentation** in the TeX format in a separate `.tex` block.
</output>

</system_prompt>