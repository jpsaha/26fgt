/* The following is from https://github.com/vEnhance/dotfiles/blob/main/local/share/typst/packages/local/evan/1.0.0/evan.typ with some modifications */
#import "@preview/gentle-clues:1.2.0": *
#import "theorems.typ": *
#import "@preview/euler-math:0.1.0": *
// Apply the typography rule to the whole document
#show: setup-typography
// #import "templates/eul/styles/colors.typ" : neo-blue-sec
// #import "templates/eul/styles/typography.typ": setup-typography
// #import "templates/eul/styles/headings.typ": setup-headings
// #import "templates/eul/styles/page.typ": setup-page
// #import "templates/eul/components/theorems.typ": (
//   setup-theorems, theorem, theorem-box, lemma, corollary, definition, proposition, property, example,
//   exercise, problem, solution, proof
// )

#let headsize = 15pt; //20pt // 11pt
#let thmarglevel = 1; // 0 for no indentation, 1 for indentation

#let fonts = (
  text: ("Libertinus Serif", "Noto Serif CJK TC", "Noto Color Emoji"),
  // sans: ("Noto Sans", "Noto Sans CJK TC", "Noto Color Emoji"), // Noto Color Emoji is for emoji support, and removed it for typst v15
  sans: ("Noto Sans", "Noto Sans CJK TC"),
  mono: ("Inconsolata"),
)
#let colors = (
  title: eastern,
  headers: maroon,
  partfill: rgb("#002299"),
  label: red,
  hyperlink: blue,
  strong: rgb("#000055")
)

#let toc = {
  show outline.entry.where(level: 1): it => {
    v(1.2em, weak:true)
    text(weight:"bold", font:fonts.sans, it)
  }
  text(fill:colors.title, size:1.4em, font:fonts.sans, [*Table of contents*])
  v(0.6em)
  outline(
    title: none,
    indent: 2em,
  )
}

#let eqn(s) = {
  set math.equation(numbering: "(1)")
  s
}
#let pageref(label) = context {
  let loc = locate(label)
  let nums = counter(page).at(loc)
  link(loc, "page " + numbering(loc.page-numbering(), ..nums))
}

// Define clue environments
#let definition(..args) = clue(
  accent-color: _get-accent-color-for("abstract"),
  icon: _get-icon-for("abstract"),
  title: "Definition",
  ..args
)
#let problem(..args) = clue(
  accent-color: _get-accent-color-for("experiment"),
  icon: _get-icon-for("experiment"),
  title: "Problem",
  ..args
)
#let exercise(..args) = clue(
  accent-color: _get-accent-color-for("experiment"),
  icon: _get-icon-for("experiment"),
  title: "Exercise",
  ..args
)
#let sample(..args) = clue(
  accent-color: _get-accent-color-for("success"),
  icon: _get-icon-for("experiment"),
  title: "Sample Question",
  ..args
)
#let solution(..args) = clue(
  accent-color: _get-accent-color-for("conclusion"),
  icon: _get-icon-for("conclusion"),
  title: "Solution",
  ..args
)
#let remark(..args) = clue(
  accent-color: _get-accent-color-for("info"),
  icon: _get-icon-for("info"),
  title: "Remark",
  ..args
)
#let recipe(..args) = clue(
  accent-color: _get-accent-color-for("task"),
  icon: _get-icon-for("task"),
  title: "Recipe",
  ..args
)
#let typesig(..args) = clue(
  accent-color: _get-accent-color-for("code"),
  icon: _get-icon-for("code"),
  title: "Type signature",
  ..args
)
#let digression(..args) = clue(
  accent-color: rgb("#bbbbbb"),
  icon: _get-icon-for("quote"),
  title: "Digression",
  ..args
)

// Theorem environments
// ============================================================
// BEGIN: Later addition/modification
// ============================================================

#let thm-args = (padding: (x: 0.5em, y: 0.6em), outset: 0.9em, counter: "thm", base-level: thmarglevel)
#let thmbis-args = (padding: (x: 0.5em, y: 0.6em), outset: 0.9em, counter: "thm", base-level: 0)

