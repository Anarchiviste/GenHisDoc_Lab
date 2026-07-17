---
title : Guidelines for Historical Corpora Annotations for Computer Vision Detection.
date : 26/06/2026
author : Jules Musquin
--- 

# Introduction 

This document describes guidelines for annotating historical corpora for image detection and retrieval tasks. Designed primarily for manuscripts (codices) and printed books, they also apply to various types of documents such as newspaper articles, photographs, or scrolls.

The page of a historical document is composed of text, illustrations, ornamentation, and other elements that, in most cases, adhere to two types of rules. For printed books, there are technical rules—called standards—that correspond to the industry's established production standards. These rules stem from the artisanal tradition (initials, typefaces) of bookmaking before the invention of printing. This tradition corresponded to the social norms that defined the standards of artisanal production and their adaptation over time.

Our goal is to extract visual elements without regard to the text or the document's meaning. These guidelines aim to obtain relevant annotations for training and testing machine learning algorithms. They focus on annotating typical visual elements at the page level, without considering text. We do not perform finer-grained classification, such as creating semantic links between illustrations.

# Definition

You will be annotating the corpus of documents with 5 classes to describe elements inside historicals documents : 

- 0: "Illustration"
- 1: "Ornament"
- 2: "Initial"
- 3: "Stamp"
- 4: "Table"

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