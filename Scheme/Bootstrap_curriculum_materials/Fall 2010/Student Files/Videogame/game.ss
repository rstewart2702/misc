;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname game) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f ())))
(require "../Teachpacks/bootstrap-teachpack.rkt")

;; Game title: Write the title of your game here
(define TITLE "My Game")
(define TITLE-COLOR "white")
(define DIRECTION "left")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Graphics - object, target, projectile and player images
(define BACKGROUND (rectangle 640 480 "solid" "black"))
(define OBJECT (circle 20 "solid" "green"))
(define TARGET (triangle 30 "solid" "red"))
(define PLAYER (rectangle 30 30 "solid" "gray"))
(define PROJECTILE (star 5 20 40 "solid" "yellow"))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Updating Code

; update-object: Number -> Number ;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; given the object's x-coordinate, output the NEXT x
(define (update-object objectX)
  objectX)

;; write examples for update-object below this line


; update-target : Number -> Number ;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; given the target's x-coordinate, output the NEXT x
(define (update-target targetX)
  targetX)

;; write examples for update-target below this line


; update-projectile : Number -> Number ;;;;;;;;;;;;;;;;;;;;;;;;
; given the projectile's x-coordinate, output the NEXT x
(define (update-projectile projectileX)
  projectileX)

;; write examples for update-projectile below this line


; update-player : Number String -> Number ;;;;;;;;;;;;;;;;;;;;;
; given the player's y-coordinate and a direction, output the NEXT y
(define (update-player playerY dir)
  playerY)

;; write examples for update-player below this line


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Geometry Functions

; distance : Number Number Number Number -> Boolean ;;;;;;;;;;;
(define (distance pX pY cX cY)
  0)

; collide? : Number Number Number Number -> Boolean ;;;;;;;;;;;
; given the player's x and y, and a Character's x and y, did they collide?
(define (collide? pX pY cX cY)
  false)

; offscreen? : Number Number -> Boolean ;;;;;;;;;;;;;;;;;;;;;;
; given a character's x and y tell if the character is OFFS the screen
(define (offscreen? x y)
  false)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; PROVIDED CODE

(test-frame TITLE BACKGROUND OBJECT TARGET PLAYER PROJECTILE)


(START TITLE TITLE-COLOR 
       BACKGROUND OBJECT TARGET PLAYER PROJECTILE
       DIRECTION
       update-player update-target update-object update-projectile
       collide? offscreen?)