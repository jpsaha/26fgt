// Shared counters
// Declare a single shared counter for all math blocks across a single lecture file
// #let math-counter = counter("math-blocks")
// counters.typ
// ------------------------------------------------------------
// Shared numbering for all mathematical blocks
//
// Example:
// Lecture 3:
//   Definition 3.1
//   Theorem 3.2
//   Exercise 3.3
// ------------------------------------------------------------


// ------------------------------------------------------------
// Current lecture number
// ------------------------------------------------------------

#let current-lecture = state("current-lecture", 0)


#let set-lecture-number(n) = {
  current-lecture.update(n)
}


#let lecture-number() = {
  context current-lecture.get()
}


// ------------------------------------------------------------
// Single shared counter
// ------------------------------------------------------------

#let math-counter = counter("math-block")


// ------------------------------------------------------------
// Reset at beginning of lecture
// ------------------------------------------------------------

#let reset-counters(n) = {
  set-lecture-number(n)
  math-counter.update(0)
}


// ------------------------------------------------------------
// Display number
// ------------------------------------------------------------

#let math-number() = {

  context {

    let lecture = current-lecture.get()
    let block = math-counter.get().first()

    str(lecture) + "." + str(block)

  }

}