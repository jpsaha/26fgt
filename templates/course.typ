// Public API
#import "utils.typ": is-html
#import "counters.typ": (
  math-counter,
  math-number,
  reset-counters,
  lecture-number,
)
#import "render.typ": block-container, page-header, setup-document, lecture-info, include-lecture
#import "blocks.typ": theorem, thm, definition, defn, exercise, exer, note, warning, example, remark, history, proof, corollary, lemma, proposition, claim
#import "nav.typ": html-nav-header, previous-next
#import "colors.typ"
#import "code.typ": (
  python,
  sage,
  lean,
  julia,
  asy,
)

#let lecture-layout(lecture) = {
  if sys.inputs.at("format", default: "pdf") == "pdf" {
    import "pdflayout.typ": *
    pdflayout.with(
      title: lecture.title,
      report-style: true,
      flipp: false,
    )
  } else {
    doc => doc
  }
}

#let eqn(s) = {
  set math.equation(numbering: "(1)")
  s
}
