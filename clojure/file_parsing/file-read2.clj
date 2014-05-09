; (:require [clojure.java.io :as io])
; (require '[clojure.java.io :as io])
; (require '[clojure.string :as strlib])

(def rec-output (fn [str] (println str)) )

; What needs to accumulate:
; + present field contents derived thus far
; + the separator
; + the source string
; + 

; (def parse-by-sep
;      [sep str field-map]
;      (cond
;       (= '() (rest str)) 
;       (= sep (first str)) 

(defn end-of-quoted
  [ field curr ]
  (let
      [ char1          (get curr 0)
        rest-of-string (subs curr 1) ]
    (cond
     (= \, char1) [ field rest-of-string ]
     (= \newline char1) [ field rest-of-string ] ) ) )

(defn quoted-field
  [ field curr ]
  (let
      [ char1          (get curr 0)
        rest-of-string (subs curr 1) ]
    (cond
     (= \" char1) (end-of-quoted (apply str field) rest-of-string)
     true (recur (conj field char1) rest-of-string) ) ) )

(defn regular-field
  [ field curr ]
  (let
      [ char1 (get curr 0)
        rest-of-string (subs curr 1) ]
    (cond
     (= \, char1) [(apply str field) rest-of-string]
     (= \newline char1) [(apply str field) rest-of-string]
     true (recur (conj field char1) rest-of-string) ) ) )

(defn start-a-field
  "Truly the heart of the fsm used to parse text-file \"records.\""
  [ field curr ]
  (let
      [ char1 (get curr 0)
        rest-of-string (subs curr 1) ]
    (cond
     (or (= \, char1) (= \newline char1)) [ (apply str field) rest-of-string ]
     (= \" char1) (quoted-field field rest-of-string)
     true (regular-field (conj field char1) rest-of-string) ) ) )

;; Should like to be able to read in a bunch of those "records"
;; and then build "maps" out of them, so that we can then
;; execute pattern-matching against the description fields, in order
;; to classify the "records."

(defn parse-record
  "Drives the invocations of the start-a-field fsm function."
  [ fields curr ]
  (cond
   (= (.length curr) 0) fields
   true (let
            [ field-and-rec (start-a-field [] curr) ]
          (recur (conj fields (get field-and-rec 0)) (get field-and-rec 1)) ) ) )


(println 
(let
  [ mapped
    (map
     (fn [k v] [k v])
     [:k1 :k2 :k3]
     (parse-record [] ",\"DEV,comma-inside\",field3\n") )
    ;;
    reduced
    (reduce (fn [mm kv] (assoc mm (get kv 0) (get kv 1))) {} mapped)  ]
  [ mapped reduced ] )
)

;; This is an example of how to use the marvelous map function:
(println 
(map
 (fn [k v] [k v])
 [:k1 :k2 :k3]
 (parse-record [] "field1,field2,field3\n"))
)

;; The process of creating a map out of the record is a
;; map-reduce couplet, right?
(println 
(reduce
 (fn [ mm kv ] (assoc mm (get kv 0) (get kv 1) ) )
 {} ;; this is an "initially empty" associative map...
 ;;
 ;; The following map expression defines a vector of
 ;; vector-pairs of keys-and-values, which allows us to
 ;; pair fields off with their "names."
 (map
  (fn [k v] [k v])
  [:k1 :k2 :k3]
  (parse-record [] ",\"D,comma-inside\",field3\n")) )
)
;;   (parse-record [] ",\"DEV,comma-inside\",\"ABC\",,fi\"rst,\n") ) )

;; This is kind of astonishing.  Many more lines of Java or Python would
;; be required to do the same things?

;
; Need a way to create a set of rules to assign a "category" to each
; record based on the contents of the record.
;
; I now understand why people make such a fuss over the use of map-reduce
; and its general applicability to many information processing situations.
; 

;; Been watching Hickey's video on "Clojure for Lisp Programmers"
;; and it has helped make a lot of things much more plain than
;; they were before.  And, oh, my goodness, Clojure truly is a 
;; tour-de-force and a graphic, in-your-face demonstration of
;; Greenspun's Tenth Rule, done right!