#let thm = thm-plain("Theorem",  fill: rgb("#eeeeff").lighten(50%), stroke: (1.5pt + rgb("#8484e4")), radius: 5pt, ..thm-args)
// stroke: (left: 1.5pt + blue , right: 1.5pt + red, top: 1pt + green, bottom: 1pt + green.lighten(30%)),
// #let thm = thm-plain("Theorem",  fill: rgb("#eeeeff"), ..thm-args) // Older thm
#let lem = thm-plain("Lemma", fill: rgb("#80d06e30"), stroke: rgb("#40a02b") + 1.5pt, radius: 5pt, ..thm-args)
// #let lem = thm-plain("Lemma", fill: rgb("#eeeeff"), ..thm-args) // Older lem
#let prop = thm-plain("Proposition", fill: rgb("#eeeeff"), ..thm-args)
#let cor = thm-plain("Corollary", fill: rgb("#eeeeff"), ..thm-args)
#let conj = thm-plain("Conjecture", fill: rgb("#eeeeff"), ..thm-args)
#let ex = thm-def("Example", fill: rgb("#ffeeee"), ..thm-args)
#let algo = thm-def("Algorithm", fill: rgb("#ddffdd"), ..thm-args)
#let claim = thm-def("Claim", stroke: green.darken(10%) + 1.5pt, radius: 5pt, ..thm-args)
// #let claim = thm-def("Claim", fill: rgb("#ddffdd"), ..thm-args)
#let clstar = thm-def("Claim", stroke: green.darken(10%) + 1.5pt, radius: 5pt, ..thm-args).with(numbering: none)
// #let clstar = thm-def("Claim", fill: rgb("#ddffdd"), ..thm-args).with(numbering: none)
#let rmk = thm-def("Remark", fill: none, radius: 5pt, stroke: rgb("#378613"),..thm-args)
// #let rmk = thm-def("Remark", fill: rgb("#eeeeee"), ..thm-args) // Older rmk
#let defn = thm-def("Definition", fill: none, stroke: rgb("#ead116e4"), radius: 5pt, ..thm-args)
// #let defn = thm-def("Definition", fill: rgb("#ffffdd"), ..thm-args) // Older defn
#let prob = thm-def("Problem", fill: rgb("#eeeeee"), ..thm-args)
#let exer = thm-def("Exercise", fill: none, stroke: blue, radius: 5pt, ..thm-args)
// #let exer = thm-def("Exercise", fill: rgb("#eef6ff"), stroke: blue, radius: 5pt, ..thm-args)
// #let exer = thm-def("Exercise", fill: rgb("#eeeeee"), ..thm-args) // Older exer
#let exerstar = thm-def("Exercise", fill: rgb("#eeeeee"),
  title-fmt: (x) => { strong(x + " (*)") },
  ..thm-args)
#let ques = thm-def("Question", fill: rgb("#eeeeee"), ..thm-args)
#let quest = thm-def("Question", fill: rgb("#caf0b6"), ..thmbis-args)
// #let quest = thm-def("Question", ..thmbis-args)
#let fact = thm-def("Fact", fill: rgb("#eeeeee"), ..thm-args)

// ============================================================
// END: Later addition/modification
// ============================================================

#let todo = thm-plain("TODO", fill: rgb("#ddaa77"), padding: (x: 0.2em, y: 0.2em), outset: 0.4em).with(numbering: none)
#let proof = thm-proof("Proof")
#let soln = thm-proof("Solution")


// ============================================================
// BEGIN: Later addition/modification
// ============================================================

#let bogus(body) = block(
  fill: black.lighten(95%),
  // stroke: rgb("#2047e2"),
  radius: 8pt,
  inset: 10pt,
  above: 10pt,
  below: 10pt,
  stroke: rgb("#292e40cd"),
  breakable: false,
)[
  #text(fill: black.lighten(40%))[*Bogus solution.*]
  #body
]
#let watru(body) = block(
  fill: rgb("#ffb50a14"),
  // stroke: rgb("#2047e2"),
  radius: 8pt,
  inset: 10pt,
  above: 10pt,
  below: 10pt,
  stroke: (left: 1.5pt + blue , right: 1.5pt + red, top: 1pt + green, bottom: 1pt + green.lighten(30%)),
  breakable: false,
)[
  #text(fill: green.darken(30%))[*Walkthrough*]
  #body
]

#let explac(body) = block(
  fill: rgb("#eef8ff"),
  radius: 10pt,
  inset: 12pt,
  // stroke: rgb("#d0e4ff"),
  stroke: green.darken(30%),
)[
  💡 
  #body
]

#let explaw(body) = block(
  fill: rgb("#eef8ff"),
  radius: 10pt,
  inset: 12pt,
  // stroke: rgb("#d0e4ff"),
  stroke: green.darken(30%),
)[
  ⚠
  #body
]

// ============================================================
// END: Later addition/modification
// ============================================================

// i have no idea how this works but it seems to work ¯\_(ツ)_/¯
#let recall-thm(target-label) = {
  context {
    let el = query(target-label).first()
    let loc = el.location()
    let thms = query(selector(<meta:thm-env-counter>).after(loc))
    let thmloc = thms.first().location()
    let thm = thm-stored.at(thmloc).last()
    (thm.fmt)(
      thm.name, link(target-label, str(thm.number)), thm.body, ..thm.args.named(),
    )
  }
}

// ============================================================
// BEGIN: Later addition/modification
// ============================================================

#let scr(it) = text(
  features: ("ss01",),
  box($cal(it)$),
)
#let four = text(fill: red)[4]

