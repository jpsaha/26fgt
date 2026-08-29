// HTML/PDF rendering helpers
// #import "counters.typ": *
#import "counters.typ": (
  math-counter,
  math-number,
  reset-counters,
  lecture-number,
)
#import "utils.typ": is-html
#import "nav.typ": html-nav-header, breadcrumb, download-buttons

// ------------------------------------------------------------
// Lecture metadata display
// ------------------------------------------------------------

#let lecture-info(lecture) = {

  if is-html {

    html.elem(
      "div",
      attrs: (
        class: "lecture-meta",
      ),
    )[

      #if "date" in lecture [
        📅 #lecture.date
        #linebreak()
      ]

      #if "reading" in lecture [
        📖 Reading: #lecture.reading
        #linebreak()
      ]

      #if "duration" in lecture [
        ⏱ Duration: #lecture.duration
        #linebreak()
      ]

      #if "difficulty" in lecture [
        ⭐ Difficulty: #lecture.difficulty
      ]

    ]

  } else {

    // PDF metadata

    if "date" in lecture {
      text(size: 10pt)[
        Date: #lecture.date
      ]
      linebreak()
    }

    if "reading" in lecture {
      text(size: 10pt)[
        Reading: #lecture.reading
      ]
      linebreak()
    }

    if "duration" in lecture {
      text(size: 10pt)[
        Duration: #lecture.duration
      ]
      linebreak()
    }

    if "difficulty" in lecture {
      text(size: 10pt)[
        Difficulty: #lecture.difficulty
      ]
    }

    v(0.5cm)
  }
}

#let page-header(lecture, chap: false) = {
  
  if is-html {
    // html-nav-header()
    breadcrumb(lecture)
    download-buttons(lecture)

    html.elem(
      "h1",
      attrs: (
        style: "font-family: system-ui, sans-serif;
        color: #111;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;"
      ),
    )[
      #if lecture.number != none {
        [#lecture.number. ]
        // [Lecture #lecture.number: ]
      }
      #lecture.title
    ]

    lecture-info(lecture)

  } else {

    // align(center)[
    //   #text(size: 20pt, weight: "bold")[
    //     #if lecture.number != none {
    //       [Lecture #lecture.number: ]
    //     }
    //     #lecture.title
    //   ]

    //   #lecture-info(lecture)

    //   #v(1cm)
    // ]

    if chap {
      text[= #lecture.title]
    }
  }
}

#let block-container(
  counter,
  number-function,
  label-text,
  title,
  primary-color,
  bg-color,
  class-name,
  content,
) = {

  counter.step()

  let full-label = context [#label-text #number-function()]

  if sys.inputs.at("format", default: "pdf") == "html" {

    html.elem(
      "div",
      attrs: (
        class: "math-card " + class-name,
        style:
          "width: 100%;"
          + "border: 1px solid "
          + primary-color
          + ";"
          + "background: none;"
          + "padding: 12px;"
          + "margin: 18px 0;"
          + "border-radius: 5px;"
          + "box-sizing: border-box;"
      ),
    )[

      #html.elem(
        "div",
        attrs: (
          class: "math-card-title",
          style:
            "display: block;"
            + "font-size: 0.9em;"
            + "margin-bottom: 4px;"
        ),
      )[
        #html.elem("strong")[
          #full-label
        ]
        #if title != none [
          (#title).
        ]
      ]

      #html.elem(
        "div",
        attrs: (
          class: "math-card-body",
        ),
      )[
        #content
      ]
    ]


  } else {

  // if sys.inputs.at("format", default: "pdf") == "html" {

  //   html.elem(
  //     "div",
  //     attrs: (
  //       class: "math-card " + class-name,
  //       style:
  //         "border-left: 5px solid "
  //         + primary-color
  //         + "; background-color: "
  //         + bg-color
  //         + "; padding: 18px; margin: 24px 0; border-radius: 0 4px 4px 0;"
  //     ),
  //   )[

  //     #html.elem(
  //       "strong",
  //       attrs: (
  //         class: "math-card-title",
  //         style:
  //           "color: "
  //           + primary-color
  //           + "; display:block; font-size:1.1em;"
  //       ),
  //     )[
  //       #full-label#if title != none [ (#title)].
  //     ]


  //     #html.elem(
  //       "div",
  //       attrs: (
  //         class: "math-card-body",
  //       ),
  //     )[
  //       #content
  //     ]
  //   ]


  // } else {

    // block(
    //   width: 100%,
    //   stroke: (left: 4pt + rgb(primary-color)),
    //   fill: rgb(bg-color),
    //   inset: 12pt,
    //   radius: (right: 4pt),
    //   breakable: true,
    // )[

    //   #text(
    //     weight: "bold",
    //     fill: rgb(primary-color),
    //     size: 1.1em,
    //   )[
    //     #full-label#if title != "" [: #title]
    //   ]

    //   #v(4pt)

    //   #content
    // ]

block(
  width: 100%,
  stroke: 0.9pt + rgb(primary-color),
  fill: none,
  inset: 9pt,
  radius: 5pt,
  breakable: true,
)[
  #text(weight: "bold", size: 0.9em)[#full-label]#if title != none [ (#title)].
  #content
]

    // block(
    //   width: 100%,
    //   stroke: rgb(primary-color) + 0.9pt,
    //   fill: none,
    //   inset: 9pt,
    //   radius: 5pt,
    //   breakable: true,
    //   // fill: none, stroke: rgb("#ead116e4"), 
    // )[

    //   #text(
    //     weight: "bold",
    //     // fill: rgb(primary-color),
    //     size: 0.9em,
    //   )[
    //     #full-label
    //   ]
    //   #if title != "" [(#title)]
    //   .
    //   // #v(4pt)
    //   #content
    // ]

  }
}

#let setup-document(doc) = {
  if is-html {
    doc
  } else {
    set page(
      paper: "a4",
      margin: (x: 2.5cm, y: 2.5cm),
      height: 29.7cm,
    )

    set text(
      size: 11pt,
      font: "Liberation Serif",
    )

    doc
  }
}

// ------------------------------------------------------------
// Typeset one lecture inside a combined book
// ------------------------------------------------------------
//
// Used by:
//   generated/book.typ
//   generated/category_*.typ
//
// Keeps the same lecture rendering for the complete course
// book and for category-specific books.

#let include-lecture(lecture, body) = [
  #pagebreak()

  // Reset counters only when a lecture number exists.
  // This keeps the function safe for future non-numbered
  // content as well.
  #if lecture.number != none {
    reset-counters(lecture.number)
  }

  // #align(center)[
  //   #text(
  //     size: 1.8em,
  //     weight: "bold",
  //   )[
  //     #if lecture.number != none [
  //       Lecture #lecture.number
  //     ] else [
  //       #lecture.title
  //     ]
  //   ]

  //   #v(0.4em)

  //   #if lecture.number != none [
  //     #text(
  //       size: 1.4em,
  //     )[
  //       #lecture.title
  //     ]
  //   ]

  //   #v(1em)
  // ]

  = #lecture.title
  #body
]
