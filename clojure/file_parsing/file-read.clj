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
     ; In the following case, we "put the newline character back."
     (= \newline char1) [ field curr ] )   ) )

; Uses "destructuring" into sequence-typed things
; to pick apart strings?  Not sure this is sensible, idiomatic
; Clojure, but is kind of consistent with the screwy way
; we're forced to deal with strings due to Java-underneath?
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
    ;; (println "REGULAR-FIELD")
    ;; (println field)
    ;; (println char1)
    ;; (println rest-of-string)
    ;; (println)
    (cond
     (= \, char1) [(apply str field) rest-of-string]
     (= \newline char1) [(apply str field) curr]
     true (recur (conj field char1) rest-of-string) ) ) )

(defn start-a-field
  [ field curr ]
  (let
      [ char1 (get curr 0)
	rest-of-string (subs curr 1) ]
    ;; (println "START-A-FIELD")
    ;; (println field)
    ;; (println char1)
    ;; (println rest-of-string)
    ;; (println)
    (cond
     ; (= \, char1) (recur field rest-of-string)
     ; (= \, char1) (recur (conj field "") rest-of-string)
     (= \, char1) [ "" rest-of-string ] 
     ;; (= \newline char1) [(apply str field) curr]
     (= \newline char1) [(apply str field) curr]
     (= \" char1) (quoted-field field rest-of-string)
     true (regular-field (conj field char1) rest-of-string) ) ) )

(defn parse-record
  [ fields curr ]
  (let
      [ field-and-rec              (start-a-field [] curr)
	char1 (get (get field-and-rec 1) 0)
	rest-of-string (subs (get field-and-rec 1) 1)     ]
    (println "PARSE-RECORD")
    (println (get field-and-rec 0))
    (println char1)
    (println rest-of-string)
    (println)
    (cond
     (= \newline char1) (conj fields (get field-and-rec 0))
     true (recur (conj fields (get field-and-rec 0)) (get field-and-rec 1)  ) ) ) )

;; Should like to be able to read in a bunch of those "records"
;; and then build "maps" out of them, so that we can then
;; execute pattern-matching against the description fields, in order
;; to classify the "records."