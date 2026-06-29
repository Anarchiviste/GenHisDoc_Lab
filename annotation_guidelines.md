---
title : Guidelines for Historical Corpora Annotations for Computer Vision.
date : 26/06/2026S
author : Jules Musquin
--- 

# Introduction 

This document describe guidelines to annotate an historical corpora for detection and images retrival tasks. Made with the primary goal to work on manuscripts(codex) and printed books, this guidelines where also used to annotate press, photography and scrolls.

The page of an historical document are composed between, text, illustrations, ornaments and other elements that in most cases follow mostly two rules. 
- For printed books, there are technicals rules - called standards - that are the way an industry as adapted to uniformize the production of an element. These rules were also the child of a tradition of artisanal book crafting.

- This tradition are socials rules that are the way an artisanal production adapted in the long term

# Definition

This dataset use 5 classes to describe elements inside historicals documents : 

- 0: "Illustration"
- 1: "Ornament"
- 2: "Initial"
- 3: "Stamp"
- 4: "Table"

# A short introduction in the element of text morphology. 

## Illustration

The illustration class should be understood as a generic class for all graphic elements. An illustration can be functional or artistic, whose function is to inform, illustrate, or entertain the reader.

Some examples of illustrations in an image are paintings, photographs, drawings, mathematical graphs, charts, diagrams, symbols, maps. The difference between an illustration and a decoration is the particular semantics of an illustration which reads in relation to the text.

On the title page, the printer's mark should be annotated as an illustration.

## Ornament

An ornament is a graphic element that decorates or embellishes a document without contributing to the illustration and understanding of the text.

An ornament is most often an abstract form of illustration, composed of classical patterns (plant ornaments, abstract headpieces, "cul-de-lampe") or repetitive motifs with no meaning other than their intrinsic value as ornaments.

## Initial

An inital letter is a letter placed at the start of a text, a paragraph or a page to signify the start of the text. We can divide initials into two category : 

- The principal initials, at the start of a book, a new section, a new chapter. They can be decorated (illuminated, historiated) or not. 

- Secondary initials, at the start of every paragraphs, a lot of the time a simplier and easier to drown or print.

- The pilcrow (¶) is a sign used to identify a paragraph. In manuscripts this sign can be mistaken for an initial. It must not be annotated.

We actually only want to annotate the most important initials. It's not possible to establish standard rules for annotating initials, but we can base ourselves on the following principle: "If an initial appears large, important, and aesthetically pleasing in the context of the text, then it should be annotated as an initial."

## Stamp

Stamps are marks that identify the institutions that hold or held the documents (libraries, archives). These markings are not all the same depending on the document and the date they were applied to the work.

For bound documents (books, manuscripts, albums), the stamp is on the first page. For a stack of unbound documents, each loose page will be stamped.

Manuscripts and old books in France (except for the national library) have moved between several libraries and therefore often have several stamps which all need to be annotated.

Before the widespread use of the stamp, book owners used a handwritten bookplate on the title page; this phrase should not be annotated as a stamp.

## Table

A table is an arrangement of information or data, usually in rows and columns, or possibly according to a more complex structure. 

For tables, the header and the footer must taken inside the annotation if it is present. 

In historical documents, some informations can have a circular representation and should be annotated as table. 