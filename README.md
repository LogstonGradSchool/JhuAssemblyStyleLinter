# Assembly Style Linter

This linter was designed with Prof. Charles Kann's Computer Organization
(EN.605.204) course in mind. It performs a strict but non-exhaustive lint;
meaning it will not catch all errors but will be noisy and exacting about those
that it does.

## Install

```
pip install jhu-assembly-linter
```

## Usage

```
$ jhu-assembly-linter ./path/to/file.s

E:: Tab found. Only spaces allowed.
18:     LDR x0, =helloWorld
    ^
E:: Instruction is not uppercase.
19:     mov     w8, #64     /* write is syscall #64 */
        ^
E:: Non-functional whitespace found.
20: 
    ^^^^^
E:: File name does not end with "Main" when it should.
21: main:
```

To lint a whole directory:

```
find . -name "*.s" | xargs -I{} jhu-assembly-linter  {}
```

SOON TO BE IMPLEMENTED:
To add a pre-commit hook:
```
repos:
-   repo: https://github.com/LogstonGradSchool/JhuAssemblyStyleLinter
    rev: v0.1.0
    hooks:
    -   id: jhu-assembly-linter
```

### Tests

```
tox
```

### Deployment

```
poetry build
poetry publish
```
