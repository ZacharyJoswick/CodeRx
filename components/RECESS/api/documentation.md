# RECESS
## **R**emote **E**xecution, **C**ompilation, and **E**valuation **S**y**S**tem

## Purpose

RECESS is a system designed to handle the compilation and evaluation of arbitrary code in a repeatable and secure environment. Applications include educational coding platforms, code challenges, coding workshops, and others. RECESS uses a simple and effective API that allows integration with virtually any platform, or manual execution through the use of tools like curl.


## General Structure

RECESS is broken out into 4 main modules as described below

### API

The API modules in the central interface by which external users access the RECESS system. The api endpoint allows the user to interact with the RECESS system by submitting jobs and registering for webhooks to be called when the job completes. The api uses the concept of jobs to handle the lifecycle of a request. Jobs are defined below:

#### Job Description

A job is comprised of the following

1. The code to be compiled
2. The set of tests to be run against the code
   1. Sent in as a list of tests
      1. Each test is comprised of a set of inputs and an expected output
      2. The inputs will be sent into the program using standard in
      3. Outputs will be collected from standard out
      4. 