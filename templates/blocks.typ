// theorem / definition / exercise
#import "render.typ": block-container
#import "colors.typ": block-colors
#import "block-engine.typ": make-block

// └── imports utils.typ



#import "counters.typ": (
  math-counter,
  math-number,
)

#import "render.typ": block-container
#import "counters.typ": (
  math-counter,
  math-number,
)


// // ------------------------------------------------------------
// // Theorem
// // ------------------------------------------------------------

// #let theorem(title: "", content) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Theorem",
//     title,
//     "#0066cc",
//     "#f0f7ff",
//     "theorem",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Definition
// // ------------------------------------------------------------

// #let definition(title: "", content) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Definition",
//     title,
//     "#2e7d32",
//     "#f1f8e9",
//     "definition",
//     content,
//   )

// }

// // ------------------------------------------------------------
// // Note
// // ------------------------------------------------------------

// #let note(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Note",
//     title,
//     "#1565c0",
//     "#e3f2fd",
//     "note",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Warning
// // ------------------------------------------------------------

// #let warning(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Warning",
//     title,
//     "#ef6c00",
//     "#fff3e0",
//     "warning",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Example
// // ------------------------------------------------------------

// #let example(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Example",
//     title,
//     "#6a1b9a",
//     "#f3e5f5",
//     "example",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Remark
// // ------------------------------------------------------------

// #let remark(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Remark",
//     title,
//     "#616161",
//     "#f5f5f5",
//     "remark",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // History
// // ------------------------------------------------------------

// #let history(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "History",
//     title,
//     "#795548",
//     "#efebe9",
//     "history",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Lemma
// // ------------------------------------------------------------

// #let lemma(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Lemma",
//     title,
//     "#1565c0",
//     "#e8f1ff",
//     "lemma",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Proposition
// // ------------------------------------------------------------

// #let proposition(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Proposition",
//     title,
//     "#0277bd",
//     "#e1f5fe",
//     "proposition",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Corollary
// // ------------------------------------------------------------

// #let corollary(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Corollary",
//     title,
//     "#00838f",
//     "#e0f7fa",
//     "corollary",
//     content,
//   )

// }


// // ------------------------------------------------------------
// // Claim
// // ------------------------------------------------------------

// #let claim(
//   title: "",
//   content,
// ) = {

//   block-container(
//     math-counter,
//     math-number,
//     "Claim",
//     title,
//     "#5e35b1",
//     "#ede7f6",
//     "claim",
//     content,
//   )

// }

// ------------------------------------------------------------
// Proof
// ------------------------------------------------------------

#let proof(
  title: "",
  content,
) = {

  if sys.inputs.at("format", default: "pdf") == "html" {

    html.elem(
      "div",
      attrs: (
        class: "proof-block",
        style:
          "margin: 20px 0; padding-left: 18px; border-left: 4px solid #2e7d32;",
      ),
    )[

      #html.elem(
        "strong",
      )[
        Proof#if title != "" [: #title].
      ]

      #v(0.5em)

      #content

      #align(right)[□]

    ]

  } else {

    block(
      inset: 6pt,
      stroke: (left: 3pt + rgb("#2e7d32")),
    )[

      #text(weight: "bold")[
        Proof#if title != "" [: #title].
      ]

      #v(4pt)

      #content

      #align(right)[□]

    ]

  }

}

// ------------------------------------------------------------
// Exercise
// ------------------------------------------------------------

