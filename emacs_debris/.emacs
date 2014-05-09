(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(org-agenda-files (quote ("~/org/current.org")))
 '(tab-stop-list (quote (4 8 12 16 20 24 28 32 36 40 44 48 52 56 60)))
 '(tool-bar-mode nil)
 '(tooltip-mode nil)
 '(transient-mark-mode t))
(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(default ((t (:stipple nil :background "SystemWindow" :foreground "SystemWindowText" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 83 :width normal :family "Andale Mono"))))
 '(mode-line ((t (:background "grey" :foreground "black" :box (:line-width -1 :style released-button))))))

;; Added 2/26/2009
;; Helps integrate the info directories for the Cygwin stuff
;; into the existing framework?
;; I'm not entirely sure that this is the right thing to do, though:
;; ("c:/Program Files/emacs-22.3/info/" "c:/cygwin/usr/share/info/")
;; Therefore, I will try adding the directory for Cygwin's info-files
;; to the set of default paths that Emacs searches when building
;; its list of directories to use. I am not entirely sure that this
;; is the right thing to do, so I will have to be careful when fiddling
;; with this stuff from here on out.
;; What this does is cause the display of the Cygwin info directory
;; file's information, followed by the Emacs info directory file's
;; stuff. Makes looking up the info file stuff for Emacs a little
;; more painful, but hopefully this is a less-invasive setting.
(setq Info-default-directory-list
      (append Info-default-directory-list '("c:/cygwin/usr/share/info")))
;; 

;; Added 2/25/2009
;; to support Remember Mode.
; This is for Remember Mode integration with Org Mode:
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/remember")
(require 'remember)
;; The following three sexp's may or may not be necessary.
;; The instructions said, "If you are, like me, missing the function
;; org-remember-insinuate, try the following." 
;;
;; Ah! Since M-x apropos tells me that I already have a function
;; called org-remember-insinuate, I guess I can omit the following
;; three sexp's from this initialization file for now.
;; (setq remember-annotation-functions '(org-remember-annotation))
;; (setq remember-handler-functions '(org-remember-handler))
;; (add-hook 'remember-mode-hook 'org-remember-apply-template)
;; 
;; The following four expr's are from Section 9.1 of the Org Mode
;; documentation:
(org-remember-insinuate)
(setq org-directory "~/org")
(setq org-default-notes-file (concat org-directory "/notes.org"))
(setq org-expenses-file (concat org-directory "/expenses.org"))
(define-key global-map "\C-cr" 'org-remember)
(setq org-remember-templates
      (list
       '("Todo" ?t "* TODO %?\n  %i\n  %a"
	  ;; "~/org/TODO.org" "Tasks"
	 )
       (list "Journal" ?j "* %U %?\n\n  %i\n" org-default-notes-file "JOURNALING" )
	;; ("Journal" ?j "* %U %?\n\n  %i\n  %a" "~/org/JOURNAL.org")
	;; ("Idea" ?i "* %^{Title}\n  %i\n  %a" "~/org/JOURNAL.org" "New Ideas"))
       (list "Marker" ?m "* %U %?\n\n  %i\n" org-default-notes-file "MARKERS" )
       (list "Needs"  ?x "* %U %?\n\n  %i\n" org-expenses-file      "MONTHLY NEEDS")
       (list "Discretionary expense" ?d "* %U %?\n\n  %i\n" org-expenses-file "NON-MONTHLY NEEDS")
      ) )
;; The Remember Mode setup instructions say the following three 
;; sexp's are needed in order to integrate with Planner Mode, which
;; I don't currently have set up...
;; (require 'remember-planner)
;; (setq remember-handler-functions '(remember-planner-append))
;; (setq remember-annotation-functions planner-annotation-functions)
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Added 2/24/2009:
;; Settings for org-mode:
;; The really lovely thing about all this is that it's possible to just
;; mark one of these expr's and then execute M-x eval-region!
;; 
(add-to-list 'auto-mode-alist '("\\.org\\'" . org-mode))
(global-set-key "\C-cl" 'org-store-link)
(global-set-key "\C-ca" 'org-agenda)
; This activates the font-lock mode for the benefit of org mode?
(global-font-lock-mode 1)                     ; for all buffers
; Suggested by the David O'Toole tutorial:
(setq org-log-done 'note)
; This is for calendar/diary integration:
(setq org-agenda-include-diary nil)
; Sets Org mode so that the TAB key DOES NOT fold-up/unfold plain list
; nodes. 
(setq org-cycle-include-plain-lists nil)

;; Added [2009-05-05 Tue]
;; to support CEDET tools.
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/cogre")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/common")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/contrib")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/ede")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/eieio")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/semantic")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/speedbar")
(add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/srecord")
;; (add-to-list 'load-path "c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/tests")

(setq Info-additional-directory-list
      ;; (append Info-additional-directory-list
	      '("c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/common"
		"c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/cogre"
		"c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/contrib"
		"c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/ede"
		"c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/eieio"
		"c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/semantic"
		"c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/speedbar"
		"c:/Program Files/emacs-22.3/lisp/cedet-1.0pre6/srecord" )
	;;      )
      )
;;
;; [2009-05-22 Fri 11:00]
(setq bookmark-save-flag 1)