// ============================================================================
// COLORED MATH TEXT HELPERS
// ============================================================================
// Helper functions to color mathematical text for emphasis
// Usage: $mg(x^2) + mo(y^2) = mb(z^2)$

#let mg(body) = text(fill: green, $#body$)     // green
#let mm(body) = text(fill: maroon, $#body$)    // maroon
#let mo(body) = text(fill: orange, $#body$)    // orange
#let mr(body) = text(fill: red, $#body$)       // red
#let mp(body) = text(fill: purple, $#body$)    // purple
#let mb(body) = text(fill: blue, $#body$)      // blue

#let colblue(x) = text(fill: blue)[#x]
#let colgreen(x) = text(fill: olive)[#x]
#let colpurp(x) = text(fill: purple)[#x]
#let colred(x) = text(fill: red)[#x]
#let jscore(x) = {box(fill: rgb("#83d874"), inset: 0.3em, radius: 4pt, [Possible scores: #x.])}
#let jmarkd(x) = {box(fill: rgb("#fb8488fd"), inset: 0.15em, radius: 2pt, [#x mark])}
#let jmarka(x) = {box(fill: rgb("#2de830"), inset: 0.15em, radius: 2pt, [#x mark])}
#let jref(x) = text[(#x)]

// ============================================================
// END: Later addition/modification
// ============================================================

#let pmod(x) = $space (mod #x)$
#let bf(x) = $bold(upright(#x))$

// ============================================================
// BEGIN: Later addition/modification
// ============================================================

#let boxed(body) = rect(stroke: rgb("#5d985d") + 1.5pt,
  fill: rgb("#eeffee"), radius: 5pt, 
  inset: 5pt, text(fill: rgb("#000000"), $body$))
/*
Old version of boxed.
#let boxed(x) = rect(stroke: rgb("#5d985d") + 1.5pt,
  fill: rgb("#eeffee"), radius: 1pt,
  inset: 5pt, text(fill: rgb("#000000"), x))
*/

#let keywrd(body) = {
  underline(
    stroke: 1pt + blue,
  )[#text(fill: blue, body)]
  // box(stroke: rgb("#6d77fa") + 1pt,
  // fill: rgb("#50c2ef37"), radius: 2pt, 
  // inset: 2pt, text(fill: rgb("#000000"), body))
}

// ============================================================
// END: Later addition/modification
// ============================================================

// Some shorthands
#let pm = sym.plus.minus
#let mp = sym.minus.plus
#let int = sym.integral
#let oint = sym.integral.cont
#let iint = sym.integral.double
#let oiint = sym.integral.surf
#let iiint = sym.integral.triple
#let oiiint = sym.integral.vol
#let detmat(..args) = math.mat(delim: "|", ..args)
#let ee = $bold(upright(e))$
#let dang = sym.angle.arc

#let url(s) = {
  link(s, text(font:fonts.mono, s))
}

// Ersatz part command (similar to Koma-Script part in scrartcl)
#let part(s) = {
  heading(numbering: none, text(size: 1.4em, fill: colors.partfill, s))
}

// Unnumbered heading commands
#let h1(..args) = heading(level: 1, outlined: false, numbering: none, ..args)
#let h2(..args) = heading(level: 2, outlined: false, numbering: none, ..args)
#let h3(..args) = heading(level: 3, outlined: false, numbering: none, ..args)
#let h4(..args) = heading(level: 4, outlined: false, numbering: none, ..args)
#let h5(..args) = heading(level: 5, outlined: false, numbering: none, ..args)
#let h6(..args) = heading(level: 6, outlined: false, numbering: none, ..args)

// ============================================================
// BEGIN: Later addition/modification
// ============================================================

