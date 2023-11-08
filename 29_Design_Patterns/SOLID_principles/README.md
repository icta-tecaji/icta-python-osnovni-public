# SOLID Principles of Object-Oriented Design

SOLID is a set of five object-oriented design principles that can help you write more maintainable, flexible, and scalable code based on well-designed, cleanly structured classes. These principles are a fundamental part of object-oriented design best practices.

## The SOLID Principles

When it comes to writing classes and designing their interactions in Python, you can follow a series of principles that will help you build better object-oriented code. One of the most popular and widely accepted sets of standards for **object-oriented design (OOD)** is known as the **SOLID** principles.

If you’re coming from C++ or Java, you may already be familiar with these principles. Maybe you’re wondering if the SOLID principles also apply to Python code. To that question, the answer is a resounding yes. If you’re writing object-oriented code, then you should consider applying these principles to your OOD.

But what are these SOLID principles? SOLID is an acronym that groups five core principles that apply to object-oriented design. These principles are the following:

1. Single-responsibility principle (SRP)
2. Open–closed principle (OCP)
3. Liskov substitution principle (LSP)
4. Interface segregation principle (ISP)
5. Dependency inversion principle (DIP)

## Single-Responsibility Principle (SRP)

The single-responsibility principle (SRP) comes from Robert C. Martin, more commonly known by his nickname Uncle Bob, who’s a well-respected figure in the software engineering world and one of the original signatories of the Agile Manifesto. In fact, he coined the term SOLID.

The single-responsibility principle states that: `A class should have only one reason to change.`

**This means that a class should have only one responsibility, as expressed through its methods. If a class takes care of more than one task, then you should separate those tasks into separate classes.**

This principle is closely related to the concept of separation of concerns, which suggests that you should split your programs into different sections. Each section must address a separate concern.

To illustrate the single-responsibility principle and how it can help you improve your object-oriented design, say that you have the following FileManager class: `01_file_manager_srp.py`

In this example, your FileManager class has two different responsibilities. It uses the `.read()` and `.write()` methods to manage the file. It also deals with ZIP archives by providing the `.compress()` and `.decompress()` methods.

This class violates the single-responsibility principle because it has two reasons for changing its internal implementation. To fix this issue and make your design more robust, you can split the class into two smaller, more focused classes, each with its own specific concern: `02_file_manager_srp.py`

Now you have two smaller classes, each having only a single responsibility. `FileManager` takes care of managing a file, while `ZipFileManager` handles the compression and decompression of a file using the ZIP format. These two classes are smaller, so they’re more manageable. They’re also easier to reason about, test, and debug.

**The concept of responsibility in this context may be pretty subjective.** Having a single responsibility doesn’t necessarily mean having a single method. Responsibility isn’t directly tied to the number of methods but to the core task that your class is responsible for, depending on your idea of what the class represents in your code. However, that subjectivity shouldn’t stop you from striving to use the SRP.

## Open-Closed Principle (OCP)

The open-closed principle (OCP) for object-oriented design was originally introduced by Bertrand Meyer in 1988 and means that: `Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification.`

To understand what the open-closed principle is all about, consider the following Shape class: `03_shapes_ocp.py`

The initializer of Shape takes a shape_type argument that can be either "rectangle" or "circle". It also takes a specific set of keyword arguments using the `**kwargs` syntax. If you set the shape type to "rectangle", then you should also pass the width and height keyword arguments so that you can construct a proper rectangle.

In contrast, if you set the shape type to "circle", then you must also pass a radius argument to construct a circle.
