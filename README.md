# Table Reasoning: Knowing What Evidence Is Enough

## About the project

We are studying how large language models (LLMs) answer questions about tables. Getting the right answer often means finding the right information in the table and checking whether there is enough information to answer at all.

A model should not guess when important information is missing. We want to understand how well models recognize the evidence they need and when they should say that the table does not provide enough evidence.

## Research questions

1. Can LLMs identify the information needed to answer a question? Which kinds of questions are harder for them?
2. When some table information is missing, can LLMs tell whether there is still enough evidence to answer?
3. Can LLMs point to the parts of a table that support their answers? Does the way a table is organized affect this?

## Our approach

We plan to test LLMs on questions about tables, including cases where some relevant information is unavailable. We will compare their answers and their judgments about whether the evidence is sufficient. We will also look at which parts of the table they use to support their answers.

## Project status

This project is ongoing. We will use this repository to keep our research notes, experiments, code, and findings as the work develops.


## Project

Project 2: Table Reasoning: Knowing What Evidence Is Enough
Members: Shula and Ahmed

Large language models are increasingly used to answer questions over tables, but producing a correct answer requires more than simply reading individual cells. A model must identify the relevant parts of the table, determine whether the available information is sufficient to answer the question, and reason correctly over the selected evidence. For example, answering "Which department had the largest increase in enrollment?" requires finding enrollment values for multiple departments and years and comparing their changes. If some of these values are missing, a reliable system should recognize that there is not enough evidence to answer the question rather than guessing.

In this project, we will investigate how well large language models identify and reason about evidence in tables. Using existing table question-answering and reasoning benchmarks, we will study three research questions: (1) Can language models identify the evidence needed to answer a question, and for what types of questions is this difficult? (2) Given a question and only part of a table, can a model determine whether the available evidence is sufficient to answer it? and (3) Can a model accurately identify which parts of a table support its answer, and how do properties of the table's structure affect its reasoning?

Students will experiment with different types of table questions, systematically vary the evidence and table structure presented to language models, and analyze when their answers and evidence judgments succeed or fail. Students will gain experience with large language models, table question answering, data processing, experimental design, and empirical evaluation. The project will produce an experimental framework and an empirical study of evidence identification, evidence sufficiency, and reasoning over structured tables.


