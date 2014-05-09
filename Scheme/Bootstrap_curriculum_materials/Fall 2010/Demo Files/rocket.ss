;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname rocket) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
(require "Teachpacks/function-teachpack.rkt")

;;;; YOUR CODE HERE
(define (rocket-height t)
  (* 7 t))

(EXAMPLE (rocket-height 3) (* 3 7))
(start rocket-height)