#let exercise(
  title: "",
  solution: none,
  content,
) = {

  math-counter.step()

  let full-label = context [
    Exercise #math-number()
  ]


  if sys.inputs.at("format", default: "pdf") == "html" {

    html.elem(
      "div",
      attrs: (
        class: "math-card exercise",
        style:
          "border-left: 5px solid #c62828;
           background-color: #ffebee;
           padding: 18px;
           margin: 24px 0;
           border-radius: 0 4px 4px 0;"
      ),
    )[

      #html.elem(
        "strong",
        attrs: (
          class: "math-card-title",
          style:
            "color: #c62828;
             display: block;
             font-size: 1.1em;
             margin-bottom: 8px;"
        ),
      )[

        #full-label
        #if title != none [ (#title)].

      ]


      #html.elem(
        "div",
        attrs: (
          class: "math-card-body",
        ),
      )[

        #content

      ]


      #if solution != none {

        html.elem(
          "details",
          attrs: (
            class: "exercise-solution-panel",
            style:
              "margin-top: 14px;
               background-color: #ffffff;
               border: 1px solid #ffcdd2;
               border-radius: 6px;
               padding: 12px;"
          ),
        )[

          #html.elem(
            "summary",
            attrs: (
              style:
                "font-weight: bold;
                 color: #c62828;
                 cursor: pointer;"
            ),
          )[

            💡 Click to Reveal Solution

          ]


          #html.elem(
            "div",
            attrs: (
              class: "solution-body",
              style:
                "margin-top: 10px;
                 padding-top: 8px;
                 border-top: 1px dashed ffcdd2;"
            ),
          )[

            #solution

          ]

        ]

      }

    ]


  } else {
    // block(
    //   width: 100%,
    //   stroke: (left: 4pt + rgb("#c62828")),
    //   fill: rgb("#ffebee"),
    //   inset: 12pt,
    //   radius: (right: 4pt),
    //   breakable: true,
    // )[

    //   #text(
    //     weight: "bold",
    //     fill: rgb("c62828"),
    //     size: 1.1em,
    //   )[

    //     #full-label
    //     #if title != "" [: #title]

    //   ]

    //   #v(4pt)

    //   #content

    block(
      width: 100%,
      stroke: 0.9pt + rgb("#c62828"),
      fill: none,
      inset: 9pt,
      radius: 5pt,
      breakable: true,
    )[

      #text(
        weight: "bold",
        size: 0.9em,
      )[

        #full-label
      ]
        #if title != none [ (#title)].

      #v(4pt)

      #content

      #if solution != none [

        #v(8pt)

        #line(
          length: 100%,
          stroke: 0.5pt + rgb("ffcdd2"),
        )

        #text(
          weight: "bold",
          fill: rgb("c62828"),
        )[Solution:]

        #v(4pt)

        #solution

      ]

    ]

  }

}


// #let exer(title: none, content) = make-block("exer", "Exercise", title, content)

// #let thm(title: none, content) = make-block("thm", "Theorem", title, content)

// #let defn(title, content) = make-block("definition", "Definition", title, content)

// #let defn(..args) = {
//   let args = args.pos()

//   if args.len() == 1 {
//     make-block("definition", "Definition", none, args.at(0))
//   } else {
//     make-block("definition", "Definition", args.at(0), args.at(1))
//   }
// }
// #let thm(..args) = {
//   let args = args.pos()

//   if args.len() == 1 {
//     make-block("thm", "Theorem", none, args.at(0))
//   } else {
//     make-block("thm", "Theorem", args.at(0), args.at(1))
//   }
// }
// #let exer(..args) = {
//   let args = args.pos()

//   if args.len() == 1 {
//     make-block("exer", "Exercise", none, args.at(0))
//   } else {
//     make-block("exer", "Exercise", args.at(0), args.at(1))
//   }
// }
// 

#let make-block-arg(kind, label) = {
  (..args) => {
    let args = args.pos()

    if args.len() == 1 {
      make-block(kind, label, none, args.at(0))
    } else {
      make-block(kind, label, args.at(0), args.at(1))
    }
  }
}

#let theorem = make-block-arg("theorem", "Theorem")
#let thm = make-block-arg("theorem", "Theorem")
#let definition = make-block-arg("definition", "Definition")
#let defn = make-block-arg("definition", "Definition")
// #let exercise = make-block-arg("exercise", "Exercise")
#let exer = make-block-arg("exercise", "Exercise")
#let lemma = make-block-arg("lemma", "Lemma")
#let proposition = make-block-arg("proposition", "Proposition")
#let corollary = make-block-arg("corollary", "Corollary")
#let claim = make-block-arg("claim", "Claim")
#let example = make-block-arg("example", "Example")
#let note = make-block-arg("note", "Note")
#let warning = make-block-arg("warning", "Warning")
#let remark = make-block-arg("remark", "Remark")
#let history = make-block-arg("history", "History")

// #let theorem(title: "", content) = make-block("theorem", "Theorem", title, content)

// #let definition(title: "", content) = make-block("definition", "Definition", title, content)

// #let lemma(title: "", content) = make-block("lemma", "Lemma", title, content)

// #let proposition(title: "", content) = make-block("proposition", "Proposition", title, content)

// #let corollary(title: "", content) = make-block("corollary", "Corollary", title, content)

// #let claim(title: "", content) = make-block("claim", "Claim", title, content)

// #let example(title: "", content) = make-block("example", "Example", title, content)

// #let note(title: "", content) = make-block("note", "Note", title, content)

// #let warning(title: "", content) = make-block("warning", "Warning", title, content)

// #let remark(title: "", content) = make-block("remark", "Remark", title, content)

// #let history(title: "", content) = make-block("history", "History", title, content)