// Main entry point to use in a global show rule
#let pdflayout(
  title: none,
  author: none,
  author2: none,
  subtitle: none,
  semester: none,
  date: none,
  maketitle: true,
  report-style: false,
  flipp: false,
  body
) = {
  // B. Apply theme
  show: setup-typography // Uncommenting this line will apply the typography setup from eul/styles/typography.typ (turnings toc chapter, sec color to blue). An effect of uncommenting this line is that the Table of Contents will not show the #part[] stuff if eul/styles/typography.typ has `show outline.entry.where(level: 1)` in line no 16. Now this level has been set to 2.
  // show: setup-headings
  // show: setup-page
  // show: setup-theorems

// ============================================================
// END: Later addition/modification
// ============================================================

  // Set document parameters
  if (title != none) {
    set document(title: title)
  }
  if (author != none) {
    set document(author: author)
  }

  // Figures formatting
  show figure.caption: cap => context {
    set text(0.95em)
    block(inset: (x: 5em), [
      #set align(left)
      #text(weight: "bold")[#cap.supplement #cap.counter.display(cap.numbering)]#cap.separator#cap.body
    ])
  }

  // Table formatting
  show figure.where(kind: table): fig => {
    // Auto emphasize the table headers
    show table.cell.where(y: 0): set text(weight: "bold")
    let tableframe(stroke) = (x, y) => (
      left: 0pt,
      right: 0pt,
      top: if y <= 1 { stroke } else { 0pt },
      bottom: stroke,
    )
    set table(
      stroke: tableframe(rgb("#21222c")),
      fill: (_, y) => if (y==0) { rgb("#ffeeff") } else if calc.even(y) { rgb("#eaf2f5") },
    )
    fig
  }

  // Report parameters
  show ref: it => {
    let el = it.element
    if el != none and el.func() == heading and el.level == 1 and it.supplement == auto and report-style {
      ref(it.target, supplement: "Chapter")
    } else {
      it
    }
  }

// ============================================================
// BEGIN: Later addition/modification
// ============================================================

  // General settings
  set page(
    paper: "a4",
    flipped: flipp,
    margin: auto,
    header: context {
      set align(right)
      set text(size:0.8em)
      if (not maketitle or counter(page).get().first() > 1) {
        text(weight:"bold", title)
        if (author != none) {
          h(0.2em)
          sym.dash.em
          h(0.2em)
          text(style:"italic", author)
        }
      }
    },
    numbering: "1",
  )
  // set block(spacing: 1.2em)
  
  set par(
    first-line-indent: (
      amount: 0.85em,
      all: false,
    ),
    justify: true,
    spacing: 0.75em
    
  )
  set text(
  //   font: fonts.text,
    size: 12pt,
  //   fallback: false,
  )

// ============================================================
// END: Later addition/modification
// ============================================================

  // For bold elements, use sans font
  show strong: set text(font:fonts.sans, size: 0.9em)

  // Theorem environments
  show: thm-rules.with(qed-symbol: $square$)

  // Change quote display
  set quote(block: true)
  show quote: set pad(x:2em, y:0em)
  show quote: it => {
    set text(style:"italic")
    v(-1em)
    it
    v(-0.5em)
  }

  // Indent lists
  set enum(indent: 1em)
  set list(indent: 1em)

  // Section headers
  set heading(numbering: "1.1")
  show heading: it => {
    block([
      #if (it.numbering != none) [
        #text(fill:colors.headers,
          (if (report-style and it.level == 1) { "Chapter " } else { "§" })
          + counter(heading).display()
          + (if (report-style and it.level == 1) { "." } else { "" })
        )
        #h(0.2em)
      ]
      #it.body
      #v(0.4em)
    ])
  }

// ============================================================
// BEGIN: Later addition/modification
// ============================================================

  show heading: set text(font:fonts.sans, size: headsize)
  show heading.where(level: 1): set text(size: headsize + 3pt)
  show heading.where(level: 2): set text(size: headsize + 1pt)

// ============================================================
// END: Later addition/modification
// ============================================================

  // Hyperlinks should be pretty
  show link: it => {
    set text(fill:
      if (type(it.dest) == label) { colors.label } else { colors.hyperlink }
    )
    it
  }

// ============================================================
// BEGIN: Later addition/modification
// ============================================================

show ref: it => {
  let el = it.element

  set text(fill: colors.label)

  if (
    el != none
    and el.func() == heading
    and el.level == 1
    and it.supplement == auto
    and report-style
  ) {
    ref(it.target, supplement: "Chapter")
  } else {
    it
  }
}

  // show ref: it => {
  //   link(it.target, it)
  // }

// ============================================================
// END: Later addition/modification
// ============================================================


  // Gentle clues default font should be sans
  show: gentle-clues.with(
    title-font: "Noto Sans"
  )

// ============================================================
// BEGIN: Later addition/modification
// ============================================================

  // Title page, if maketitle is true
  if maketitle {
    v(2.5em)
    set align(center)
    set block(spacing: 2em)
    block(text(fill:colors.title, size:2.5em, font:fonts.sans, weight:"bold", title))
    if (subtitle != none) {
      block(text(size:2em, font:fonts.sans, weight:"bold", subtitle))
    }
    if (title != none) {
      // block(smallcaps(text(size: 2em, weight:"bold", title)))
    }
    if (semester != none) {
      block(smallcaps(text(size: 2em, semester)))
    }
    if (author != none) {
      block(smallcaps(text(size:1.7em, author)))
    }
    if (author2 != none) {
      block(smallcaps(text(size:1.7em, author2)))
    }
    if (type(date) == datetime) {
      block(text(size:1.2em, date.display("[day] [month repr:long] [year]")))
    }
    else if (date != none) {
      block(text(size:1.2em, date))
    }
    v(1.5em)
  }
  body
}

// ============================================================
// END: Later addition/modification
// ============================================================
