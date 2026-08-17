// src/lec1.typ
#import "../../templates/course.typ": *

#let lecture = (
  file: "lec2",
  type: "lecture",
  number: 1,
  title: "Field extensions",
  category: "Fields and Galois theory",
  tags: ["division algorithm", "Gauss' lemma"],
)

#show: lecture-layout(lecture)

#show: doc => {
  reset-counters(lecture.number)
  doc
}

#page-header(lecture, chap: true)

#include "lec2_content.typ"

#previous-next(lecture)
