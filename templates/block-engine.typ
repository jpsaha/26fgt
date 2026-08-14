#import "colors.typ": block-colors
#import "render.typ": block-container
#import "counters.typ": (
  math-counter,
  math-number,
)

#let make-block(
  kind,
  label,
  title,
  content,
) = {

  let c = block-colors.at(kind)

  block-container(
    math-counter,
    math-number,
    label,
    title,
    c.border,
    c.bg,
    kind,
    content,
  )

}
